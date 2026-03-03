# Structure

### Project structure
The project top level directory is structured as the following:

```
|-- README.md
|-- docs
|-- screenshots
|-- pyproject.toml.bak
|-- pytest.ini
|-- requirements.txt
|-- setup.py
|-- src
|-- tests
```

The project's modules and source code are located in `src/gvault/`. `pyproject.toml` contains configurations to the
project's development or usage on external tools, such as `black`, `coverage`, and others. Its format was changed to
`.bak` to prevent it from causing conflicts on the package installation. But if needed to development purposes, just
remove the `.bak`. `pytest.ini` sets to ignore the learning tests at the tests directory, containing onl

Other directories that are included or were omitted by `.gitignore` are cache related or `venv`. So the project can
contain those directories or cache files aswell.
