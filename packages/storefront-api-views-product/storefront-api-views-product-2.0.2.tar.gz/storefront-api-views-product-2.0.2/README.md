# Storefront API Views - Product

[![python](https://img.shields.io/badge/python-3.8-informational)](https://docs.python.org/3.8/)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![pytest](https://img.shields.io/badge/pytest-enabled-brightgreen)](https://docs.pytest.org/en/latest/)

## Getting Started

```bash
pip install storefront-api-views-product
```

For the full details of this library, see the included [documentation](docs/README.md).

## Library Development

Getting started with developing on storefront-api-views-product

### Setup your virtual environment

You will have 2 choices here depending on whether you use `pyenv-virtualenv` or `virtualenv`

1. Using `pyenv-virtualenv`:
    ```bash
    pyenv virtualenv 3.8 storefront-api-views-product
    echo "storefront-api-views-product" >| .python-version
    ```

2. Using `virtualenv`:
    ```bash
    virtualenv -p python3 venv
    source venv/bin/activate
    ```

### Install dependencies

Install the service and developer dependencies, as well as, configure pre-commit

```bash
make deps
pre-commit install
```

> **Note:** If you have already set up the repo, and just want to update your dependencies, just use:
> ```bash
> make deps
> ```

> **Note:** If you want to run the pre-commits without committing to a branch:
> ```bash
> pre-commit run
> ```

### Running Unit Tests

```bash
make test
```

> **Note:** This will generate an HTML coverage file located at `htmlcov/index.html`
