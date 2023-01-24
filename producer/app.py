import json
import os
import time

from flask import Flask, flash, redirect, render_template, request
from kafka import KafkaProducer

time.sleep(120)
# Get Enviroment variables for Kafka connection
KAFKA_BROKER_URL = os.environ.get('KAFKA_BROKER_URL')
KAFKA_TOPIC_NAME = os.environ.get('KAFKA_TOPIC_NAME')

#KAFKA_BROKER_URL = "localhost:9092"
#KAFKA_TOPIC_NAME = "orders"

# Kafka Producer
producer = KafkaProducer(
    bootstrap_servers=[KAFKA_BROKER_URL],
    value_serializer=lambda x: json.dumps(x).encode('ascii')
)

# Configure application
app = Flask(__name__)
app.secret_key = 'super secret'  # added for flash needs

@app.route("/", methods=["GET", "POST"])
def order():
    if request.method == "POST":

        # Get customer data
        main_dish = request.form.get("MainDish")  # "steak_25"
        appetizer = request.form.get("Appetizer")  # "soup_8"
        beverage = request.form.get("Beverage")  # "coke_2"

        # Ensure something has ordered
        if not (main_dish or appetizer or beverage):
            flash("Plaese Order Something")
            return redirect("/")

        # Prepare data for pushing to kafka producer
        data = {
            "main_dish": main_dish,
            "appetizer": appetizer,
            "beverage": beverage
        }

        # Push to kafka producer
        producer.send(KAFKA_TOPIC_NAME, data)

        # Go back to homepage
        flash('Ordered!')
        return redirect("/")

    else:
        # Render homepage
        return render_template("index.html")
    

if __name__ == "__main__":
    app.run(debug=True)
