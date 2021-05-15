# Backend-end _partnerdo.pl_

### Setup your VSC + pipenv

- `$ pipenv install` # create env in local machine
- `$ pipenv --venv` # get venv path
- setup settings

```javascript
{
   "python.pythonPath": "<env path>/bin/python",
  "[python]": {
    "editor.codeActionsOnSave": {
      "source.organizeImports": true
    }
  },
  "editor.formatOnSave": true,
  "python.linting.enabled": true,
  "python.linting.flake8Enabled": true,
  "python.linting.flake8Path": "<env path>/bin/flake8",
  "python.formatting.provider": "autopep8",
  "python.formatting.autopep8Path": "<env path>/bin/autopep8"
}
```

### Run project

#### _Without docker_

- `$ make activate`
- `$ make run`

#### _With docker_

- `$ make up`
- `$ make login`
- `$ make run` (no need to activate pipenv because docker plays role of scoped environment)

### Documentation

- [Tools](docs/tools.md)
- [Application architecture](docs/application.md)
- [Development](docs/development.md)
- [Deployment](docs/deployment.md)
- [Testing](docs/testing.md)
- [Commands](docs/commands.md)
