FROM python:3.10

WORKDIR /app

RUN pip install --upgrade pip
RUN apt-get update && apt-get install -y sqlite3 libblas3 liblapack3
RUN pip install sqlite_vss numpy openai

ENV LD_LIBRARY_PATH=/path/to/lib:$LD_LIBRARY_PATH

COPY . /app/

CMD ["python", "app.py"]
