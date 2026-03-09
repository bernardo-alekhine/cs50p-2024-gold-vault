# Gold Vault

## [Video Demo](https://youtu.be/UEdGssHA8Ig)

## Content table

- [Description](#description)
- [Cautions](#cautions)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [App Docs](#app-docs)
- [Contact Information and Licensing](#contact-information)

### Description

This project aims to provide the user with a quick and efficient way to reversibly
encrypt and decrypt any types of files as wished. It uses python built-in `argparse` library to parse command line
arguments and functionalities from the `cryptography` module.

It provides the `gvault` entry point command to enrypt file which follows this structure:

`gvault (-e|--encrypt)|(-d|--decrypt) input_paths... (-o|--output_paths) outpupt_paths...`

Flags of `-e` and `-d` specify the usage of the program. Followed by the arguments of file paths to perform the
operations. And then output paths as `-o`. The input path's output path post processing is implicitly taken as the
element at same index at output path. So in:

`gvault -e file1.txt file2.txt -o output1.txt output2.txt`

`file1`'s output file post processing will be `output1.txt`, `file2` will be `output2`, etc.

Any invalid usage will raise descriptive messages pointing the root of the error. After inserting the valid command,
a password will be prompted through `getpass`, in which it isn't visible and won't be saved in the terminal history.
This password will be derviated into a key and be the way to revert the cryptography of given file. Only if such
password is the same password that was used on encryption of this file. So for:

`gvault -e file1.txt -o output1.txt`
`Password: John`

`output1.txt` decrpytion will only work with:

`gvault -d output1.txt -o decrypted_file.txt`
`Password: John`

Else, an decryption error will be raised.

### Cautions

Only files encrypted by `gvault` will be able to be decrypted by `gvault` decrypt functionality. If the password for an
encrypted file is forgotten, the `gvault` command doesn't have any way to retrieve or decrypt it by any conventional
means offered by the program. Any operation executed by `gvault` won't delete the given `input_paths` but occasional
overwriting of files of `output_paths` might to do so. In case of any path existing with same name as the output path
given, confirmation will be asked to overwrite the already existing output path.

`gvault` performs file IO operations, read on the input paths given and write to given output paths. Any possible
unexpected behavior in system's resources or other operations related to such built-in functionality might affect the
program's normal behavior.

Encrypted files preferably shouldn't have their data modified, or it could put at risk the original data written to it
to be reversible to decryption.

For sake of simplicity and efficiency, confirmation isn't asked for passwords. So, if in doubt whether the password
typed is correct. Attempt decryption of the now encrypted file using the same password. Preferably don't delete the
original file or its data before assuring it's with the correct password.

### Prerequisites

- Python 3.12.4 or later: [Download Python](https://www.python.org/downloads/)
- pip 24.2

### Installation

1. Run `pip install .` at the top level directory of the project. Either local or virtual (venv).

2. The `gvault` command will be available at the command line interface to use.

### App docs

Brief documentation referent to app specific structure, behavior or functionality are found at [docs](docs/).

#### Contact Information

- GitHub: [Bernardiswz](https://github.com/bernardo-alekhine)
- LinkedIn [Bernardo Alekhine](https://www.linkedin.com/in/bernardo-alekhine)

This project may not be production-ready and/or fully fledged.
I take no responsibility for the usage or any possible fails or losses of data through the usage of `gvault`. Since it
is a learning project and the project and meant to be sent to CS50P 2024 as the final project.
