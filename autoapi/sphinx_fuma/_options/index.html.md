# sphinx_fuma._options

Normalisation of `html_theme_options` into template-friendly context values.

Sphinx passes theme options through as `theme_<name>` context entries whose
values are strings when they come from `theme.conf` and arbitrary Python
objects when they come from `html_theme_options`. The templates want a single
normalised shape, so everything is coerced here rather than in Jinja.

## Functions

| [`build_context`](#sphinx_fuma._options.build_context)(→ dict[str, object])   | Return the `fuma_*` context entries derived from the theme options.   |
|-------------------------------------------------------------------------------|-----------------------------------------------------------------------|

## Module Contents

### sphinx_fuma._options.build_context(context: dict) → dict[str, object][[source]](../../../_modules/sphinx_fuma/_options.html.md#build_context)

Return the `fuma_*` context entries derived from the theme options.
