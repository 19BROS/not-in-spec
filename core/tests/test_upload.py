import gzip
import io
import json
import logging
import shutil
import tarfile
import tempfile
from collections.abc import Iterator
from pathlib import Path
from typing import Any

import pytest

from notinspec import upload
from notinspec.demo import SCHEMA
from notinspec.upload import ArchiveError, extract_archive, process_upload

EXAMPLES = Path(__file__).parents[1] / "examples" / "cli"
SPHINX_XML = Path(__file__).parent / "fixtures" / "sphinx" / "xml-plain"
RUN_ID = "20261119T1200Z-items-0a1b"
ARTIFACTS = {"comment.md", "ingestion.json", "report.html", "results.json", "run.json"}

Member = tuple[tarfile.TarInfo, bytes | None]


def regular(name: str, data: bytes = b"") -> Member:
    info = tarfile.TarInfo(name)
    info.size = len(data)
    info.mode = 0o644
    return info, data


def special(name: str, kind: bytes, linkname: str = "") -> Member:
    info = tarfile.TarInfo(name)
    info.type = kind
    info.linkname = linkname
    return info, None


def folder(root: Path, prefix: str = "") -> list[Member]:
    """Every file below `root`, named like `notinspec pack` names them."""
    paths = sorted(p for p in root.rglob("*") if p.is_file())
    return [regular(prefix + p.relative_to(root).as_posix(), p.read_bytes()) for p in paths]


def write_archive(path: Path, members: list[Member]) -> Path:
    """The pack format (PR #43): tar.gz, PAX, mtime 0, owner 0, sorted as given."""
    with (
        path.open("wb") as raw,
        gzip.GzipFile(filename="", fileobj=raw, mode="wb", mtime=0) as compressed,
        tarfile.open(fileobj=compressed, mode="w", format=tarfile.PAX_FORMAT) as tar,
    ):
        for info, data in members:
            tar.addfile(info, io.BytesIO(data) if data is not None else None)
    return path


def config(text: str) -> Member:
    return regular("notinspec.yaml", text.encode())


# core/examples/cli without its `project:`, so the default (the config folder) decides
NO_PROJECT = 'docs: {paths: ["docs/**/*.md"], openapi: "openapi.yaml"}\n'
EXAMPLE = [m for m in folder(EXAMPLES) if m[0].name != "notinspec.yaml"]
SPHINX = [config('docs: {sphinx_xml: "build/xml"}\n'), *folder(SPHINX_XML, "build/xml/")]


@pytest.fixture(autouse=True)
def temp(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Iterator[Path]:
    """Temporary folders go below tmp_path, and none may be left after any test."""
    for name in ("GITHUB_REPOSITORY", "NOTINSPEC_COMMIT", "NOTINSPEC_PR"):
        monkeypatch.delenv(name, raising=False)
    temp = tmp_path / "temp"
    temp.mkdir()
    monkeypatch.setattr(tempfile, "tempdir", str(temp))
    yield temp
    assert list(temp.iterdir()) == []


def run(tmp_path: Path, members: list[Member], **kwargs: Any) -> upload.UploadResult:
    archive = write_archive(tmp_path / "inputs.tar.gz", members)
    return process_upload(archive, tmp_path / "runs", kwargs.pop("run_id", RUN_ID), **kwargs)


def ingestion(tmp_path: Path, run_id: str = RUN_ID) -> dict[str, Any]:
    data: dict[str, Any] = json.loads((tmp_path / "runs" / run_id / "ingestion.json").read_bytes())
    return data


def assert_input_error(tmp_path: Path, result: upload.UploadResult) -> str:
    assert (result.status, result.error_kind, result.verdict) == ("error", "input", None)
    assert result.error is not None and result.error in result.comment_md
    # no half-written run, and no server path shown to the repo owner
    assert list((tmp_path / "runs").iterdir()) == []
    assert str(tmp_path) not in result.error and "notinspec-upload-" not in result.error
    return result.error


def test_valid_archive_gives_a_demo_run(tmp_path: Path) -> None:
    url = f"https://example.org/#/runs/{RUN_ID}"
    result = run(tmp_path, [*EXAMPLE, config(NO_PROJECT)], project="items", web_url=url)
    assert result == upload.UploadResult(RUN_ID, "done", None, None, None, result.comment_md)
    out = tmp_path / "runs" / RUN_ID
    assert {p.name for p in out.iterdir()} == ARTIFACTS  # no run.json.tmp, no staging folder

    # what the API's /demo/runs/{id} returns as is
    run_json = json.loads((out / "run.json").read_bytes())
    assert run_json["schema"] == SCHEMA and run_json["id"] == RUN_ID
    assert run_json["project"] == "items"
    assert run_json["counts"]["files"] == 2 and run_json["counts"]["chunks"] > 0
    assert run_json["commit"] == "0" * 40  # no commit given and none from git
    assert [s["status"] for s in run_json["steps"][:4]] == ["done", "done", "skipped", "skipped"]

    counts = json.loads((out / "results.json").read_bytes())["ingestion"]
    assert f"{counts['files']} files, {counts['chunks']} chunks, " in result.comment_md
    assert "no verdict yet" in result.comment_md and upload.NOT_EVALUATED in result.comment_md
    assert f"[Full results]({url})" in result.comment_md
    assert "<!--" not in result.comment_md  # the Action adds its own marker


def test_sphinx_archive(tmp_path: Path) -> None:
    result = run(tmp_path, SPHINX, project="lib")
    assert result.status == "done", result.error
    run_json = json.loads((tmp_path / "runs" / RUN_ID / "run.json").read_bytes())
    assert run_json["docs"]["sphinx_version"].startswith("9.")
    assert run_json["counts"]["symbols"] > 0
    assert "[Full results]" not in result.comment_md


def test_same_archive_twice_same_chunks(tmp_path: Path) -> None:
    # chunk IDs leave the project out (chunking/chunker.py), but breadcrumbs start with it
    members = [*EXAMPLE, config(NO_PROJECT)]
    for run_id in ("first", "second"):
        assert run(tmp_path, members, run_id=run_id, project="items").status == "done"
    first, second = ingestion(tmp_path, "first"), ingestion(tmp_path, "second")
    assert first["project"] == "items"
    assert first["chunks"] == second["chunks"]  # IDs, breadcrumbs, hashes
    assert first["input_hash"] == second["input_hash"]
    assert first["chunks"][0]["breadcrumb"].startswith("items > ")

    # without a project the folder name is fixed too, never the random temp name
    assert run(tmp_path, members, run_id="third").status == "done"
    assert run(tmp_path, members, run_id="fourth").status == "done"
    third, fourth = ingestion(tmp_path, "third"), ingestion(tmp_path, "fourth")
    assert third["project"] == "upload"
    assert third["chunks"] == fourth["chunks"]
    assert [c["id"] for c in third["chunks"]] == [c["id"] for c in first["chunks"]]


def test_config_project_wins_over_the_repo_name(tmp_path: Path) -> None:
    assert run(tmp_path, folder(EXAMPLES), project="items").status == "done"
    assert ingestion(tmp_path)["project"] == "items-api"


@pytest.mark.parametrize(
    ("member", "message"),
    [
        (regular("../../../evil.md", b"x"), "stay inside the archive"),
        (regular("docs/../../../../evil.md", b"x"), "stay inside the archive"),
        (regular("/evil.md", b"x"), "stay inside the archive"),
        (regular("C:/evil.md", b"x"), "stay inside the archive"),
        (regular("docs\\..\\..\\evil.md", b"x"), "stay inside the archive"),
        (special("docs/link.md", tarfile.SYMTYPE, "../../../evil.md"), "is a symbolic link"),
        (special("docs/abs.md", tarfile.SYMTYPE, "/etc/passwd"), "is a symbolic link"),
        (special("docs/hard.md", tarfile.LNKTYPE, "openapi.yaml"), "is a hard link"),
        (special("docs/dev", tarfile.CHRTYPE), "is a device"),
        (special("docs/disk", tarfile.BLKTYPE), "is a device"),
        (special("docs/fifo", tarfile.FIFOTYPE), "is a FIFO"),
        (special("docs/sparse.md", tarfile.GNUTYPE_SPARSE), "is a sparse file"),
    ],
)
def test_unsafe_member_rejected(tmp_path: Path, member: Member, message: str) -> None:
    before = set(tmp_path.rglob("*"))
    result = run(tmp_path, [*folder(EXAMPLES), member])
    assert message in assert_input_error(tmp_path, result)
    # only our own archive and the (empty) runs folder are new: nothing landed outside
    assert set(tmp_path.rglob("*")) - before == {tmp_path / "inputs.tar.gz", tmp_path / "runs"}


@pytest.mark.parametrize(
    "member",
    [
        regular("../../../evil.md", b"x"),
        special("docs/link.md", tarfile.SYMTYPE, "../../../evil.md"),
    ],
)
def test_data_filter_still_stops_what_our_checks_miss(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, member: Member
) -> None:
    monkeypatch.setattr(upload._Members, "add", lambda self, m: True)
    before = set(tmp_path.rglob("*"))
    result = run(tmp_path, [*folder(EXAMPLES), member])
    assert f"{member[0].name}: rejected (" in assert_input_error(tmp_path, result)
    assert set(tmp_path.rglob("*")) - before == {tmp_path / "inputs.tar.gz", tmp_path / "runs"}


@pytest.mark.parametrize(
    ("members", "message"),
    [
        ([regular("a.md"), regular("a.md")], "a.md appears twice"),
        ([regular("a.md"), regular("a.md/b.md")], "a.md is both a file and a folder"),
        ([regular("a/b.md"), regular("a")], "a is both a file and a folder"),
    ],
)
def test_ambiguous_names_rejected(tmp_path: Path, members: list[Member], message: str) -> None:
    result = run(tmp_path, [config(NO_PROJECT), *members])
    assert message in assert_input_error(tmp_path, result)


@pytest.mark.parametrize(
    ("limit", "value", "message"),
    [
        ("MAX_MEMBERS", 4, "more than 4 files and folders"),
        ("MAX_MEMBER_BYTES", 500, "openapi.yaml is larger than 500 bytes unpacked"),
        ("MAX_TOTAL_BYTES", 1200, "all files together are larger than 1200 bytes unpacked"),
        ("_MAX_STREAM_BYTES", 2000, "all files together are larger than 250 MB unpacked"),
    ],
)
def test_limits(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, limit: str, value: int, message: str
) -> None:
    members = [*folder(EXAMPLES), regular("more/a.md", b"# A\n"), regular("more/b.md", b"# B\n")]
    assert run(tmp_path, members, run_id="fits").status == "done"
    shutil.rmtree(tmp_path / "runs" / "fits")
    monkeypatch.setattr(upload, limit, value)
    assert message in assert_input_error(tmp_path, run(tmp_path, members))


def test_a_header_claiming_a_huge_file_is_rejected_before_its_data(tmp_path: Path) -> None:
    # 51 MB announced, nothing behind it: the real limit stops it without reading anything
    info = tarfile.TarInfo("huge.bin")
    info.size = upload.MAX_MEMBER_BYTES + 1
    archive = tmp_path / "inputs.tar.gz"
    archive.write_bytes(gzip.compress(info.tobuf(tarfile.PAX_FORMAT), mtime=0))
    result = process_upload(archive, tmp_path / "runs", RUN_ID)
    assert "huge.bin is larger than 50 MB unpacked" in assert_input_error(tmp_path, result)


@pytest.mark.parametrize("damage", ["not gzip", "plain tar", "truncated", "garbage tar"])
def test_broken_archive(tmp_path: Path, damage: str) -> None:
    archive = write_archive(tmp_path / "inputs.tar.gz", folder(EXAMPLES))
    data = archive.read_bytes()
    if damage == "not gzip":
        data = b"PK\x03\x04 a zip file"
    elif damage == "plain tar":
        data = gzip.decompress(data)
    elif damage == "truncated":
        data = data[: len(data) // 2]
    else:
        data = gzip.compress(b"\x01" * 2048)
    archive.write_bytes(data)
    result = process_upload(archive, tmp_path / "runs", RUN_ID)
    assert "not a valid tar.gz" in assert_input_error(tmp_path, result)


@pytest.mark.parametrize(
    ("members", "message"),
    [
        ([], "no notinspec.yaml at its root"),
        (EXAMPLE, "no notinspec.yaml at its root"),
        ([*EXAMPLE, regular("sub/notinspec.yaml", NO_PROJECT.encode())], "no notinspec.yaml"),
        ([*EXAMPLE, special("notinspec.yaml", tarfile.DIRTYPE)], "no notinspec.yaml"),
    ],
)
def test_config_missing(tmp_path: Path, members: list[Member], message: str) -> None:
    assert message in assert_input_error(tmp_path, run(tmp_path, members))


def test_config_errors_keep_the_config_error_text(tmp_path: Path) -> None:
    unknown = run(tmp_path, [*EXAMPLE, config(NO_PROJECT.replace("}", ", sphinx: x}"))])
    assert assert_input_error(tmp_path, unknown).startswith("docs.sphinx was replaced")
    unknown = run(tmp_path, [*EXAMPLE, config("docs: {paths: [a.md], extra: 1}\n")])
    assert assert_input_error(tmp_path, unknown) == "unknown docs field(s): extra"
    broken = assert_input_error(tmp_path, run(tmp_path, [*EXAMPLE, config("docs: [\n")]))
    # the path in ConfigError is shown relative to the archive root
    assert broken.startswith("cannot read config notinspec.yaml: ")


@pytest.mark.parametrize(
    ("members", "message"),
    [
        (  # ConfigError from ingest: an input the config names is missing
            [config('docs: {openapi: "missing.yaml"}\n')],
            "input is not a file: missing.yaml",
        ),
        (  # SphinxInputError, wrapped into ConfigError by ingest
            [
                *(m for m in SPHINX if m[0].name != "build/xml/build-env.txt"),
                regular("build/xml/build-env.txt", b"sphinx-build 8.2.3\n"),
            ],
            "Sphinx 8.2.3 is not supported",
        ),
        (  # not well-formed XML
            [*SPHINX, regular("build/xml/broken.xml", b"<document><p>")],
            "docs.sphinx_xml build/xml: broken.xml: not well-formed XML",
        ),
        (  # SpecLoadError
            [config('docs: {openapi: "spec.yaml"}\n'), regular("spec.yaml", b"swagger: '2.0'\n")],
            "Swagger 2.0 is not supported",
        ),
        (
            [config('docs: {openapi: "spec.json"}\n'), regular("spec.json", b"{nope")],
            "cannot parse spec.json",
        ),
    ],
)
def test_bad_inputs_found_by_ingest(tmp_path: Path, members: list[Member], message: str) -> None:
    assert message in assert_input_error(tmp_path, run(tmp_path, members))


@pytest.mark.parametrize("step", ["ingest", "build_demo_run"])
def test_unexpected_error_is_internal_and_logged(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture, step: str
) -> None:
    def boom(*args: object, **kwargs: object) -> None:
        raise RuntimeError("secret detail")

    # build_demo_run: after the artifacts are written, so the folder is not empty
    monkeypatch.setattr(upload, step, boom)
    with caplog.at_level(logging.ERROR, logger="notinspec.upload"):
        result = run(tmp_path, folder(EXAMPLES))
    assert (result.status, result.error_kind) == ("error", "internal")
    assert (
        result.error == f"internal error in NOT-IN-SPEC, not caused by your inputs (run {RUN_ID})"
    )
    assert "secret detail" not in result.comment_md
    assert list((tmp_path / "runs").iterdir()) == []
    assert "secret detail" in caplog.text and "Traceback" in caplog.text


def test_git_never_reads_a_repo_from_the_archive(tmp_path: Path) -> None:
    members = [
        *folder(EXAMPLES),
        regular(".git/HEAD", b"ref: refs/heads/main\n"),
        regular(".git/refs/heads/main", b"b" * 40 + b"\n"),
        regular(".git/config", b"[core]\n\trepositoryformatversion = 0\n"),
        regular(".git/objects/.keep"),
    ]
    assert run(tmp_path, members).status == "done"
    run_json = json.loads((tmp_path / "runs" / RUN_ID / "run.json").read_bytes())
    assert run_json["commit"] == "0" * 40

    # the token's commit, when given, is the one used; git is not asked
    shutil.rmtree(tmp_path / "runs" / RUN_ID)
    assert run(tmp_path, members, commit="c" * 40).status == "done"
    run_json = json.loads((tmp_path / "runs" / RUN_ID / "run.json").read_bytes())
    assert run_json["commit"] == "c" * 40


@pytest.mark.parametrize(
    ("kwargs", "error"),
    [
        ({"run_id": "../escape"}, ValueError),
        ({"run_id": ".."}, ValueError),
        ({"run_id": ""}, ValueError),
        ({"project": "a/b"}, ValueError),
        ({"project": ".git"}, ValueError),
        ({"project": ".GIT"}, ValueError),
        ({"commit": "C" * 40}, ValueError),
        ({"commit": "abc"}, ValueError),
    ],
)
def test_caller_mistakes_raise(tmp_path: Path, kwargs: dict[str, str], error: type) -> None:
    with pytest.raises(error):
        run(tmp_path, folder(EXAMPLES), **kwargs)
    assert not (tmp_path / "escape").exists()
    assert not (tmp_path / "runs").exists() or list((tmp_path / "runs").iterdir()) == []


def test_existing_run_folder_is_never_touched(tmp_path: Path) -> None:
    existing = tmp_path / "runs" / RUN_ID
    existing.mkdir(parents=True)
    (existing / "run.json").write_text("{}")
    with pytest.raises(FileExistsError):
        run(tmp_path, folder(EXAMPLES))
    assert (existing / "run.json").read_text() == "{}"


def test_extract_archive_names_and_root_folder(tmp_path: Path) -> None:
    dot = tarfile.TarInfo(".")
    dot.type = tarfile.DIRTYPE
    archive = write_archive(
        tmp_path / "inputs.tar.gz",
        [(dot, None), special("docs", tarfile.DIRTYPE), *folder(EXAMPLES, "./")],
    )
    dest = tmp_path / "dest"
    assert extract_archive(archive, dest) == (
        "docs/guide.md", "notinspec.yaml", "openapi.yaml"
    )  # fmt: skip
    assert (dest / "docs" / "guide.md").read_bytes() == (EXAMPLES / "docs/guide.md").read_bytes()
    with pytest.raises(ValueError, match="not empty"):
        extract_archive(archive, dest)
    assert issubclass(ArchiveError, ValueError)
