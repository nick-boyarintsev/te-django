# Django Project Example

## Local Deployment

Open the terminal and run the following commands:

```bash
git clone https://github.com/nick-boyarintsev/te-django.git te-django
cd te-django
```

Make sure you have Docker installed and configured correctly. Create a file in the project folder with the name - `docker-compose.override.yml`. Copy the contents of `docker-compose.override-dev.yml` to this file. If you need it, substitute the values of environment that suit you. Make sure port 8000 is free.

Next, run the following command:

```bash
docker-compose up -d --build          # builds the images and runs the containers
```

After executing the last command, all required docker images will be downloaded and built. The web-server will start.

## Starting or stopping work

If you don't need to build the image, but need to start the web server, just run one of the following commands:

```bash
docker-compose up -d          # (re)creates and starts the docker containers
docker-compose start          # only starts the docker containers
```

If you need to stop the web server, just run one of the following commands:

```bash
docker-compose down           # stops and destroys the docker containers
docker-compose stop           # only stops the docker containers
```

## Viewing logs

If you want to view Django's web-server logs, run the following command:

```bash
docker-compose logs -f backend
```

## Running tests manually

If you want to run Django's tests manually while the web-server is running, simply run the following command:

```bash
docker-compose exec backend python3 manage.py test
```

## Testing API

To test API, I use HTTPIE command line utility. The installation guide is [here](https://httpie.io/docs#installation). Or you can, for example, use [Postman](https://www.postman.com/).

An example of testing a request using HTTPIE:

```bash
# get-request
http http://localhost:8000/api/v1/registrations/9f076b60-6012-4bf3-9c17-87b7e0ed56c6

# post-request
http post http://localhost:8000/api/v1/registrations registrationDate='2021-01-01T00:00:00.000000+01:00' locale='en' person='{"firstName": "First", "lastName": "Last", "email": "test@test.com"}'
```