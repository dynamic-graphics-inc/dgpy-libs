# CHANGELOG

## 2026-11-13

- ALL
  - Enable `ty` typechecking
  - Remove `pyright` typechecking
  - Replace `pre-commit` with [`prek`](https://prek.j178.dev)
    (`.pre-commit-config.yaml` -> `prek.toml`; uses prek builtin hooks)
- `jsonbourne`
  - **BREAKING:** iterating a `JsonBaseModel` yields keys, not `(key, value)`
    tuples (use `.items()`)
  - **BREAKING:** `JsonObj.get`/`pop` `default` is positional-only (like `dict`)
  - fixed `JsonObj.get`/`pop`/`setdefault` ignoring falsy or missing defaults
  - fixed `JsonArr.map`/`filter` arg counting for methods, callables, and
    builtins
  - fixed `JsonArr *=` being a no-op
- `aiopen`
  - fixed `AiopenContextManager.gi_*` raising `AttributeError`
- `shellfish`
  - `file_lines_gen` and `shebang` read files as UTF-8 (was locale default)

---

## 2026-11-05

- ALL
  - pytest warnings are errors everywhere
  - set `asyncio_default_fixture_loop_scope`
  - `license = "MIT"` instead of license classifiers
  - `inspect.iscoroutinefunction` instead of `asyncio.iscoroutinefunction`
    (deprecated in python3.14)
- `aiopen`
  - `detach()` returns the detached buffer (was returning `None`)
- `asyncify`
  - `aiorun*` closes the coroutine before raising on extra args
- `shellfish`
  - `run_async` terminates the process and closes its pipes on timeout

---

## 2026-06-12

- ruff `RET` rules turned on

---

## 2026-06-12

- updated `__about__.py` files to slice
- fixed codeql unclosed file warnings

---

## 2026-04-15

- `h5`
  - add support for bool-json-serialization in `h5 tree` command

---

## 2025-10-15

- ALL
  - python3.14 & patch version

---

## 2025-09-17

- ALL
  - Adopted ruffs `FBT` rules
  - Minor-version bump all packages
  - Bump min python version to 3.11
  - Ruff lints updated for python-v3.11
  - CICD updates for min python version 3.11
  - Remove `_meta.py` files
- `shellfish`
  - Remove old python blocks (pre python3.11)

---

## 2025-07-22

- h5
  - Migrate types (`Dict` -> `dict`, `List` -> `list`, `Tuple` -> `tuple`, `Set`
    -> `set`, etc...)
