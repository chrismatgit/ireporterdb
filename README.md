[![Build Status](https://travis-ci.org/chrismatgit/ireporterdb.svg?branch=develop)](https://travis-ci.org/chrismatgit/ireporterdb)             [![Coverage Status](https://coveralls.io/repos/github/chrismatgit/ireporterdb/badge.svg?branch=develop)](https://coveralls.io/github/chrismatgit/ireporterdb?branch=develop)           [![Maintainability](https://api.codeclimate.com/v1/badges/7b9d7da2259084c82395/maintainability)](https://codeclimate.com/github/chrismatgit/ireporterdb/maintainability)


# iReporterdb


Corruption is a huge bane to Africa’s development. African countries must develop novel and localised solutions that will curb this menace, hence the birth of iReporter. iReporter enables any/every citizen to bring any form of corruption to the notice of appropriate authorities and the general public. Users can also report on things that needs government intervention


## Getting Started

You can clone the project using the link [Github repository] (https://github.com/chrismatgit/ireporterdb.git) .


## Installing

* Clone the project into your local repository using this command:

```sh
  $ git clone https://github.com/chrismatgit/iReporter.git
  ```
  Switch to the cloned directory, install a virtual environment, create a virtual environment, activate it, checkout to the most stable branch, install app dependencies and run the app.
  ```sh
    $ cd iReporter
    $ pip install virtualenv
    $ virtualenv -p python3 venv
    $ source venv/bin/activate
    $ git checkout ft-api
    $ pip install -r requirements.txt
    $ python3 run.py
 ```

**Note** If you're using Windows, activate your virtualenv using `` $ source venv/Scripts/activate ``
* Copy the url http://127.0.0.1:5000/ into your Postman and to run any endpoint follow the table under the heading (**Endpoints**) with the url prefix ('/api/v1') for each endpoint.

## Endpoints
HTTP Method | Endpoint | Functionality | Parameters | Protected
----------- | -------- | ------------- | ---------- | ---------
POST | /auth/signup | Create a user | None | False
POST | /auth/signup/admin | Create a admin | None | False
POST | /auth/login | Login a user | None | False
GET | /welcome | Welcome a user | None | True
GET | /users | Fetch all users | None | False
POST | /red-flags | Create a red-flag | None | True
GET | /red-flags/int:incident_id | Fetch a single red-flags record | incident_id | True
GET | /red-flags/| Fetch all red-flags records | None | True
PATCH | /red-flags/incident_id/comment| Update a comment of a single red-flag record | None | True
PATCH | /red-flags/incident_id/location| Update a location of a single red-flag record | None | True
PATCH | /red-flags/incident_id/status| Update a status of a single red-flag record | None | True
DELETE | /red-flag/incident_id| Delete a single red-flag record | incident_id | True
POST | /interventions | Create a intervention | None | True
GET | /interventions/int:intervention_id | Fetch a single interventions record | intervention_id | True
GET | /interventions/| Fetch all interventions records | None | True
PATCH | /interventions/intervention_id/comment| Update a comment of a single intervention record | None | True
PATCH | /interventions/intervention_id/location| Update a location of a single intervention record | None | True
PATCH | //interventions/int:intervention_id/status| Update a status of a single intervention record | None | True
DELETE | /intervention/intervention_id| Delete a single red-flag record | intervention_id | True


## Running the tests

Install pytest, source the .env file, run the tests.
```sh
  $ pip install pytest
  $ python3 -m pytest
  ```
## Deployment

The Python application is hosted on [Heroku](https://ireporterdbc.herokuapp.com/api/v1/)


## Tools Used

* [Flask](http://flask.pocoo.org/) - Web microframework for Python
* [Virtual environment](https://virtualenv.pypa.io/en/stable/) - tool used to create isolated python environments
* [pip](https://pip.pypa.io/en/stable/) - package installer for Python

## Built With

The project has been built with the following technologies so far:

* Python/Flask

## Contributions

To contibute to the project, create a branch from the **develop** branch and make a PR after which your contributions may be merged into the **develop** branch

## Authors

Christian Matabaro