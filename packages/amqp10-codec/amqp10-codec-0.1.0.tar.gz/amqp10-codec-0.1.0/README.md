# AMQP 1.0 Message Format

![testing](https://github.com/effedib/ParserAMQP/actions/workflows/test.yml/badge.svg)

The library is for encode and decode AMQP 1.0 message format. 

### Use Poetry
- create your virtual environment with `python -m venv venv`
- activate your virtual environment with `source venv/bin/activate`
- install poetry with `pip install poetry isort black pytest`
- install dependencies with `poetry install`
- run tests with `poetry run pytest`

### Contributing to the project
Format and sort the code with 
- `poetry run black amqp10_codec tests`  
- `poetry run isort amqp10_codec tests`.


