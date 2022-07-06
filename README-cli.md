# The command line interface

## Synopsis

```
python3 -m electronic_symbol_generator_for_cad --format=[format] --into=[path] [source files]
```

Convert the each source file into the target format.

## Mandatory arguments

* `source files` : one or more files, each can be either [a Markdown structured datasheet](https://github.com/sporniket/electronic-package-descriptor/blob/main/README-datasheet.md) (extension `.md`) or a [JSON serialized format](https://github.com/sporniket/electronic-package-descriptor/blob/main/README-json.md) (extension `.json`)

## Optional arguments

* `--format=[format]` (short form : `-f [format]`) : format of the output file ; either `json`, `kicad5` or `kicad6` ; the default value is `kicad6` ; the JSON format is following [this specification](https://github.com/sporniket/electronic-package-descriptor/blob/main/README-json.md) ; the Kicad 5 symbol library is a `.lib` file ; the Kicad 6 symbol library is a `.kicad_sym`.
* `--into=[path]` : directory where the output file will be generated ; when not specified, the output file is generated in the same directory than the input file.
