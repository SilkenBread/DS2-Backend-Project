FROM python:3.9
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
