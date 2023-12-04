
install:
	pipenv install

dev:
	uvicorn magicpost.main:app --reload

demo:
	python -m magicpost.main