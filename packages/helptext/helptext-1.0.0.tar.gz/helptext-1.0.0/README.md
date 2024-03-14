# Help Text - a documentation-generated argument parser

### Stop wasting time on over-engineered nonsense.

> [PEP 257 – Docstring Conventions][1]
>
> The docstring of a script (a stand-alone program) should be usable as its
> “usage” message, [...] as well as a complete quick reference to all options
> and arguments for the sophisticated user.

### Which means your script can already do this:

```py
"""
Usage: hello [-ghv]

OPTIONS
  -h, --help           display this help text and exit
  -v, --version        display version information and exit
  -g, --global         print a familiar message
"""

__version__ = '1.2.3'

import sys
from helptext import parse

opts, _ = parse(sys.argv[1:], __doc__, __version__)
if opts['--global']['enabled']:
    print('Hello, world!')
```

```console
$ hello -h
Usage: hello [-ghv]

OPTIONS
  -h, --help           display this help text and exit
  -v, --version        display version information and exit
  -g, --global         print a familiar message
$ hello --version
1.2.3
$ hello -g
Hello, world!
```

# Installation

```console
$ python3 -m pip install helptext
```

# API

Help Text provides a single `parse` function.

## parse

```py
from helptext import parse
opts, operands = parse(args, doc, version=None, posixly_correct=False)
```

### Arguments
  - `args`: a list of command-line argument strings.
  - `doc`: a docstring containing an _option list_.
  - `version`: a version string.
  - `posixly_correct`: a boolean to enable POSIX mode.

If `version` is not `None`, checks for `--help` and then `--version`. If
defined in `doc` and invoked in `args`, prints `doc` or `version` accordingly,
then raises `SystemExit(0)`.

If `posixly_correct` is `True`, support for GNU-style long options is disabled
and non-option operands terminate argument parsing.

### Return Values
  - `opts`: a dictionary of option flags (e.g. `-h`, `--help`):
    - `flags`: a list of flag aliases for this option.
    - `argument`: a boolean for whether an argument is required or forbidden.
    - `enabled`: an integer count of command-line invocations.
    - `value`: an option-argument string, default is `None`.
  - `operands`: a list of non-option operand strings.

# Docstring Format

```py
"""
  -a --alpha           this option takes no arguments
  -b arg --beta        this option requires an argument
  -c, --gamma arg      this option behaves the same
                       this line will be ignored
  -d, --delta=arg      attached notation works as well
"""
```

- Leading whitespace is ignored.
- Lines not beginning with a dash (`-`) are ignored.
- Flags and option-arguments are separated by whitespace or commas (`,`).
- All flags on a line are aliases to the same option.
- A single option-argument will also set the requirement for all aliases.
- Long option flags may attach option-arguments with an equals sign (`=`).
- Line parsing is terminated by two consecutive spaces (`  `).

# Best Practices

Designing user interfaces is _hard_. Even simple text-based command-line
interfaces are difficult to execute cleanly. We do have some standards to
guide us (e.g. [POSIX][2], [GNU][3]), but we are contending with several
decades of legacy code and bad advice ([argparse][4]).

The features below are unsupported in favor of encouraging CLI best practices.

<table>
  <thead>
    <tr>
      <th style="width:30%">Feature</th>
      <th>Comment</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><b>Required options</b></td>
      <td>
A required option is an oxymoron. Set a reasonable default or use positional
arguments to accept input, otherwise subcommands can be used to change modes.
      </td>
    </tr>
    <tr>
      <td><b>Mutually-exclusive options</b></td>
      <td>
Reduce command-line clutter by inverting your program logic. Use subcommands
or an option-argument to select a value from a list.
      </td>
    </tr>
    <tr>
      <td><b>Optional option-arguments</b></td>
      <td>
Indicates an overloaded option. Can often be split into two options, one that
requires an option-argument and another that does not.
      </td>
    </tr>
    <tr>
      <td><b>Multiple option-arguments</b></td>
      <td>
The standard approach is to use comma- or whitespace-separated values inside
a single (quoted or escaped) option-argument. Such values can even accept
arguments of their own by attaching them with an equals sign.
      </td>
    </tr>
  </tbody>
</table>

[1]: https://peps.python.org/pep-0257
[2]: https://pubs.opengroup.org/onlinepubs/9699919799/basedefs/V1_chap12.html
[3]: https://www.gnu.org/software/libc/manual/html_node/Argument-Syntax.html
[4]: https://docs.python.org/3/library/argparse.html

