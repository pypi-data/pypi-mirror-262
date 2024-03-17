# Baum

[![PyPI](https://img.shields.io/pypi/v/baum)](https://pypi.org/project/baum)
[![Typecheck](https://github.com/fwcd/baum/actions/workflows/typecheck.yml/badge.svg)](https://github.com/fwcd/baum/actions/workflows/typecheck.yml)
[![Test](https://github.com/fwcd/baum/actions/workflows/test.yml/badge.svg)](https://github.com/fwcd/baum/actions/workflows/test.yml)

A small Python script that generates a Unicode or ASCII tree from a parenthesized expression.

## Examples

```sh
baum "this [is [an, example, tree], with [a, bunch, of, nodes]]"
```

```
this
├─ is
│  ├─ an
│  ├─ example
│  └─ tree
└─ with
   ├─ a
   ├─ bunch
   ├─ of
   └─ nodes
```

In addition to the default style, which is `unicode`, a number of other styles are supported, which can be set via the `--style` flag, e.g.:

```sh
baum --style ascii "this [is [an, example, tree], with [a, bunch, of, nodes]]"
```

```
this
+- is
|  +- an
|  +- example
|  \- tree
\- with
   +- a
   +- bunch
   +- of
   \- nodes
```

Or even emoji for visualizing file trees:

```sh
baum --style emoji "this [is [an [], example [], tree []], with [a, bunch, of, nodes]]"
```

```
📁 this
  📁 is
    📁 an
    📁 example
    📁 tree
  📁 with
    📄 a
    📄 bunch
    📄 of
    📄 nodes
```

Run `baum --help` for a complete overview.
