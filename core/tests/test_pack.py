import shutil
import tarfile
from pathlib import Path

import pytest

from notinspec.cli import main
from notinspec.config import ConfigError
from notinspec.pack import pack_inputs

EXAMPLES = Path(__file__).parents[1] / "examples" / "cli"
SPHINX_XML = Path(__file__).parent / "fixtures" / "sphinx" / "xml-plain"


def members(archive: Path) -> dict[str, tarfile.TarInfo]:
    with tarfile.open(archive) as tar:
        return {m.name: m for m in tar.getmembers()}


def test_same_inputs_same_bytes_from_another_folder(tmp_path: Path) -> None:
    copy = tmp_path / "copy"
    shutil.copytree(EXAMPLES, copy)
    (tmp_path / "out").mkdir()
    first, second = tmp_path / "out" / "a.tar.gz", tmp_path / "out" / "b.tar.gz"
    names = pack_inputs(EXAMPLES / "notinspec.yaml", first)
    pack_inputs(copy / "notinspec.yaml", second)
    assert names == ("docs/guide.md", "notinspec.yaml", "openapi.yaml")
    assert first.read_bytes() == second.read_bytes()
    info = members(first)
    assert list(info) == list(names)
    assert all(m.isfile() and m.mtime == 0 and m.uid == 0 for m in info.values())


def test_sphinx_folder_only_reader_files_and_config_renamed(tmp_path: Path) -> None:
    root, out = tmp_path / "repo", tmp_path / "out" / "inputs.tar.gz"
    out.parent.mkdir()
    shutil.copytree(SPHINX_XML, root / "build" / "xml")
    (root / "build" / "xml" / "objects.inv").write_bytes(b"not read")
    (root / "ci").mkdir()
    (root / "ci" / "docs.yaml").write_text('docs: {sphinx_xml: "../build/xml/"}\n')
    # the config's folder is the archive root, so it must contain its inputs
    with pytest.raises(ConfigError, match="inside the config directory"):
        pack_inputs(root / "ci" / "docs.yaml", out)

    (root / "docs.yaml").write_text('docs: {sphinx_xml: "build/xml/"}\n')
    assert main(["pack", "--config", str(root / "docs.yaml"), "--out", str(out)]) == 0
    assert set(members(out)) == {
        "notinspec.yaml",
        *(f"build/xml/{p.name}" for p in SPHINX_XML.iterdir()),
    }


def test_defaults_in_the_project_folder_twice(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    shutil.copytree(EXAMPLES, tmp_path, dirs_exist_ok=True)
    monkeypatch.chdir(tmp_path)
    assert main(["pack"]) == 0
    first = (tmp_path / "inputs.tar.gz").read_bytes()
    # the second run finds the first archive in the config folder and replaces it
    assert main(["pack"]) == 0
    assert (tmp_path / "inputs.tar.gz").read_bytes() == first
    assert "inputs.tar.gz" not in members(tmp_path / "inputs.tar.gz")


def test_link_out_of_the_config_folder_is_rejected(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    shutil.copytree(SPHINX_XML, root / "build" / "xml")
    (tmp_path / "secret.xml").write_text("<secret/>")
    try:
        (root / "build" / "xml" / "leak.xml").symlink_to(tmp_path / "secret.xml")
    except OSError:
        pytest.skip("no symlink permission (Windows without developer mode)")
    (root / "notinspec.yaml").write_text('docs: {sphinx_xml: "build/xml/"}\n')
    with pytest.raises(ConfigError, match="inside the config directory"):
        pack_inputs(root / "notinspec.yaml", tmp_path / "inputs.tar.gz")


def test_config_error_exits_2(tmp_path: Path) -> None:
    (tmp_path / "notinspec.yaml").write_text('docs: {paths: ["missing/*.md"]}\n')
    out = tmp_path / "out" / "inputs.tar.gz"
    out.parent.mkdir()
    assert main(["pack", "--config", str(tmp_path / "notinspec.yaml"), "--out", str(out)]) == 2
