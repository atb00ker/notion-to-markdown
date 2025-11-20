.PHONY: init

init:
	python3 -m venv .venv
	.venv/bin/pip install --upgrade pip
	.venv/bin/pip install -r requirements.txt

test:
	pytest --cov=./notion_to_markdown --cov-report=term-missing --cov-report=html

release:
	git tag -a v$$(python setup.py --version) -m "Release version $$(python setup.py --version)"
	git push origin v$$(python setup.py --version)
	python setup.py sdist bdist_wheel
	twine upload dist/*
