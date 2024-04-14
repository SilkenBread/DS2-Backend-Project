# Backend Project for Software Development II
Made with Django RestFramework

## Steps for project creation
### Step 1 create `DockerFile` at root
```dockerfile
FROM python:3.10
# SET TIME ZONE  TO LOCAL TIME
RUN echo "America/Bogota" > /etc/timezone
RUN ln -fs /usr/share/zoneinfo/America/Bogota /etc/localtime
RUN dpkg-reconfigure -f noninteractive tzdata
# END SETTING UP TIMEZONE
ENV PYTHONUNBUFFERED 1
RUN mkdir /app
WORKDIR /app
ADD requirements.txt /app/
RUN apt-get update && apt-get install -y python3-gdal
RUN pip install -r requirements.txt
ADD . /app/
```
### Step 2 create `docker-compose.yml` at root
```yml
version: '3.5'
services:
  sigt_django:
    build: .
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - .:/my_app_django_dir
    ports:
      - "80:8000"
```

## Commands
```bash
sudo docker-compose run --rm backend-hoze django-admin startproject config .
```
```bash
sudo docker-compose run --rm backend-hoze python manage.py makemigrations
```
