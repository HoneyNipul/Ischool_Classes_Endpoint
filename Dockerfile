FROM python:3.6-slim-jessie

RUN apt-get -y update && apt-get -y upgrade && \
    apt-get install -y bash git libpq-dev \
    libtiff5-dev libjpeg-dev zlib1g-dev \
    libfreetype6-dev liblcms2-dev libwebp-dev libharfbuzz-dev libfribidi-dev \
    tcl8.6-dev tk8.6-dev python-tk curl apt-transport-https

RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/debian/8/prod.list > /etc/apt/sources.list.d/mssql-release.list

RUN apt-get -y update
RUN ACCEPT_EULA=Y apt-get install -y msodbcsql17
RUN apt-get install -y unixodbc-dev

RUN apt-get autoremove && apt-get clean

RUN pip install uwsgi

COPY . /var/webapp

COPY uwsgi.ini /etc/uwsgi/uwsgi.ini

WORKDIR /var/webapp

RUN pip install -r requirements.txt

COPY entrypoint.sh /usr/local/bin/entrypoint.sh

RUN chmod +x /usr/local/bin/entrypoint.sh

EXPOSE 9000

# Command to run the sites
CMD ["/bin/bash", "/usr/local/bin/entrypoint.sh"]