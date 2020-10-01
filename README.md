# FastAPI-Django Template

A starter API REST template that mix two of most lovely
python web frameworks: [FastAPI](https://fastapi.tiangolo.com/) & [Django](https://www.djangoproject.com/)

## About

FastAPI is a relatively new web framework built on top of starlette and uvicorn,
making it one of the fastest python frameworks.
It was build follow international standars as OpenAPI and OAuth.

Django is a veteran, and is almost the standard in python web
development. One of the most powerful characteristics is it's own ORM thant only works
in company with itself.

This template is an integration of both tecnologys that allows make use of the FastAPI
routing that provides request validation and automatic swagger documentation and the
Django-ORM and Django-Admin.

**FastAPI** manage all view/routing and network layer (including middlewares).
**Django** manage the DB layer trhough thd DjangoORM and implements the AdminPanel

## Characteristics

- Routing and view layer trhough the FastAPI api.
- Automatic documentation in swagger and OpenAPI
- Complete access to Django-ORM and it migration capabilities.
- Env varibles through dotenv file.
- Docker integration.
- PostgreSQL as default DB
- Docker compose to orchest the trhee primarly services:
  - The API server
  - The AdminPanl
  - Postgres instance

- Use [poetry](https://python-poetry.org/docs/), the best python package manager.
- Flake8 and Black as code formaters.

## Prebuilt Features

- Initial user endpoints to:
  - signup
  - login (cookie based)
  - update user info
  - send password recovery email
  - reset password

- Email module that allow by default:
  - send a welcome email
  - send email for password recovery

- Common response module:
  - Schemas to document swagger response info
  - Exception module with the most common http errors

- Auth & Security module:
  - Allow create JWT for session and password recovery
  - Authentication middleware

## Installation

You must need to have Django installed and type in the terminal:

```bash
django-admin startproject \
--template=https://github.com/emanuelosva/fastapi-django-template/archive/master.zip \
--extension py,yml,toml,ini \
<project_name>
```

## Usage

First you must to rename the file /app/.env.example as /app/.env
and set the needed secrete vars.

Then build the Docker image.

```bash
source scripts/build.sh
```

To run all services on development only type:

```bash
source scripts/start-dev.sh
```

Then you can browse in http://localhost:3000/docs and you will see something like this:

![imagen](https://user-images.githubusercontent.com/62397465/94862576-d11f5480-03fe-11eb-9adf-2fca029becb8.png)

To access to Django admin panel go to: http://localhost:8000/admin

## File structure

- **app**
  - app - Settings and entrypoint
    - ***settings*** - All settings
    - ***urls*** - Merge all FastAPI routers
    - ***wsgi*** - The FastAPI entrypoint
  - services - This dir contain all common features and modules
  - users - The users app (Like Django style)
    - ***admin*** - Same as in Django 
    - ***apps*** - Same as in Django
    - ***models*** - Same as in Django
    - ***schemas*** - Pydantic models used to validate requests and document
    - ***views*** - Bussiness logic
    - ***urls*** - FastAPI router for users
  - any_other_app - 
    - ***Same structure that users***

#### Integrate poetry in VSCode

To use the poetry virtual env and activate autocomplete features you need to modify the .vscode file, and add:

```json
{
  "python.venvPath": "~/.cache/pypoetry/virtualenvs",
  "python.pythonPath": "~/.cache/pypoetry/virtualenvs/<name_of_your_virtualenv>"
}
```

#### Create a new app

To create a new app you must have positioned in app dir and type:

```bash
# If poetry shell is off
poetry run django-admin startapp <app_name>

# If poetry shell is active
django-admin startapp <app_name>
```

#### The schema.py file

The `schema.py` is used to declare [Pydantic](https://pydantic-docs.helpmanual.io/) objects.
**FastAPI** use pydantic objects to validate the request and response data and generate the automatic documentation.

To improve the deveoper experience and use the DRY pattern this template make use of [pydantic-django](https://pypi.org/project/pydantic-django/).
This package allows to convert the Django Model into a Pydantic object and you can exclude any field.

Example

```python
from pydantic-django import PydanticDjangoModel
from pydantic import BaseModel
from .model import Model

class ModelSchema(PydanticDjangoModel):
    some_aditional_fiel: str
    class Config:
        model = Model
        exclude = ["hidden_field", "metadata"]

class ModelSchemaInput(BaseModel):
    field_one: str
    fielf_two: int
```

### Middleware

How FastAPI is the view manager, the Django middlewares are no useful.
If you want to add some middleware check the FastAPI docs:
- [Dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-in-path-operation-decorators/)
- [Middleware](https://fastapi.tiangolo.com/tutorial/middleware/)

The prebuild authentication middleware used in this template make use of
`dependencies in route functions` to get [the current user](https://fastapi.tiangolo.com/tutorial/security/get-current-user/)

The usage is:

```python
from fastapi import Depends, APIRouter
from services.auth.utils import get_auth_user

router = APIRouter

@router.post("/secure-path/{param}")
def some_secure_operation(param: str, user=Depends(get_auth_user)):
    # If the session is invalid or user is not found
    # a exception is raised before the code below is executed.
    result = some_secure_process(param, user)
    return result
```

## Usefull links

- [FastAPI official documentation](https://fastapi.tiangolo.com/)
- [Django documentation](https://www.djangoproject.com/)
- [FastAPI official project template](https://github.com/tiangolo/full-stack-fastapi-postgresql/tree/master/%7B%7Bcookiecutter.project_slug%7D%7D/backend/app)
- [The inspired blog for this template](https://www.stavros.io/posts/fastapi-with-django/)

## Contributing
- If you want to add some feature only fork this repository and send a pull request.

## Author
Emanuel Osorio <emanuelosva@gmail.com>
