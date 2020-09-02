# Ecosystem Notebooks

## What is Ecosystem Notebooks?

Ecosystem Notebooks is a wrapper for the Ecosystem API servers. They can be used for both the Prediction and Runtime servers. 

The notebooks are a great interface to work from in order to test, and explore the server’s capabilities. They allow you to navigate them easily by removing the complexities of directly interacting with the APIs.

Ecosystem Notebooks are built using the Jupyter Notebook coding environment, and Python 3 kernel for code execution.

## Requirements

* To use any of the notebooks, access to an Ecosystem API server is required
* [Jupyter Notebook](https://jupyter.org/)
* [Python 3](https://www.python.org/downloads/): The notebooks were built using python 3.6, but most Python 3 versions will work

## Getting started

To begin using Ecosystem Notebooks, you need to first install Jupyter Notebook.

This can be done by running the configure_jupyter.sh shell script. 
In addition, recommended styling options can be added by running the configure_jupyter_styling.sh shell script. While this is not required, you are welcome to play around with it to personalise the Ecosystem workbench style.

To install the relevant python code, add the parent directory (ecosystem-notebooks) to the PYTHONPATH environment variable. 

Once Jupyter is installed, enter the directory containing the notebooks. At the designated .ipynb extension, run the command:
```bash
jupyter notebook
```
This will open up a default web browser to the Jupyter Notebook landing page from which you can open up one of the desired notebooks.

![Jupyter Landing Page](https://github.com/ecosystemai/ecosystem-notebooks/blob/master/docs/images/jupyter_landing_page.png "Jupyter Landing Page")

## How does Ecosystem Notebooks work

From within a chosen notebook, Ecosystem Notebooks can be used. This coding environment, from which you can edit and run live code, provides the interface with which to utilise the API endpoints for Ecosystem Prediction and Runtime servers.For easy navigation within any of the notebooks, you can use the table of contents which will be situated on the left.

In order for the API endpoints to properly function, you will need to login. Depending on which notebooks you have chosen to use, logging in could require a URL endpoint. Or a username, password and URL combination, which will generate an authentication token. This token will activate the API, then you can begin using Ecosystem Notebooks!

![Login](https://github.com/ecosystemai/ecosystem-notebooks/blob/master/docs/images/login.png "Login")

Ecosystem Notebooks contains all the available API endpoints on the Ecosystem Servers. You can either play around in the ecosystem environment, or you can use it in your own chosen infrastructure.
