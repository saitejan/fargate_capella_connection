FROM python:3.9

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt

COPY . /app

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]


# FROM ubuntu:16.04

# RUN apt-get update -y && \
#     apt-get install -y python-pip python-dev

# COPY ./ /app
# WORKDIR /app
# RUN pip install -r requirements.txt
# # ENTRYPOINT [ "python" ]
# CMD [ "uvicorn main:app" ]

# Base image