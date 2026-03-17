from pathlib import Path
from typing import TYPE_CHECKING, Generic, Iterable, TypeVar

try:
    from jinja2 import Template

    ENABLE_JINJA2 = True
except ImportError:

    class Template:
        pass

    ENABLE_JINJA2 = False
if TYPE_CHECKING:
    from enum import StrEnum

TEnum = TypeVar("TEnum", bound="StrEnum")


class FileStore(Generic[TEnum]):
    def __init__(self, path: str):
        """Store object in file

        Args:
            path (str): Set `__file__` or its parent directory. Path to the file where the object will be stored

        Example:
            There is automatic syncing enum by the store in the file.
            ```python
            from enumsync import FileStore

            store = FileStore(__file__)
            ```
        """
        _path = Path(path)
        if _path.is_dir():
            folder = _path
            file = _path / "__init__.py"
        else:
            folder = _path.parent
            file = Path(path)
        self.file = file
        self.folder = folder

    def sync(self, output: str | Path | None = None) -> None:
        """Generate a typed module that mirrors the files in the store folder.

        Args:
            output: Optional path for the generated module. Relative paths are
                resolved from the store folder.
        """
        from enumsync.sync import generate_sync_code

        code = generate_sync_code(self)
        if output is None:
            output_path = self.file
        else:
            output_path = Path(output)
            if not output_path.is_absolute():
                output_path = self.folder / output_path

        output_path.write_text(code, encoding="utf-8")

    def get_text(self, value: TEnum) -> str:
        """Get the file path

        Returns:
            str: The file path where the object is stored
        """
        return (self.folder / str(value)).read_text()

    def get_template(self, value: TEnum) -> "Template":
        """Get the template file path

        Returns:
            Template: The template file path where the object is stored
        """
        if not ENABLE_JINJA2:
            raise ImportError(
                "Jinja2 is not installed. Please install it to use this feature."
            )

        from jinja2 import Environment, FileSystemLoader, select_autoescape

        env = Environment(
            loader=FileSystemLoader(self.folder), autoescape=select_autoescape()
        )
        return env.get_template(str(value))

    def glob(self, pattern: str) -> Iterable[Path]:
        """Glob the file path

        Args:
            pattern (str): The glob pattern to match files

        Returns:
            Iterable[Path]: An iterable of file paths that match the glob pattern
        """
        return self.folder.glob(pattern)
