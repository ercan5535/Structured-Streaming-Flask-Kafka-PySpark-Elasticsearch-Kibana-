# Structured Streaming
In this project I created a structured streaming with common technologies.<br>
It was a good practice to use these technologies while working at the same time together.<br>

- Producer:
I create data from very simple Flask App by ordering food and beverages.<br>
Flask App get that data and load to Kafka topic for every order.<br>

- Consumer:<br>
I created a Spark Session to read stream from Kafka topic.<br>
PySpark reads streaming from Kafka, does some data processing and writes to Elasticsearch.<br>

- Visualization:<br>
I used Kibana to visualize Elasticsearch data.<br>

Flask App

<img src="https://user-images.githubusercontent.com/67562422/210098040-c3e1e4cf-3bcf-4c28-8ea6-ac55cf560d41.png" width="500" height="280" >

Kibana Dashboard

<img src="https://user-images.githubusercontent.com/67562422/210098100-9fbd6f2f-7724-4c46-94b8-817b39999232.png" width="1000" height="280" >


# Installation and Starting Services
## Step 1) Start Kafka broker service

#### - Get Kafka
$ wget https://dlcdn.apache.org/kafka/3.3.1/kafka_2.13-3.3.1.tgz <br>
$ tar -xzf kafka_2.13-3.3.1.tgz<br>
$ cd kafka_2.13-3.3.1<br>


##### - Start the Kafka environment
NOTE: Your local environment must have Java 8+ installed.
Run the following commands in order to start all services in the correct order:

##### - Start the ZooKeeper service
$ bin/zookeeper-server-start.sh config/zookeeper.properties
Open another terminal session and run:
##### - Start the Kafka broker service
$ bin/kafka-server-start.sh config/server.properties

Once all services have successfully launched, you will have a basic Kafka environment running and ready to use. 

Create topic:<br>
$ bin/kafka-topics.sh --create --topic orders --bootstrap-server localhost:9092

Kafka topic "orders" is ready to use.
## Step 2) Start Elasticsearch

#### - Install elasticsearch 8.5.3
$ wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-8.5.3-amd64.deb<br>
$sudo dpkg -i elasticsearch-8.5.3-amd64.deb<br>

#### - Setup network configuration for elasticsearch
Open file: <br>
$sudo nano /etc/elasticsearch/elasticsearch.yml<br>

- and set IP as localhost<br>
...<br>
network.host: 127.0.0.1<br>
...<br>

- and replace this setting with false<br>
...<br>
Enable security features<br>
xpack.security.enabled: false<br>
...<br>

$ sudo systemctl daemon-reload<br>
$ sudo systemctl enable elasticsearch.service<br>

#### - Start elasticsearch service
$ sudo systemctl start elasticsearch.service<br>

to test elastic service:<br>
curl -X GET 'http://localhost:9200'<br>

#### - Then we can create index

curl -XPUT 'http://localhost:9200/orders_index' -H 'Content-Type: application/json' -d ' <br>
{<br>
&nbsp;  "mappings": {<br>
&ensp;    "properties": {<br>
&emsp;      "main_name":  { "type": "keyword"},<br>
&emsp;      "appetizer_name":  { "type": "keyword"},<br>
&emsp;      "beverage_name":  { "type": "keyword"},<br>
&emsp;      "main_price":  { "type": "integer"},<br>
&emsp;      "appetizer_price":  { "type": "integer"},<br>
&emsp;      "beverage_price":  { "type": "integer"},<br>
&emsp;      "timestamp":  { "type": "date"}<br>
&ensp;   }<br>
&nbsp;  }<br>
}'<br>

Elasticsearch index is ready to write data.

## Step 3) Start Flask app (Producer)
Open a new terminal session and run:<br>
$ cd producer/<br>
$ flask run<br>

It will be working on: localhost:5000/ <br><br>
Now Flask App is ready. Go localhost:5000/ and order something :)
## Step 4) Start PySpark (Consumer)
Open a new terminal session and run:<br>
$ cd consumer/
$ spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.1 --jars elasticsearch-spark-30_2.12-8.5.3.jar consumer.py










