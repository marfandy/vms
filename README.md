# Vendor Management System powered by [Django](https://www.djangoproject.com/).
### Vendor Management System with Performance Metrics


## Quick Start

### Working with Python
Prerequisites
- git
- Python 3.10
- Code Editor (e.g. Visual Code)

1. Clone this project
    ```bash
    git clone git@github.com:marfandy/vms.git
    ```
2. Create `.env` and set your environment variables for development

    ```bash
    python3 -m venv venv
    ```
3. Active local environment
    ```bash
    source venv/bin/activate
    ```
4. Init project (install packages and migrate table)
    ```bash
    make init-app
    ```

## Runing Test Suite.
1. Run all test
    ```bash
    make test
    ```
2. Run spesifict test by app
    ```bash
    make test testr={app_name.tests}
    ```
    ```bash
    make test testr=authentication.tests
    ```
    ```bash
    make test testr=v1.tests
    ```

## Run Project
```bash
make run
```

## API DOCS
```bash
http://127.0.0.1:8000/docs/
```

#### Seed User For Login
- username : admin
- password : admin!@#

<p align="center">~Happy Code~</p>

