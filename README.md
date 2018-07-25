# Multilibrary API


Now it's API for multimedia library. Later it will be added front-end.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

```
- Python 3.5.2 + (Python 3.6 + recommended) with PIP
- some Linux distributive recommended
```

### Backend server local deploy

1) Firstly you need to install PostgreSQL database:

 - complete the first five steps from https://djbook.ru/examples/77/ (set title "postgres" to project db)
 - change db password to prevent ensuing error message:

```
$ sudo -u postgres psql -c "ALTER USER multilibrary_db PASSWORD '1111';"
```

2) In the selected directory create project folder and initiate git repository there.

3) In root project folder create and activate virtual environment:

```
$ python3.6 -m venv env
$ . env/bin/activate
```

4) Install all the dependencies:

```
$ pip install -r requirements.txt
```

5) Then run the server:

```
$ python manage.py runserver
```

 Server is ready!