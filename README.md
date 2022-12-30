# Start Kafka broker service

### Get Kafka
$ wget https://dlcdn.apache.org/kafka/3.3.1/kafka_2.13-3.3.1.tgz <br>
$ tar -xzf kafka_2.13-3.3.1.tgz<br>
$ cd kafka_2.13-3.3.1<br>


### Start the Kafka environment
NOTE: Your local environment must have Java 8+ installed.
Run the following commands in order to start all services in the correct order:

#### Start the ZooKeeper service
$ bin/zookeeper-server-start.sh config/zookeeper.properties
Open another terminal session and run:
#### Start the Kafka broker service
$ bin/kafka-server-start.sh config/server.properties

Once all services have successfully launched, you will have a basic Kafka environment running and ready to use. 

Create topic:<br>
$ bin/kafka-topics.sh --create --topic orders --bootstrap-server localhost:9092

# Start Flask app
Open a new terminal session and run:<br>
$ cd producer/<br>
$ flask run<br>

It will be working on: localhost:5000/

# Start Elasticsearch

### Install elasticsearch 8.5.3
$ wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-8.5.3-amd64.deb<br>
$sudo dpkg -i elasticsearch-8.5.3-amd64.deb<br>

### Setup network configuration for elasticsearch
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

### Start elasticsearch service
$ sudo systemctl daemon-reload<br>
$ sudo systemctl enable elasticsearch.service<br>
$ sudo systemctl start elasticsearch.service<br>

to test elastic service:<br>
curl -X GET 'http://localhost:9200'<br>

### Then we can create index

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

search data:
curl -X GET "localhost:9200/orders_index/_search?pretty"



https://serverfault.com/questions/699977/ubuntu-uninstall-elasticsearch
https://stackoverflow.com/questions/35921195/curl-52-empty-reply-from-server-timeout-when-querying-elastiscsearch
---------------------------------------------------------------------------
sudo systemctl start kibana





