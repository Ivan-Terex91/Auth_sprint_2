FROM python:3.9-slim
EXPOSE 80
WORKDIR /api/app

RUN apt-get update && apt-get --yes upgrade

COPY ./requirements /api/requirements
RUN pip install -r /api/requirements/prod.txt --no-cache-dir

COPY . /api

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]
