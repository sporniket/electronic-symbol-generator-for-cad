# Sporniket's electronic symbol generator for CAD

[![Latest version](https://img.shields.io/github/v/release/sporniket/electronic-symbol-generator-for-cad?include_prereleases)](https://github.com/sporniket/electronic-symbol-generator-for-cad/releases)
[![Workflow status](https://img.shields.io/github/workflow/status/sporniket/electronic-symbol-generator-for-cad/Python%20package)](https://github.com/sporniket/electronic-symbol-generator-for-cad/actions/workflows/python-package.yml)
[![Download status](https://img.shields.io/pypi/dm/electronic-symbol-generator-for-cad-by-sporniket)](https://pypi.org/project/electronic-symbol-generator-for-cad-by-sporniket/)

> [WARNING] Please read carefully this note before using this project. It contains important facts.

Content

1. What is **Sporniket's electronic symbol generator for CAD**, and when to use it ?
2. What should you know before using **Sporniket's electronic symbol generator for CAD** ?
3. How to use **Sporniket's electronic symbol generator for CAD** ?
4. Known issues
5. Miscellanous

## 1. What is **Sporniket's electronic symbol generator for CAD**, and when to use it ?

**Sporniket's electronic symbol generator for CAD** is a python library with a command line interface to generate symbols of electronic packages for electronic CAD suites like Kicad.


### Licence

**Sporniket's electronic symbol generator for CAD** is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

**Sporniket's electronic symbol generator for CAD** is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more details.

### Release notes

#### v0.0.1

* TBD

## 2. What should you know before using **Sporniket's electronic symbol generator for CAD** ?

**Sporniket's electronic symbol generator for CAD** is written using python version 3.6, and should work with python version 3.7 up to 3.10.

It relies on the following packages to build and test :

* build
* pytest

It also relies on the following package to enforce source formatting :

* black

see [README packaging](https://github.com/sporniket/electronic-symbol-generator-for-cad/blob/main/README-packaging.md) for further details.

**Sporniket's electronic symbol generator for CAD** is build upon [Sporniket's electronic package descriptor](http://github.com/sporniket/electronic-package-descriptor) and its file format specifications.

> Do not use **Sporniket's electronic symbol generator for CAD** if this project is not suitable for your project.

## 3. How to use **Sporniket's electronic symbol generator for CAD** ?

### From sources

To get the latest available models, one must clone the git repository, build and install the package.

	git clone https://github.com/sporniket/electronic-symbol-generator-for-cad.git
	cd electronic-symbol-generator-for-cad
	python3 -m build && python3 -m pip install --force-reinstall dist/*.whl

Then, invoke the command line interface :

```
python3 -m electronic_symbol_generator_for_cad [option] input_file
```

### Using pip

```
pip install electronic-symbol-generator-for-cad-by-sporniket
```

Then, import the library in your code :

```
python3 -m electronic_symbol_generator_for_cad [option] input_file
```

## 4. Known issues
See the [project issues](https://github.com/sporniket/electronic-symbol-generator-for-cad/issues) page.

## 5. Miscellanous

Supplemental documentation :

* [README packaging](https://github.com/sporniket/electronic-symbol-generator-for-cad/blob/main/README-packaging.md) : some technical details about packaging this project.
* TBD...

### Report issues
Use the [project issues](https://github.com/sporniket/electronic-symbol-generator-for-cad/issues) page.
