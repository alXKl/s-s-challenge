FROM python:3.9-alpine

WORKDIR /api

COPY /api .

RUN pip install flask
RUN pip install requests

EXPOSE 5000

ENTRYPOINT ["python3"]
CMD ["api.py"]