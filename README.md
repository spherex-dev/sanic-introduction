# An Async based HTTP server using Sanic

Sanic is a flask like http server that supports asynchronous requests and is very fast. 

This code base provides a simple example of using Sanic coupled with sqlalchemy to create a simple rest http api with protected endpoints.

This example can be downloaded and extended by the user. We also accept comments and pull requests for new features.


## Installation

A python version 3.7 or higher is required. Required depenedencies are included in the requirements.txt file and can be installed via `pip install -r requirements.txt`.

## Running the tests

Running the unit tests will provide the fastest way to understand how the code works. When running test, ensure that the path of the root of this repository is added to the PYTHONPATH environment variable.

### User endpoint tests

The user endpoint tests are located under `./user/tsts/test_user.py` will illustrace a simple request to an end point and the creation/deletion of a user, in addition to connection to a protected endpoint.