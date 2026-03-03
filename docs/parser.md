# Parser

## Content table
+ [Description](#description)
+ [Overview](#overview)

### Description
The [parser](/src/gvault/parser) package contains the app's algorithms and operations to generate a parser object
to parse command line arguments into an `argparse.Namespace` object. As following:

```
parse_args: argparse.Namespace = {
    encrypt (bool),
    decrypt (bool),
    input_paths (List[str]),
    output_paths(List[str])
}
```

Those arguments are parsed following this pattern:

`gvault (-e|--encrypt)|(-d|--decrypt) input_paths... (-o|--output_paths) outpupt_paths...`

All flags including either of mutually exclusive (encrypt|decrypt) are mandatory for the program's execution and
normal behavior.

### Overview ###
The `parser` package and it's sub modules and files contain doc strings of their own in their source code. And for more
in depth information or documentation it's advisable to peek at the code. But in summary, `parser` package provides an
interface to parsing of command line arguments through the help of many built-in python modules, and uses `argparse` to
parse args.
