# base image
FROM python:3.6.5-slim

# set working directory
WORKDIR /usr/src/app

# add app
COPY . /usr/src/app/

# add and install requirements
RUN pip install -r requirements.txt

# add entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh

EXPOSE 5000

# run server
CMD ["/usr/src/app/entrypoint.sh"]
