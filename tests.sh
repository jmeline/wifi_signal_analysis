cd src
coverage run --source=tests -m py.test && mv .coverage ..
# py.test --cov=tests
