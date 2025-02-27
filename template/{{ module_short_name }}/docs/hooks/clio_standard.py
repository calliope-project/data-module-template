"""Generate documentation for all the existing modules."""

import subprocess
from pathlib import Path

MODULE_PATH = Path("./")
DOCS_FILE_PATH = MODULE_PATH / "docs" / "how_to_use.md"

TEMPLATE = """
# How to use
This specification is based on `clio` standards.
For more information, please consult the [`clio` documentation](https://clio.readthedocs.io/).

???+ info "Visual summary"

    TODO: create mermaid graph

??? info "`snakemake` execution steps"

    TODO: run rulegraph


## Configuration

We recommend to start with the following configuration.
All configuration options can be found in the module's schema.

???+ example "Example configuration"

    ```yaml
    --8<-- "{example_config}"
    ```

??? info "Configuration schema"

    ```yaml
    --8<-- "{schema}"
    ```

## Attribution

!!! quote "Citation"

    {citation}

??? info "Contributors"

    --8<-- "{authors}"

??? info "License"

    --8<-- "{license}"

"""


def on_pre_build(config):
    """Generate standard documentation page per module.

    Automatically called by mkdocs if the hook is configured.
    """
    create_module_docfile()


def on_post_build(config):
    """Remove automatically generated files."""
    DOCS_FILE_PATH.unlink()


def create_module_docfile():
    """Save a fully documented page for the requested module."""
    authors = MODULE_PATH / "AUTHORS"
    example_config = MODULE_PATH / "config/example.yaml"
    schema = MODULE_PATH / "workflow/internal/config.schema.yaml"
    citation = MODULE_PATH / "CITATION.cff"
    license = MODULE_PATH / "LICENSE"
    assert all(
        [file.exists() for file in [authors, example_config, schema, citation, license]]
    )

    text = TEMPLATE.format(
        example_config=example_config,
        schema=schema,
        citation=get_apa_citation(citation),
        authors=authors,
        license=license,
    )

    with open(DOCS_FILE_PATH, "w") as file:
        file.write(text)


def create_module_rulegraph(name, prefix: Path, module_dir: Path) -> Path:
    """Run snakemake rulegraph commands and save a .png in the requested location."""
    tmp_rulegraph = prefix / f"{name}.png"
    command = f"snakemake --rulegraph | dot -Tpng > {str(tmp_rulegraph.resolve())}"
    subprocess.run(command, shell=True, check=True, cwd=str(module_dir.resolve()))

    return tmp_rulegraph


def get_apa_citation(citation_file: Path) -> str:
    """Return APA citation if the .cff file is correct."""
    subprocess.run(
        f"cffconvert -i {citation_file.name} --validate",
        shell=True,
        check=True,
        cwd=citation_file.parent,
    )
    citation = subprocess.run(
        f"cffconvert -i {citation_file.name} -f apalike",
        shell=True,
        check=True,
        cwd=citation_file.parent,
        capture_output=True,
    )
    return citation.stdout.decode()
