os: linux
dist: xenial
language: python

python:
  - "3.5"
  - "pypy3.5"
  - "3.6"
  - "3.7"
  - "3.5-dev"
  - "3.6-dev"
  - "3.7-dev"
  - "3.8-dev"

env:
  - COVERAGE=True

matrix:
  fast_finish: true
  allow_failures:
    - python: "3.5-dev"
    - python: "3.6-dev"
    - python: "3.7-dev"
    - python: "3.8-dev"

# install dependencies
install:
  - pip install coverage codecov
  - pip install -r requirements.txt

# run tests
script:
  - ./test/RUN.sh

# upload coverage report to codecov
after_success:
    - codecov

# only trigger build for pushes on master branch
branches:
  only:
    - master
