FROM python:3.8
COPY ./Survey /Survey
RUN pip install -r /Survey/requirements.txt
CMD ["python", "./Survey/manage.py", "runserver"]
