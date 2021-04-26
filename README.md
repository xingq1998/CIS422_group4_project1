# Introduction

Welcome to Vaccine Clinic Information and Scheduling System

* Title: ReadME.md
* Project: Vaccine Clinic Information and Scheduling System(VCISS)
* Team: NoMad
* Course Name: CIS 422
* Assignment: Project 1
* Date: April 26th, 2021

# Architecture

The website consist of two parts:

* A public site that lets people view user and clinic information.
* An abilty for a user to schedule and manage a vaccination appointment at a clinic.

# Environment

* database: SQLite
* Website framework: django Python 3.7.9

# How to run

1) Open a shell program of your choice and change to the directory where this program is located.
2) You must have the django package installed on your local machine. You can tell django is installed and which version by running the following command.

    `$ python -m django --version`

3) The following command must be run if there is no version of django found.

    `$ pip install django`

4) Once django is installed, the database tables need to be created and synced by running the following commands:

    `$ python manage.py makemigrations`

    `$ python manage.py migrate`

5) Populate the database tables with test data by running:

    `$ python uploadTestData.py `

6) To run the Django project, run the following command in the shell prompt:

    `$ python manage.py runserver `

7) Finally, you will be able to use the website while the server is running. See UserGuide.md file for documentation on how to access and use the site.

8) Once you are done with the server and scheduling an appointment, return to the shell where you enterd the previous commands and press ctrl+c to stop the local server from running.


# Reference

For Django backend: https://docs.djangoproject.com/en/3.2
