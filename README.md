
# corteva-hiring-project

This repository is for the Cortev Hiring Process. Feedback regardless of the result would be appreciated.

The AWS discussion is in the file "AWS-structure.md"

### Installing the project
Use poetry for dependency managment.

Install poetry using 

`curl -sSL https://install.python-poetry.org | python3 -`

Or in windows by using 

``
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
``

Install by using

`poetry install`


Migrate the sqlite database using

`python manage.py migrate`


Run the debug server using

`python manage.py runserver`


Run the production server using

`poetry run gunicorn corteva_weather.wsgi:application --bind 0.0.0.0:8000`


Or, if you have docker installed, build the docker image using

`docker build -t image_name .`


And then run it

`docker run --env-file .env -p 8000:8000 image_name`


The swagger docs can be acessed by the url

`http://localhost:8000/api/schema/swagger-ui/`


### Data ingestion


For the Weather Station data, you can run the command :

`python manage.py ingest_weather_data folder_path` 


To generate the statistics, run the command

`python manage.py generate_statistics` 


To generate the statistics for a specific station_name, run

`python manage.py generate_station_statistics station_name`


To ingest the corn yield data, run

`python manage.py ingest_yield file_path`


Run tests using the command
`pytest`

### Some points of possible improvement

- Celery tasks
- Redis Cache
- Integration Tests
- Terraform
