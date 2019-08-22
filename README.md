# Flask-Api-Kit
This repository is a flask starter kit focusing on making robust API.

## API Usage

The api root will contain generated Swagger documentation for endpoints.
On a local environment this will usually be http://localhost:5000 if using docker-compose.

## Dev Setup

Copy the example .env file
```bash
cp .env.example .env
```

Run the Docker container the first time:
```bash
docker-compose up -d
```

After updating the source tree, to refresh the api containers:
```
docker-compose build
docker-compose up -d --force-recreate
```

Running migrations:
```bash
docker-compose run api alembic upgrade head
```

Check that the api is running at (http://0.0.0.0:5000/)

### Python dependencies

You must install the `pipenv` utility on your computer to update dependencies.

See the [Installation guide](https://pipenv.readthedocs.io/en/latest/install/#installing-pipenv)

To add a dependency to Pipfile and update Pipfile.lock
```bash
# from your project's root directory
pipenv install [package-name]
```

You can can also 
[specify the version](https://pipenv.readthedocs.io/en/latest/basics/#specifying-versions-of-a-package).
Using `~=` is preferred to `==` so the packages can be updated. Dont specify the patch version.
For example: instead of `==3.9.2` use `~=3.9`.

```bash
pipenv install [package-name]~=[version]
```

If you manually add a package to the Pipfile
```bash
pipenv lock
```

Add the dependencies to your current container
```bash
docker-compose exec api pipenv install --deploy --system
```

Rebuild the image (updates dependencies on the docker image):
```bash
docker-compose build api
```

Update dependencies to your current container
- Add <library> = "*" in packages section of Pipfile and execute below command to update single lib into env.
- Don't forgot to commit updated Pipfile.lock file.

```bash
docker-compose exec api pipenv update [library]
```

### View logs
```bash
docker-compose logs -f
```

## Database Migrations

Generating a Migration:

```bash
docker-compose run api alembic revision --autogenerat -m "<description of changes>"
```

Fixes migration permissions:
```bash
sudo chown -R ${USER}:${USER} alembic/versions
```

Running migrations:
```bash
docker-compose run api alembic upgrade head
```

Rolling back
```bash
docker-compose run api alembic downgrade -1
```

Resolve a Schema Conflict with a Merge
- check is schema conflict heads
```
alembic heads

#output
1e21d19c87f5 (head)
35cc6bc4108f (head)

```
- Merge conflict heads
```bash
alembic  merge -m "message" [HEAD-1] [HEAD-2]

#Example
alembic  merge -m "merge migrations 11912dfa54c4, 1944c1e7a0f4" 11912dfa54c4 1944c1e7a0f4
```

## Create Mock Data Seed
- Goto mock_seed/data
```bash
cd mock_seed/data
```

- Create mock data seed xml file
```xml
<table name="table_name">
    <row
            id="value"
            column1="value"
            column2="value"/>
    <row
            id="value"
            column1="value"
            column2="value"/>
</table>
```

- Open mock_seed/confmock.py and add file name in array of seed_file_order.
```python
seed_file_order = [
    'postal_addresses.xml',
    'persons.xml',
    'users.xml',
]
```

- Run mock seed script
```bash
docker-compose run api python seed_mock_data.py
```

## Create Test Data Seed 
- Goto tests/seed/data
```bash
cd tests/seed/data
```

- Create test data seed xml file
```xml
<table name="table_name">
    <row
            id="value"
            column1="value"
            column2="value"/>
    <row
            id="value"
            column1="value"
            column2="value"/>
</table>
```

- Open tests/conftest.py and add file name in array of seed_file_order.
```python
seed_file_order = [
    'addresses.xml',
    'contacts.xml',
    'users.xml',
]
```

##Testing

### docker-compose testing

Run all tests with docker
```bash
docker-compose run api_test
```

### localhost testing

- Create test database
- open .env file and set TEST_DATABASE_URI value
```bash
#example
TEST_DATABASE_URI=postgresql://postgres:password@localhost:5432/test_flask_api_kit
```

```bash
#Run all tests
python -m pytest -v

#Run specific test file
python -m pytest [file_path]

#example
python -m pytest tests/resources/test_post.py
python -m pytest tests/resources/test_post.py::TestPostResource::test_get_post_by_id
```

## Branching Strategy

* Use [git flow](https://danielkummer.github.io/git-flow-cheatsheet/)

### Creating a release

Based on the [git-flow](https://danielkummer.github.io/git-flow-cheatsheet/) workflow

```bash
git checkout -b release/2.0.0 qa
```

```bash
git commit -a -m "release [2.0.0] - 2019-06-01"
```

```bash
git checkout staging
git pull
git merge --ff-only release/2.0.0
git tag -a 2.0.0 -m "[2.0.0] - 2019-06-01"
```

```bash
git checkout dev
git merge release/2.0.0
```

## Code Style

* Use [PEP 8](https://www.python.org/dev/peps/pep-0008/)
* Use [mypy typing](http://www.mypy-lang.org/) whenever possible
* Make sure all code changes are linted
* Only break a standard if you have a good reason for doing so
* Disable linting rules on a case by case basis
* Make sure you understand the reason for a linting error before disabling a rule

### Linting

Always try to have 10/10 code. If you have a good reason to break the standard use 
`# pylint: diable=`.

Use pylint to lint the code:
```bash
pylint api
```

### Coding guidelines

Don't Repeat Yourself! (DRY) 

Always try to abstract out common code in a way that can be used a la carte.

### API Documentation

```bash
cd docs
sphinx-apidoc -f -o . ../api
```

```bash
cd docs
make html
```

#### marshmallow_with

The `marshmallow_with` is based on the 
[flask_restplus marshal_with() decorator](https://flask-restplus.readthedocs.io/en/stable/marshalling.html)

## Docker Details


The `docker-compose.yml` defines a network named `flask_api_kit`.
Containers are addressible by name within this network. This means that the api project `api` container can 
resolve the  project `minio` container.

This is why the `api` container uses the `minio` of `http://minio:9000`

### Coding guidelines

Don't Repeat Yourself! (DRY) 

Always try to abstract out common code in a way that can be used a la carte.

### API Documentation

```bash
cd docs
sphinx-apidoc -f -o . ../api
```

```bash
cd docs
make html
```

## useful commands

clean out all pyc files 
```bash
find . -name \*.pyc -delete
```
