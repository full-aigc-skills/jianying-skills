# Third-Party Notices

This skill package is Apache-2.0. It contains instructions, examples, and validation tooling; it
does not bundle third-party editing engines, application binaries, model weights, or proprietary
JianYing resources.

## Permitted interoperability sources

- [GuanYixuan/pyJianYingDraft](https://github.com/GuanYixuan/pyJianYingDraft), Apache-2.0.
  Its public draft behavior is a differential-parity reference for the independently implemented
  Rust runtime. Apache attribution and notice obligations remain applicable; rewriting in Rust
  does not erase them.
- [renezander030/capcut-cli](https://github.com/renezander030/capcut-cli), MIT.
  Its public command behavior and documentation are parity references. Required copyright and
  license notices must remain with any copied MIT material.
- [luoluoluo22/jianying-editor-skill](https://github.com/luoluoluo22/jianying-editor-skill),
  MIT, fixed at commit `32c56928ded4f9e2c2b80e099dc7abb793d2c30b` for assisted-production
  workflow research. This package independently rewrites workflow knowledge only; it does not
  bundle that project's Python runtime, vendored pyJianYingDraft, UI automation, cloud-download
  scripts, databases, cached media, or effect assets. The detailed boundary is recorded in
  [ASSISTED_PRODUCTION_PROVENANCE.md](docs/ASSISTED_PRODUCTION_PROVENANCE.md).

The current skills call only `jianying-cli` or a plugin Runtime Adapter. Neither upstream is a
runtime dependency of an installed skill.

## Excluded non-commercial source

- `mcncarl/jianying-headless`, related forks, tests, fixtures, blueprints, resources, implementation
  constants, and other non-commercially licensed implementation material are not migration inputs
  and are not runtime dependencies.
- The Rust project may independently implement comparable observable capabilities from clean
  requirements and locally generated test material. A language rewrite does not remove upstream
  license obligations, so provenance gates must remain active.

## Interoperability and trademarks

JianYing, 剪映, CapCut, and related bundle identifiers are names of interoperability targets and
remain trademarks of their respective owners. Local application installation, account access,
membership resources, cloud speech usage, and model checkpoints retain their own authorization
and license conditions.
