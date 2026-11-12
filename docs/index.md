---
title: dgpy-libs
description: Dynamic Graphics Python libraries
hide:
  - navigation
  - toc
---

<div class="dgpy-hero" markdown>

![dgpy-libs](images/dgpy_logo.svg){ .dgpy-hero__logo }

# dgpy-libs

Python libraries from [Dynamic Graphics Inc](https://dgi.com/): async file IO,
callable modules, secret-agent JSON, shell & filesystem tools and more. Typed,
`async`-friendly and published on PyPI.

```bash
uv add aiopen asyncify fmts funkify h5 jsonbourne lager listless requires shellfish xtyping
```

</div>

## Libraries

| Library | What it does | Install | API |
| ------- | ------------ | ------- | --- |
| [aiopen](libs/aiopen/index.md) | Async file IO | `uv add aiopen` | [reference](reference/aiopen/index.md) |
| [asyncify](libs/asyncify/index.md) | Sync → async: run blocking code from async land | `uv add asyncify` | [reference](reference/asyncify/index.md) |
| [fmts](libs/fmts/index.md) | String transformation utilities | `uv add fmts` | [reference](reference/fmts/index.md) |
| [funkify](libs/funkify/index.md) | Make modules callable | `uv add funkify` | [reference](reference/funkify/index.md) |
| [h5](libs/h5/index.md) | h5py utilities & CLI | `uv add h5` | [reference](reference/h5/index.md) |
| [jsonbourne](libs/jsonbourne/index.md) | EZPZ JSON — secret-agent JSON objects | `uv add jsonbourne` | [reference](reference/jsonbourne/index.md) |
| [lager](libs/lager/index.md) | EZ-PZ logging built on loguru | `uv add lager` | [reference](reference/lager/index.md) |
| [listless](libs/listless/index.md) | Generator & iterable utilities | `uv add listless` | [reference](reference/listless/index.md) |
| [requires](libs/requires/index.md) | Runtime imports & dependency utilities | `uv add requires` | [reference](reference/requires/index.md) |
| [shellfish](libs/shellfish/index.md) | Shell & filesystem utilities | `uv add shellfish` | [reference](reference/shellfish/index.md) |
| [xtyping](libs/xtyping/index.md) | `typing` + `typing_extensions` | `uv add xtyping` | [reference](reference/xtyping/index.md) |
| [dgpytest](libs/dgpytest/index.md) | pytest plugin & fixtures | `uv add dgpytest` | [reference](reference/dgpytest/index.md) |

Want them all? `uv add dgpylibs` installs the lot.
