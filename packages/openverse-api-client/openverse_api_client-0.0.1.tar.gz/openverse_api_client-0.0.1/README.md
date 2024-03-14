# openverse-api-client

Fully typed Openverse API clients for Python and JavaScript.

[![PyPI - Version](https://img.shields.io/pypi/v/openverse-api-client.svg)](https://pypi.org/project/openverse-api-client)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/openverse-api-client.svg)](https://pypi.org/project/openverse-api-client)

-----

## Installation

**Python**

```console
pip install openverse-api-client
```

**JavaScript**

```console
npm install @openverse/api-client
```

## Development

**Dependencies**:
- `hatch`
- `pnpm`
- `just`

This project generates Python and TypeScript clients for the Openverse API, based on endpoint definitions written in Python, and Jinja2 templates for Python and TypeScript files. A full build of both clients requires the following steps:

1. Generating the client code: `hatch run generate`
2. Building the npm package (including TypeScript definitions): `just pnpm build`
3. Building the Python package: `hatch build`

The `just build` recipe encapsulates these tasks into a single command. Each task can run on its own for debugging different parts of the client code generation or build process.

In most cases, you will need to run at least `hatch run generate` for development tools to work, because otherwise critical files will be missing that other runtime code depends on.

The Python clients live in the same package as the client generation code, which allows them to reuse the endpoint definitions for Python type hints without introducing an intermediary package. The Jinja2 dependency is optional, and only installed when the `generator` feature is installed (i.e., `pip install openverse-api-client[generator]`).

## License

`openverse-api-client` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
