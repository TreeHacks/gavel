FROM python:3.6.6

ARG APP_PATH=/gavel

WORKDIR $APP_PATH

ADD requirements.txt $APP_PATH
RUN pip install -r requirements.txt

ADD . $APP_PATH

EXPOSE $FLASK_RUN_PORT
# RUN python initialize.py

CMD ["python", "runserver.py"]
