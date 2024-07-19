test:
	python -m unittest discover

install:
	pip install Flask
	pip install psycopg2
	pip install python-dotenv
	pip install pytest
	pip install pytest-flask

uninstall:
	pip uninstall -y Flask
	pip uninstall -y psycopg2
	pip uninstall -y python-dotenv