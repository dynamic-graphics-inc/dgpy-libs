# CHANGELOG

## 2026-11-13

- `funkify`
  - Retired: removed from the repo and no longer published (existing PyPI
    releases are left in place)
- **BREAKING:** modules are no longer callable (no deprecation period)
  - `aiopen` (v0.9.0): use `from aiopen import aiopen` instead of
    `import aiopen; aiopen(...)`
  - `asyncify` (v0.13.0): use `from asyncify import asyncify` instead of
    `import asyncify; @asyncify`
  - `requires` (v0.13.0): use `from requires import requires` instead of
    `import requires; @requires(...)`
  - `shellfish` (v0.8.0): use `shellfish.do(...)` / `shellfish.sh.do(...)`
    instead of `shellfish(...)` / `shellfish.sh(...)`
- `aiopen`, `asyncify`, `requires`, `shellfish`
  - No longer depend on `funkify`
- `dgpylibs` (v0.2.0)
  - Dropped `funkify` from dependencies and from the version/metadata registry
    (`__funkify_version__` and the `funkify` metadata fields are gone)
- `jsonbourne`
  - jsonbourne is unchanged: `JSON(...)` is still callable (this did not use funkify as a dependency)

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
