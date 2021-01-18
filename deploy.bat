rm -rf build/
rm -rf dist/
rm -rf python_geth.egg-info/
bump2version --allow-dirty patch setup.py
python setup.py test sdist bdist_wheel
python -m twine upload --repository pypi dist/*
