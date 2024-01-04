#!/bin/bash

rm dist/*
. ${PYENV_ROOT}/versions/blenderLibBuild/bin/activate
python -m build  
twine upload --skip-existing -r pypitest dist/*