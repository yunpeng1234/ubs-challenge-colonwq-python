# README

This is the [Flask](http://flask.pocoo.org/) [quick start](http://flask.pocoo.org/docs/1.0/quickstart/#a-minimal-application) example for [Render](https://render.com).

The app in this repo is deployed at [https://flask.onrender.com](https://flask.onrender.com).

## Deployment

If a new package is installed that does not come with python, add it to `requirements.txt` with the version number

## Adding API endpoints

Create a new folder under `routes` indicating challenge name

Copy the the `Blueprint` and the decorate to define a method
After resolving the answer, jsonify the output

Tag the blueprint object to the `app` object in `app.py` with `register_blueprint` to expose the endpoint

### Local testing

Uncomment out logging info onwards in `app.py` and just `python app.py`

Test with postman or unit test up to u keks


