#!/usr/bin/env python3
"""校验视频质量档案。此工具只验证知识，不授予运行或审批权限。"""
import argparse
import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills/jianying-video-planning'
CATALOG_FILE = SKILL / 'references/quality-profiles-v1.json'
SCHEMA_FILE = SKILL / 'references/quality-profiles-v1.schema.json'

ALLOWED_ACTIONS = {
    'trim', 'reorder', 'replace_clip', 'adjust_volume', 'caption_edit',
    'crop', 'scale', 'color_adjust', 'music_edit',
}
FORBIDDEN_FIELDS = {
    'command', 'commands', 'script', 'handler', 'executable', 'argv', 'arguments',
    'approved', 'approval', 'capability_status', 'model_provider', 'timecode', 'timecodes',
}
CATALOG_FIELDS = {'schema', 'profiles', 'metadata'}
PROFILE_FIELDS = {
    'schema', 'profile_id', 'version', 'dimensions', 'allowed_actions',
    'human_boundaries', 'metadata',
}
DIMENSION_FIELDS = {
    'dimension_id', 'label', 'weight', 'threshold', 'hard_gate', 'evidence_types',
}


def parse_json(text):
    """解析 JSON，并拒绝重复键及非标准数值。"""
    def pairs(values):
        result = {}
        for key, value in values:
            if key in result:
                raise ValueError(f'profile_duplicate_key: {key}')
            result[key] = value
        return result

    def constant(value):
        raise ValueError(f'profile_schema_invalid: {value}')

    return json.loads(text, object_pairs_hook=pairs, parse_constant=constant)


def canonical_digest(value):
    """返回跨平台稳定的规范 JSON SHA-256。"""
    payload = json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False,
    ).encode('utf-8')
    return hashlib.sha256(payload).hexdigest()


def _non_empty_strings(value):
    return (isinstance(value, list) and value and
            all(isinstance(item, str) and item.strip() for item in value) and
            len(value) == len(set(value)))


def _forbidden_paths(value, location='$'):
    paths = []
    if isinstance(value, dict):
        for key, item in value.items():
            path = f'{location}.{key}'
            if key.lower() in FORBIDDEN_FIELDS:
                paths.append(path)
            paths.extend(_forbidden_paths(item, path))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            paths.extend(_forbidden_paths(item, f'{location}[{index}]'))
    return paths


def validate(skill, catalog):
    """返回结构化错误，不把知识档案解释为运行证据。"""
    errors = []

    def error(code, message):
        errors.append({'code': code, 'message': message})

    if not isinstance(catalog, dict) or catalog.get('schema') != 'jianying-quality-profile-catalog/v1':
        return [{'code': 'unsupported_profile_schema', 'message': 'expected quality profile catalog v1'}]
    if set(catalog) != CATALOG_FIELDS:
        error('profile_schema_invalid', 'catalog fields must be exact')
    if not isinstance(catalog.get('profiles'), list) or not catalog['profiles']:
        error('profile_schema_invalid', 'profiles must be a non-empty array')
        return errors
    if not isinstance(catalog.get('metadata'), dict):
        error('profile_schema_invalid', 'catalog metadata must be an object')

    try:
        schema = parse_json((skill / 'references/quality-profiles-v1.schema.json').read_text())
    except (OSError, ValueError) as exc:
        error('profile_schema_invalid', f'schema unavailable: {exc}')
        return errors
    if schema.get('$id') != 'jianying-quality-profile-catalog/v1':
        error('profile_schema_invalid', 'schema identity mismatch')

    forbidden = _forbidden_paths(catalog)
    if forbidden:
        error('profile_execution_field', ', '.join(forbidden))

    try:
        workflows = parse_json((skill / 'references/representative-workflows-v1.json').read_text())
        sources = parse_json((skill / 'references/source-index.json').read_text())
        workflow_ids = {item['id'] for item in workflows['workflows']}
        source_ids = {item['id'] for item in sources['sources']}
    except (OSError, ValueError, KeyError, TypeError) as exc:
        error('profile_reference_invalid', f'reference index unavailable: {exc}')
        return errors

    profile_ids = []
    for index, profile in enumerate(catalog['profiles']):
        location = f'profiles[{index}]'
        if not isinstance(profile, dict):
            error('profile_schema_invalid', f'{location} must be an object')
            continue
        if set(profile) != PROFILE_FIELDS:
            error('profile_schema_invalid', f'{location} fields must be exact')
            continue
        if profile['schema'] != 'jianying-quality-profile/v1':
            error('profile_schema_invalid', f'{location}.schema')
        profile_id = profile['profile_id']
        if not isinstance(profile_id, str) or not profile_id.strip():
            error('profile_schema_invalid', f'{location}.profile_id')
        else:
            profile_ids.append(profile_id)
        if not isinstance(profile['version'], str) or not re.fullmatch(r'\d+\.\d+\.\d+', profile['version']):
            error('profile_schema_invalid', f'{location}.version')
        if not isinstance(profile['metadata'], dict):
            error('profile_schema_invalid', f'{location}.metadata')
            continue
        if any('.' not in key for key in profile['metadata']):
            error('profile_schema_invalid', f'{location}.metadata keys must be namespaced')

        referenced_workflows = profile['metadata'].get('partme.workflow_ids')
        referenced_sources = profile['metadata'].get('partme.source_ids')
        if not _non_empty_strings(referenced_workflows) or set(referenced_workflows) - workflow_ids:
            error('profile_reference_invalid', f'{location}.metadata.partme.workflow_ids')
        if not _non_empty_strings(referenced_sources) or set(referenced_sources) - source_ids:
            error('profile_reference_invalid', f'{location}.metadata.partme.source_ids')

        actions = profile['allowed_actions']
        if not isinstance(actions, list) or len(actions) != len(set(actions)):
            error('profile_schema_invalid', f'{location}.allowed_actions')
        elif set(actions) - ALLOWED_ACTIONS:
            error('profile_action_invalid', f'{location}: {sorted(set(actions) - ALLOWED_ACTIONS)}')
        if not _non_empty_strings(profile['human_boundaries']):
            error('profile_schema_invalid', f'{location}.human_boundaries')

        dimensions = profile['dimensions']
        if not isinstance(dimensions, list) or not dimensions:
            error('profile_schema_invalid', f'{location}.dimensions')
            continue
        dimension_ids = []
        for dimension_index, dimension in enumerate(dimensions):
            dim_location = f'{location}.dimensions[{dimension_index}]'
            if not isinstance(dimension, dict) or set(dimension) != DIMENSION_FIELDS:
                error('profile_schema_invalid', f'{dim_location} fields must be exact')
                continue
            dimension_id = dimension['dimension_id']
            if not isinstance(dimension_id, str) or not dimension_id.strip():
                error('profile_schema_invalid', f'{dim_location}.dimension_id')
            else:
                dimension_ids.append(dimension_id)
            if not isinstance(dimension['label'], str) or not dimension['label'].strip():
                error('profile_schema_invalid', f'{dim_location}.label')
            for key in ('weight', 'threshold'):
                value = dimension[key]
                if isinstance(value, bool) or not isinstance(value, (int, float)) or not 0 <= value <= 10:
                    error('profile_schema_invalid', f'{dim_location}.{key}')
            if not isinstance(dimension['hard_gate'], bool):
                error('profile_schema_invalid', f'{dim_location}.hard_gate')
            if not _non_empty_strings(dimension['evidence_types']):
                error('profile_schema_invalid', f'{dim_location}.evidence_types')
        if len(dimension_ids) != len(set(dimension_ids)):
            error('profile_identity_conflict', f'{location}.dimensions')

    if len(profile_ids) != len(set(profile_ids)):
        error('profile_identity_conflict', 'duplicate profile_id')
    if isinstance(catalog.get('metadata'), dict) and any('.' not in key for key in catalog['metadata']):
        error('profile_schema_invalid', 'catalog metadata keys must be namespaced')
    return errors


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('skill', nargs='?', type=Path, default=SKILL)
    args = parser.parse_args()
    try:
        catalog = parse_json((args.skill / 'references/quality-profiles-v1.json').read_text())
        errors = validate(args.skill, catalog)
        digest = None if errors else canonical_digest(catalog)
    except (OSError, ValueError) as exc:
        errors = [{'code': str(exc).split(':')[0], 'message': str(exc)}]
        digest = None
    print(json.dumps({'ok': not errors, 'digest': digest, 'errors': errors}, ensure_ascii=False))
    return bool(errors)


if __name__ == '__main__':
    raise SystemExit(main())
