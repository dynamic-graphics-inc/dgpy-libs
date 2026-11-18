# docs/images

Logos and banners for the dgpy-libs READMEs and the docs site.
File names are `kebab-case`.

| file                        | used by                                                         |
| --------------------------- | --------------------------------------------------------------- |
| `dgpy-banner.svg`           | README banner, light backgrounds (black lettering)              |
| `dgpy-banner-dark.svg`      | README banner, dark backgrounds (white lettering)               |
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

## Why `<picture>` and two banner files

The READMEs wrap the banner in `<picture>` with a
`prefers-color-scheme: dark` `<source>` pointing at `dgpy-banner-dark.svg`.
Don't swap this for one SVG with a media query inside it. An SVG loaded
through `<img>` follows the OS colour scheme, not the page's, so on PyPI
(always a light page) a dark-mode OS would get white lettering on white.
PyPI strips `<source>` and always shows the light `<img>`.
