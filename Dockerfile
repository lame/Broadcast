FROM python:3.5.2-slim

COPY . /docker_app

WORKDIR /docker_app

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python", "manage.py", "runserver", "--host", "0.0.0.0"]
