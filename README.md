# enumsync

enumsync generates a typed enum module from the files in a folder.

It scans a directory and writes a Python module that includes:

- a `StrEnum` with file names as values
- a typed `FileStore[...]` alias for that enum
- a small sync call to keep the generated file updated

## Example

```python
from enumsync import FileStore

FileStore(__file__).sync("expected.py")
```

This creates a generated module like the example in `examples/example1/expected.py`.

## Structure

- `src/enumsync/store.py`: file store and sync entry point
- `src/enumsync/sync.py`: AST-based code generator
- `examples/example1/`: example input and generated output
- `tests/test_sync.py`: tests for generated output and explicit output paths
