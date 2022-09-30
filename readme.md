# Local Setup
- Clone the project
- Run `local_setup.sh`

# Local Development Run
- `local_run.sh` It will start the flask app in `development`. Suited for local development

# Replit run
- Go to shell and run
    `pip install --upgrade poetry`
- Click on `main.py` and click button run
- Sample project is at https://replit.com/@thejeshgn/flask-template-app
- The web app will be availabe at https://flask-template-app.thejeshgn.repl.co
- Format https://<replname>.<username>.repl.co

# Folder Structure

- `test_database` has the sqlite DB. It can be anywhere on the machine. Adjust the path in ``application/config.py`. Repo ships with one required for testing.
- `application` is where our application code is
- `.gitignore` - ignore file
- `local_setup.sh` set up the virtualenv inside a local `.env` folder. Uses `pyproject.toml` and `poetry` to setup the project
- `local_run.sh`  Used to run the flask application in development mode
- `static` - default `static` files folder. It serves at '/static' path. More about it is [here](https://flask.palletsprojects.com/en/2.0.x/tutorial/static/).
- `static/script.js` All the javascript functions have been added in this file
- `templates` - Default flask templates folder


```
├── application
│   ├── __init__.py
│   ├── config.py
│   ├── controllers.py
│   ├── database.py
│   ├── models.py
│   ├── api.py
│   ├── validation.py
│   └── __pycache__
│       ├── config.cpython-36.pyc
│       ├── config.cpython-37.pyc
│       ├── controllers.cpython-36.pyc
│       ├── controllers.cpython-37.pyc
│       ├── database.cpython-36.pyc
│       ├── database.cpython-37.pyc
│       ├── __init__.cpython-36.pyc
│       ├── __init__.cpython-37.pyc
│       ├── models.cpython-36.pyc
│       └── models.cpython-37.pyc
├── test_database
│   └── data.sqlite3
├── local_run.sh
├── local_setup.sh
├── main.py
├── poetry.lock
├── pyproject.toml
├── readme.md
├── requirements.txt
├── InsomniaAPI.yaml
├── static
│   ├── script.js
│   ├── image.jpg
│   └── card-checklist.svg
└── templates
    ├── login.html
    ├── base.html
    ├── home.html
    ├── create_list.html
    ├── update_list.html
    ├── create_card.html
    ├── update_card.html
    └── summary.html
```