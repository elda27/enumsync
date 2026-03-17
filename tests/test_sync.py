from pathlib import Path

from enumsync.store import FileStore
from enumsync.sync import generate_sync_code

ROOT = Path(__file__).resolve().parents[1]


def test_generate_sync_code_matches_example_fixture() -> None:
    expected_path = ROOT / "examples" / "example1" / "expected.py"
    expected = expected_path.read_text(encoding="utf-8")

    assert generate_sync_code(FileStore(expected_path)) == expected


def test_file_store_can_write_to_explicit_output(tmp_path: Path) -> None:
    bootstrap_path = tmp_path / "__init__.py"
    bootstrap_path.write_text(
        'from enumsync import FileStore\n\nFileStore(__file__).sync("expected.py")\n',
        encoding="utf-8",
    )
    (tmp_path / "README.md").write_text("", encoding="utf-8")

    original_bootstrap = bootstrap_path.read_text(encoding="utf-8")
    FileStore(bootstrap_path).sync("expected.py")

    generated_path = tmp_path / "expected.py"
    generated = generated_path.read_text(encoding="utf-8")

    assert generated_path.exists()
    assert bootstrap_path.read_text(encoding="utf-8") == original_bootstrap
    assert "ExpectedPy = 'expected.py'" in generated
    assert "ReadmeMd = 'README.md'" in generated
    assert "__init__.py" not in generated
