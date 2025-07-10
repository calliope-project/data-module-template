"""Test a simplified template use-case."""

import subprocess
from copy import deepcopy

import pytest
from copier import run_copy


@pytest.fixture(scope="module", params=["Apache-2.0"])
def template_project(request, tmp_path_factory, template_path, simple_answers):
    """Run the template in a temporary location, for further testing."""
    path = tmp_path_factory.mktemp(request.param)
    modified_answers = deepcopy(simple_answers)
    modified_answers.update(license=request.param)
    run_copy(
        src_path=str(template_path),
        dst_path=str(path),
        data=modified_answers,
        vcs_ref="HEAD",  # Use the latest version for the test
    )
    return path


@pytest.fixture(scope="module")
def pixi_built(template_project):
    """Create a pixi environment for the temporary template project."""
    pixi_config = template_project / "pixi.toml"
    subprocess.run(
        f"pixi install --manifest-path {pixi_config}",
        shell=True,
        cwd=template_project,
        check=True,
    )
    return template_project


def test_mkdocs_build(pixi_built):
    """The template's mkdocs should build without issues."""
    assert subprocess.run("pixi run build-docs", shell=True, check=True, cwd=pixi_built)


def test_pytest(pixi_built):
    """The template's tests should pass by default."""
    assert subprocess.run(
        "pixi run test-integration", shell=True, check=True, cwd=pixi_built
    )


def test_linting(pixi_built):
    """The generated project should result in perfect snakemake linting."""
    assert subprocess.run(
        "pixi run snakemake --lint", shell=True, check=True, cwd=pixi_built
    )
