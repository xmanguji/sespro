# setup directly from nodejs image from aws
FROM public.ecr.aws/lambda/python:3.8

COPY . /var/task/

# install native deps
RUN yum install -y postgresql-devel gcc
# install pip deps
RUN pip install -r requirements.txt
# install DB driver manually just in case
RUN pip install psycopg2
# install wrapper to translate API Gateway events from Lambda into ASGI requests (manually again, just in case)
RUN pip install mangum

# set lambda handler
CMD [ "main.app" ]
