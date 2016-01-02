cd src
coverage run --source=tests -m py.test && coveralls
# py.test --cov=tests
