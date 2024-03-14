# 10Duke Scale SDK for Python

The 10Duke Scale SDK for Python is a library to facilitate building applications licensed using
[10Duke Scale](https://docs.scale.10duke.com/).

## Contents

- [Why?](#why)
- [Installation](#installation)
- [Development](#development)
- [Getting involved](#getting-involved)
- [Resources](#resources)
- [License](#license)

## Why

Providing a set of Python client bindings for the 10Duke Scale REST API and a set of helper classes
to configure the SDK, authenticate users, and provide authorization for API requests enables
software vendors to focus on their software and their application domain. The SDK makes using 10Duke
Scale in an application simpler and allows faster adoption.

## Installation

### Using pip

```bash
pip install tenduke_scale
```

### Using poetry

```bash
poetry add tenduke_scale
```

## Development

To get started with working on the code, clone this repository.

```bash
git clone git@gitlab.com:10Duke/scale/python/python-scale-sdk.git
```

Then you need to install the tools and dependencies.

Install poetry:

```bash
curl -sSL https://install.python-poetry.org | python3
```

Start the virtual environment for the project:

```bash
poetry shell
```

Resolve dependencies:

```bash
poetry lock
```

Install dependencies:

```bash
poetry install
```

The tests can be run using

```bash
pytest .
```

For linux or macOS, a `Makefile` is provided to automate these, and other, development tasks.

### Code formatting / linting

This project is using:

- [ruff](https://github.com/astral-sh/ruff) for linting and code formatting
- [markdownlint](https://github.com/markdownlint/markdownlint) for linting markdown.

### Bumping version and releasing

The project is using [Semantic Versioning](https://semver.org/).

The version shall be set using `poetry version`. This will update the version number in
`pyproject.toml`.

That change shall be committed in a new revision.

That revision shall be tagged (for example `git tag v1.1.1`).

The new tag shall be pushed (`git push --tags`).

That will trigger the creation of a new package and the publishing of that package to the relevant
repository.

## Getting involved

We welcome contributions! [Contributing](./CONTRIBUTING) explains what kind of contributions we
welcome.

## Resources

- [10Duke Scale documentation](https://docs.scale.10duke.com/index.html)
- [10Duke.com](https://www.10duke.com/) - Find more information about 10Duke products and services

## License

10Duke Scale SDK for Python is licensed under the [MIT](./LICENSE) license.
