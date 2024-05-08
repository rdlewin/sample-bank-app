FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./src /src

# Image expects a file /app/main.py or /app/app/main.py,
# so overriding it by running from root + symlinking /app to point at /src

RUN rm -rf /app && \
    ln -s /src /app

WORKDIR /