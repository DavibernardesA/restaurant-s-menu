install:
	pip install Flask
	pip install psycopg2
	pip install python-dotenv

clear:
	uninstall:
	pip uninstall -y Flask
	pip uninstall -y psycopg2
	pip uninstall -y python-dotenv