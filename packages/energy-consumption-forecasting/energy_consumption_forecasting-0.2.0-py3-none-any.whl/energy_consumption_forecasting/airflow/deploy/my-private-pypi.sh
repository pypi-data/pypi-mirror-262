# !/bin/bash

# Building and publishing the project using poetry in the private pypi repository.
# Before executing this file, poetry needs to know the repository in which it needs to 
# publish for that update the config file: 
# "poetry config repositories.my-pypi http://localhost"

poetry build -vvv
poetry publish -r my-pypi