# docs/images

Logos and banners for the dgpy-libs READMEs and the docs site.
File names are `kebab-case`.

| file                        | used by                                                         |
| --------------------------- | --------------------------------------------------------------- |
| `dgpy-banner.svg`           | README banner (adapts to light/dark, see below)                 |
| `dgpy-white-edge-small.svg` | docs site header logo (`theme.logo` in `zensical.toml`)         |
| `favicon.png`               | docs site favicon (`theme.favicon` in `zensical.toml`)          |
| `favicon.ico`               | multi-size favicon (16/32/48/256)                               |
| `dgpy-logo.svg`, `dgpy-all-white.svg`, `dgpy-white-edge.svg`, `dgpy-white-edge-small.png`, `logo.svg` | logo variants (unused in-repo) |

## Legacy file -- do not delete

`dgpy_banner.svg` (snake_case) is a **copy** of `dgpy-banner.svg`.

READMEs already published to PyPI (every lib released before the
kebab-case rename) load the banner from
`https://github.com/dynamic-graphics-inc/dgpy-libs/blob/main/docs/images/dgpy_banner.svg?raw=true`.
PyPI never re-renders an old release's README, so deleting or renaming this
file breaks the banner on those pages.

When you change `dgpy-banner.svg`, copy it over `dgpy_banner.svg` too:

```sh
cp docs/images/dgpy-banner.svg docs/images/dgpy_banner.svg
```

## How the banner handles light/dark

`dgpy-banner.svg` is one file used as a plain `<img>` everywhere (GitHub,
PyPI, the docs site). Its lettering styles itself:

```css
.t{fill:#000;stroke:#fff;stroke-width:5px;stroke-linejoin:round;paint-order:stroke}
@media (prefers-color-scheme: dark){.t{fill:#fff;stroke:#000}}
```

- The `prefers-color-scheme` query inside an SVG `<img>` follows the
  embedding page's `color-scheme` when the page declares one, otherwise the
  OS. GitHub and Zensical both declare it from their theme toggle, so the
  lettering is black on light pages and white on dark ones.
- PyPI declares nothing, so there it follows the OS. A dark-mode OS gets
  white lettering on PyPI's white page; the opposite-colour outline
  (`stroke` + `paint-order: stroke`) keeps it readable. Everywhere else the
  outline matches the background and is invisible.

No `<picture>`, no second file, no JS.
