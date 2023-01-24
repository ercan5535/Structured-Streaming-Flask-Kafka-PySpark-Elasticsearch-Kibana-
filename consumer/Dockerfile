
FROM openjdk:slim
COPY --from=python:3.8-slim-buster / /


WORKDIR /python-docker

COPY . .
RUN pip3 install -r requirements.txt


CMD ["spark-submit", "--packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.1", "--jars", "elasticsearch-spark-30_2.12-8.5.3.jar", "spark.py"]