# KURF-Telehealth

# SOURCES
## Developer Installation Instructions
### Local Environment
To install the software and use it in your local development environment, you must first set up and activate a local development environment. From the root of the project, execute the following commands:

```
$ virtualenv venv
$ source venv/bin/activate
```

### Install Packages
Install all the packages required to run the software by executing the following command:

```
$ pip3 install -r requirements.txt
```

### Database Migrations
To migrate the database, run the following command:

```
$ python3 manage.py migrate
```

### Handling Issues
Sometimes, migrations may not work as they are intended due to a variety of factors.

In this case, we recommend the following set of steps:

#### Delete all files within ticketing_system/migrations excluding __init__.py
#### Delete the db.sqlite3 file from the root directory of the project
#### Run the following commands in this order:
```
$ python3 manage.py makemigrations
$ python3 manage.py migrate
```

### Running The Server
Run the server:

```
$ workon venv
$ python3 manage.py runserver
```

By default, the server will run on localhost port 8000 (http://127.0.0.1:8000/)


