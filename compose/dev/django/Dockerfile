FROM python:3.6-alpine

ENV PYTHONUNBUFFERED 1

RUN apk update \
  # psycopg2 dependencies
  && apk add --virtual build-deps gcc python3-dev musl-dev \
  && apk add default-libmysqlclient-dev \
  # Pillow dependencies
  && apk add jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev \
  # CFFI dependencies
  && apk add libffi-dev py-cffi 

# Requirements are installed here to ensure they will be cached.
COPY ./requirements /requirements
RUN pip install -r /requirements/dev.txt

COPY ./compose/production/django/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

COPY ./compose/dev/django/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

WORKDIR /app

ENTRYPOINT ["/entrypoint"]
