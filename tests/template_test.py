"""Test a simplified template use-case."""

import subprocess
from copy import deepcopy
from pathlib import Path

import pytest
import snakemake
from copier import run_copy


def run_copier(template_path: Path, test_path: Path, answers: dict):
    """Run a copier instance of the template."""
    run_copy(src_path=str(template_path), dst_path=str(test_path), data=answers)


@pytest.fixture(scope="module", params=["MIT", "Apache-2.0"])
def simple_template(request, tmp_path_factory, template_path, simple_answers):
    """A simple template for each license case."""
    path = tmp_path_factory.mktemp(request.param)
    modified_answers = deepcopy(simple_answers)
    modified_answers.update(license=request.param)
    run_copier(template_path, path, modified_answers)
    return path / modified_answers["module_short_name"]


def test_template_license(simple_template):
    """Generated license files should match the copier request."""
    assert (simple_template / "LICENSE").exists()


def test_citation_file(simple_template):
    """The generated citation file should be valid."""
    citation_file = simple_template / "CITATION.cff"
    assert subprocess.run(
        f"cffconvert -i {citation_file.name} --validate",
        shell=True,
        check=True,
        cwd=simple_template,
    )


def test_mkdocs_build(simple_template):
    """Mkdocs should build without issues."""
    assert subprocess.run("mkdocs build", shell=True, check=True, cwd=simple_template)


def test_snakemake_all_failure(simple_template):
    """The 'all' rule should return an error by default."""
    # snake_path = simple_template
    pipe = subprocess.Popen(["snakemake"], cwd=simple_template, stderr=subprocess.PIPE)
    _, error = pipe.communicate()
    assert "This workflow must be called as a snakemake module" in str(error)


