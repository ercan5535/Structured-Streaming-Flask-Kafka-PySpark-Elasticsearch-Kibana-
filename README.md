# Structured Streaming
Pipeline

<img src="https://user-images.githubusercontent.com/67562422/213930430-33b6af44-c0b6-434b-9405-d38fe077ec28.png" width="800" height="100" >
<br>
Flask App

<img src="https://user-images.githubusercontent.com/67562422/210098040-c3e1e4cf-3bcf-4c28-8ea6-ac55cf560d41.png" width="500" height="280" >

Kibana Dashboard

<img src="https://user-images.githubusercontent.com/67562422/210100372-c5ab6564-eb08-4545-9f31-318fe3f2475a.png" width="1000" height="280" >

In this project I created a structured streaming with common technologies.<br>
It was a good practice to use these technologies while working together.<br>

- Producer:<br>
Simple Flask App by ordering food and beverages.<br>
Flask App get that data and load to Kafka topic for every order.<br>

- Consumer:<br>
Spark Session to read stream from Kafka topic.<br>
PySpark reads streaming from Kafka, does some data processing and writes to Elasticsearch.<br>

- Visualization:<br>
Kibana to visualize Elasticsearch data.<br>

# Starting Services
Docker versions <br>
<img src="https://user-images.githubusercontent.com/67562422/214274763-a9432f84-d144-468d-9103-c4d687282e1d.png" width="300" height="50" >

<b>$ sudo docker-compose up</b> <br>
is fine to start all services. <br>

# Usage
Flask App: localhost:5000 <br>
Kibana Dashboard: localhost:5602 <br>









