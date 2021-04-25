# Introduction

Welcome to Vaccine Clinic Information and Scheduling System

* Title: ReadME.md
* Project: Vaccine Clinic Information and Scheduling System(VCISS)
* Team: NoMad
* Course Name: CIS 422
* Assignment: Project 1
* Date: April 14th, 2021

# Architecture

The website consist of three parts:

* A public site that lets people view user and clinic information.
* An admin site that lets you add, change, and delete data.

# Environment

database: mysql https://dev.mysql.com/downloads/mysql/
backend: django Python 3.7.9

# How to run

We’ll assume you have Django installed already.

You can tell Django is installed and which version by running the following command in a shell prompt (indicated by the
$ prefix):

`$ python -m django --version`

To run the Django project, first change into the outest directory, and run the following command in a shell prompt:

`$ python manage.py runserver `

Changing the port

By default, the runserver command starts the development server on the internal IP at port 8000.

If you want to change the server’s port, pass it as a command-line argument. For instance, this command starts the
server on port 8080:

`$ python manage.py runserver 8080`

To create your module, make sure you’re in the same directory as manage.py and type this command:

`$ python manage.py startapp [new module name]`

To sync models with db updates, the following commands can be used:

`$ python manage.py makemigrations`

`$ python manage.py migrate `

To populate dummy clinics for functional testing, run the following command in the terminal:

`$ python uploadTestData.py `

# Reference

For Django backend: https://docs.djangoproject.com/en/3.2

