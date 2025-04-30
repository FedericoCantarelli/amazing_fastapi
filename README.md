# Amazing FastAPI
> The definitive FastAPI template for complex project.

![Fast API](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=%23ffffff)
![Uv package manager](https://img.shields.io/badge/package_manager-606060?style=flat-square&logo=uv&logoColor=%23ffffff&label=uv&labelColor=DE5FE9)
![Code style](https://img.shields.io/badge/code_style-606060?style=flat-square&logo=ruff&logoColor=%23333&label=ruff&labelColor=D7FF64)
![Code quality](https://img.shields.io/badge/code%20quality-606060?style=flat-square&logo=pytest&logoColor=ffffff&label=pytest&labelColor=0A9EDC)
![Type Checking](https://img.shields.io/badge/type%20checking-606060?style=flat-square&label=MyPy&labelColor=%231E5082)

## Repository Structure
### App Code
```
app
├── __init__.py
├── __version__.py
├── core
│   ├── __init__.py
│   ├── env_config.py
│   ├── exceptions.py
│   ├── logger.py
│   └── validation.py
├── dependencies.py
├── log_config.json
├── main.py
├── middleware
│   ├── __init__.py
│   └── debug_middleware.py
├── models
│   └── __init__.py
├── repository
│   ├── __init__.py
│   └── base_repository.py
├── routers
│   ├── __init__.py
│   ├── healthcheck.py
│   └── v1
│       ├── __init__.py
│       ├── routes
│       │   └── __init__.py
│       └── v1_router.py
├── services
│   ├── __init__.py
│   └── setup.py
└── views
    ├── __init__.py
    ├── error_response.py
    └── ready_response.py
```
### Secrets
All the secrets can be safely stored in `.secrets` folder. All the files included in this folder are ignored by git.