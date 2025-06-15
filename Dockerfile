FROM python:3.12-alpine
RUN pip install flask
WORKDIR /app
COPY ./app.py .
ENTRYPOINT ["python"]
CMD ["app.py"]
