autoflake -i -r --remove-all-unused-imports src/filare/
isort src/filare/*.py src/filare/tools/*.py
black src/filare/*.py src/filare/tools/*.py
