# Data module template

A template for modular data workflows using [snakemake](https://snakemake.readthedocs.io/en/stable/), part of the [clio](https://clio.readthedocs.io/) toolset.

## How to use this template

1. Install [copier](https://copier.readthedocs.io/en/stable/) with your favourite package management system (we'll assume [mamba](https://mamba.readthedocs.io/en/latest/) in this example).
2. Use `copier` to copy this repo.
3. Answer some questions so we pre-fill licensing, citiation files, etc...
4. You're all set up!

```bash
mamba install copier
copier copy https://github.com/calliope-project/data-module-template.git ./path/to/destination
```

## Features

- Standardised layout following `clio` guidelines.
- Pre-made integration test setup for your module.
- Pre-made Continuous Integration (CI) settings, ready for [pre-commit.ci](https://pre-commit.ci/).
- Autommated documentation, ready for [Read the Docs](https://about.readthedocs.com/).

## IMPORTANT

A few things to be aware of.

- **Modules do not work like regular snakemake workflows!** The primary way to test them should be external (calling `module:`, passing resources, and requesting results) and not internal (calling the `all:` rule). Check the pre-made `.tests/` for more info.
- Keep `INTERFACE.yaml` up-to-date with your module's required resources (both user provided and automatically downloaded), relevant result files, and user provided wildcards.
- The template includes an example of a modular workflow by default. Feel free to remove this once you understand how it works.

## Example module

```tree
example_module/
├── AUTHORS
├── CITATION.cff
├── environment.yaml
├── INTERFACE.yaml                 # Module interface description
├── LICENSE
├── mkdocs.yaml
├── README.md
├── ruff.toml
├── config/
│   └── example.yaml               # Configuration example
├── docs/
│   ├── index.md
│   └── hooks/
│       └── clio_standard.py       # Standardised documentation
├── resources/
│   ├── automatic/                 # Automatically downloaded files should go here
│   └── user/                      # User inputted files should go here
├── results/                       # All module rule outputs should go here
├── tests/
│   └── integration/               # A lightweight integration test
│       ├── Snakefile
│       └── test_config.yaml
└── workflow/
    ├── Snakefile
    ├── envs/
    │   └── shell.yaml
    ├── internal/
    │   ├── config.schema.yaml
    │   └── settings.yaml
    ├── profiles/
    │   └── default/
    │       └── config.yaml
    ├── rules/
    │   ├── automatic.smk
    │   └── dummy.smk
    └── scripts/
        └── dummy_script.py
```
