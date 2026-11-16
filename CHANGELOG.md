# CHANGELOG

## 2026-11-16

- Docs
  - Built with [Zensical](https://zensical.org) instead of MkDocs 1.x +
    Material (MkDocs 1.x is unmaintained; MkDocs 2.0 drops plugins/Material)
  - Lib README pages include `libs/<lib>/README.md` directly (snippets) instead
    of rendering a copied `README.ipynb` (mkdocs-jupyter is not supported);
    `fmts`, `listless` and `shellfish` README pages added
  - Removed the stale `libs/*/README.ipynb` files; `README.md` is the source of
    truth (it is also the PyPI description)
  - `docs/notebooks/*.ipynb` are served as committed `.md` conversions
  - Docs home page includes the root `README.md` instead of a hand-kept copy
  - Python 3.11+ stated in README/docs (was 3.9+)
  - Dropped dead `python_version<'3.10'` docs dependencies
  - nox sessions renamed: `mkdocs` -> `docs`, `mkdocs_serve` -> `docs_serve`
  - CI deploys to `gh-pages` via `peaceiris/actions-gh-pages`

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


- type-checking
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
