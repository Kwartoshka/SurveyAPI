FROM python:3.8
COPY ./Survey /Survey
WORKDIR /Survey
RUN pip install -r /Survey/requirements.txt
CMD ["python", "manage.py", "runserver", "0.0.0.0:5000"]
