#!/usr/bin/env python3
"""校验开放知识目录。只在内容开发/发布使用，不是剪辑运行引擎。"""
import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills/jianying-video-planning'
SCHEMA = SKILL / 'references/planning-catalog-v2.schema.json'


def parse_json(text):
    """拒绝重复键及非 JSON 数值，避免消费者解析结果不一致。"""
    def pairs(values):
        result = {}
        for key, value in values:
            if key in result:
                raise ValueError(f'catalog_duplicate_key: {key}')
            result[key] = value
        return result
    def constant(value):
        raise ValueError(f'catalog_schema_invalid: {value}')
    return json.loads(text, object_pairs_hook=pairs, parse_constant=constant)


def schema_errors(value, rule, root, location='$'):
    """执行本仓 Schema 使用的有限关键字集合；不宣称实现完整 JSON Schema。"""
    known = {'$schema', '$id', '$defs', '$ref', 'type', 'const', 'enum', 'properties',
             'required', 'additionalProperties', 'items', 'minItems', 'uniqueItems', 'minLength', 'pattern'}
    if set(rule) - known:
        return [f'{location}: unsupported schema keyword']
    if '$ref' in rule:
        name = rule['$ref']
        if not name.startswith('#/$defs/') or name[8:] not in root['$defs']:
            return [f'{location}: invalid schema reference']
        return schema_errors(value, root['$defs'][name[8:]], root, location)
    errors = []
    if 'const' in rule and value != rule['const']:
        errors.append(f'{location}: const')
    if 'enum' in rule and value not in rule['enum']:
        errors.append(f'{location}: enum')
    types = {'object': dict, 'array': list, 'string': str, 'boolean': bool}
    kind = rule.get('type')
    if kind and type(value) is not types.get(kind):
        return errors + [f'{location}: expected {kind}']
    if kind == 'object':
        props = rule.get('properties', {})
        errors += [f'{location}.{key}: missing' for key in rule.get('required', []) if key not in value]
        for key, item in value.items():
            if key in props:
                errors += schema_errors(item, props[key], root, f'{location}.{key}')
            elif rule.get('additionalProperties') is False:
                errors.append(f'{location}.{key}: unknown field')
            elif isinstance(rule.get('additionalProperties'), dict):
                errors += schema_errors(item, rule['additionalProperties'], root, f'{location}.{key}')
    if kind == 'array':
        if len(value) < rule.get('minItems', 0):
            errors.append(f'{location}: too few items')
        if rule.get('uniqueItems') and len({json.dumps(v, sort_keys=True) for v in value}) != len(value):
            errors.append(f'{location}: duplicate items')
        for index, item in enumerate(value):
            errors += schema_errors(item, rule.get('items', {}), root, f'{location}[{index}]')
    if kind == 'string':
        if len(value.strip()) < rule.get('minLength', 0):
            errors.append(f'{location}: empty string')
        if 'pattern' in rule and not re.search(rule['pattern'], value):
            errors.append(f'{location}: pattern')
    return errors


def safe_file(root, relative, limit):
    """逐段拒绝链接/逃逸，并在读取前限制大小。"""
    if not isinstance(relative, str) or not relative or '\\' in relative or ':' in relative:
        raise ValueError('catalog_path_invalid')
    if relative.startswith('/') or any(p in ('', '.', '..') for p in relative.split('/')):
        raise ValueError('catalog_path_invalid')
    file = Path(root)
    if file.is_symlink():
        raise ValueError('catalog_path_invalid')
    for part in relative.split('/'):
        file = file / part
        if file.is_symlink():
            raise ValueError('catalog_path_invalid')
    if not file.is_file():
        raise ValueError('catalog_path_invalid')
    if file.stat().st_size > limit:
        raise ValueError('catalog_resource_limit')
    return file


def validate(skill, catalog, *, allow_test=False, max_scenes=10000, max_example_bytes=262144):
    """返回结构化错误；安全限制与业务分类数量无关。"""
    errors = []
    def error(code, message):
        errors.append({'code': code, 'message': message})
    if not isinstance(catalog, dict) or catalog.get('schema') != 'jianying-planning-catalog/v2':
        return [{'code': 'unsupported_catalog_schema', 'message': 'expected v2'}]
    if catalog.get('scenes') == []:
        error('catalog_empty', 'scenes must not be empty')
    schema = parse_json(SCHEMA.read_text())
    invalid = schema_errors(catalog, schema, schema)
    # 对象完全重复也是身份冲突，优先保留这个可操作诊断。
    for group in ('scenes', 'recipes', 'sources', 'domains', 'overlays', 'dimensions'):
        values = catalog.get(group, [])
        if isinstance(values, list):
            ids = [v.get('id') for v in values if isinstance(v, dict) and isinstance(v.get('id'), str)]
            if len(set(ids)) != len(ids):
                error('catalog_identity_conflict', group)
    if invalid:
        return errors + [{'code': 'catalog_schema_invalid', 'message': e} for e in invalid]
    if len(catalog['scenes']) > max_scenes:
        error('catalog_resource_limit', f'scenes exceeds {max_scenes}')
        return errors
    sets = {key: {x['id'] for x in catalog[key]} for key in ('recipes', 'sources', 'domains', 'overlays')}
    dimensions = {d['id']: {v['id'] for v in d['values']} for d in catalog['dimensions']}
    for dimension in catalog['dimensions']:
        if len(dimensions[dimension['id']]) != len(dimension['values']):
            error('catalog_identity_conflict', dimension['id'] + '.values')
    identities = set()
    def refs(values, allowed, label):
        if set(values) - allowed:
            error('catalog_reference_invalid', label)
    for scene in catalog['scenes']:
        for identity in [scene['id'], *scene['legacy_ids'], *scene['aliases']]:
            key = identity.lower()
            if key in identities:
                error('catalog_identity_conflict', identity)
            identities.add(key)
        for key, group in [('domain_ids', 'domains'), ('source_ids', 'sources'), ('overlay_ids', 'overlays')]:
            refs(scene[key], sets[group], scene['id'] + '.' + key)
        refs([scene['primary_recipe_id']], sets['recipes'], scene['id'] + '.recipe')
        for key, values in scene['tags'].items():
            refs(values, dimensions.get(key, set()), scene['id'] + '.tags.' + key)
        if scene['status'] == 'test_fixture' and not allow_test:
            error('catalog_test_fixture', scene['id'])
        try:
            safe_file(skill, scene['example_path'], max_example_bytes)
        except ValueError as exc:
            error(str(exc), scene['example_path'])
    for recipe in catalog['recipes']:
        refs(recipe['optional_overlays'], sets['overlays'], recipe['id'] + '.overlays')
        refs(recipe['conflicts'], sets['recipes'], recipe['id'] + '.conflicts')
    aliases = {a for s in catalog['scenes'] for a in s['legacy_ids']}
    refs(catalog['compatibility']['legacy_seed_ids'], aliases, 'legacy_seed_ids')
    published_sources = {source_id for scene in catalog['scenes']
                         if scene['status'] == 'published_knowledge' for source_id in scene['source_ids']}
    for source in catalog['sources']:
        if source['id'] not in published_sources:
            continue
        popularity = source['popularity']
        if source['access_scope'] == 'test_fixture' or not source['adaptation'].strip():
            error('catalog_source_invalid', source['id'] + ': missing method provenance')
        if popularity['status'] == 'measured' and not popularity['metrics']:
            error('catalog_source_invalid', source['id'] + ': measured without metrics')
        if not popularity['observed_on'].strip() or not popularity['scope'].strip():
            error('catalog_source_invalid', source['id'] + ': popularity provenance incomplete')
    for key in catalog['metadata']:
        if '.' not in key:
            error('catalog_schema_invalid', 'metadata keys must be namespaced')
    return errors


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('skill', nargs='?', type=Path, default=SKILL)
    parser.add_argument('--allow-test', action='store_true')
    args = parser.parse_args()
    try:
        file = safe_file(args.skill, 'references/planning-catalog-v2.json', 16 * 1024 * 1024)
        errors = validate(args.skill, parse_json(file.read_text()), allow_test=args.allow_test)
    except (ValueError, OSError) as exc:
        errors = [{'code': str(exc).split(':')[0], 'message': str(exc)}]
    print(json.dumps({'ok': not errors, 'errors': errors}, ensure_ascii=False))
    return bool(errors)


if __name__ == '__main__':
    raise SystemExit(main())
