"""Test a simplified template use-case."""

import subprocess
from copy import deepcopy

import pytest
from copier import run_copy


@pytest.fixture(scope="module", params=["MIT"])
def simple_template(request, tmp_path_factory, template_path, simple_answers):
    """Run the template in a temporary location, for further testing."""
    path = tmp_path_factory.mktemp(request.param)
    modified_answers = deepcopy(simple_answers)
    modified_answers.update(license=request.param)
    run_copy(src_path=str(template_path), dst_path=str(path), data=modified_answers)
    return path / modified_answers["module_short_name"]


@pytest.fixture(scope="module")
def pixi_built(simple_template):
    """Create a pixi environment for the temporary template project."""
    pixi_config = simple_template / "pixi.toml"
    subprocess.run(
        f"pixi install --manifest-path {pixi_config}",
        shell=True,
        cwd=simple_template,
        check=True,
    )
    return simple_template

@pytest.fixture(scope="module")
def snakemake_built(pixi_built):
    """Create snakemake environments in the temporary template project."""
    subprocess.run(
        "pixi run snakemake --conda-create-envs-only",
        shell=True,
        cwd=pixi_built,
        check=True
    )
    return pixi_built


def test_template_license(simple_template):
    """Generated license files should match the copier request."""
    assert (simple_template / "LICENSE").exists()


def test_citation_file(pixi_built):
    """The generated citation file should be valid."""
    citation_file = pixi_built / "CITATION.cff"
    assert subprocess.run(
        f"pixi run cffconvert -i {citation_file.name} --validate",
        shell=True,
        check=True,
        cwd=pixi_built,
    )


def test_mkdocs_build(pixi_built):
    """Mkdocs should build without issues."""
    assert subprocess.run("pixi run mkdocs build", shell=True, check=True, cwd=pixi_built)


def test_snakemake_all_failure(snakemake_built):
    """The 'all' rule should return an error by default."""
    process = subprocess.run("pixi run snakemake", shell=True, cwd=snakemake_built, capture_output=True)
    assert "This workflow must be called as a snakemake module" in str(process.stderr)


def test_snakemake_integration_testing(snakemake_built):
    """The automatic integration test should run by default."""
    assert subprocess.run("pixi run snakemake --use-conda",
        check=True,
        cwd=snakemake_built / "tests/integration",
    )
