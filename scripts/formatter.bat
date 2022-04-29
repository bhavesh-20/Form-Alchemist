call autoflake --in-place --remove-all-unused-imports --recursive --exclude=__init__.py app
call isort app
call isort main.py
call black app
call black main.py