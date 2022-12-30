import json

from flask import Flask, flash, redirect, render_template, request
from kafka import KafkaProducer

KAFKAS_SERVER = 

# Kafka Producer
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda x: json.dumps(x).encode('ascii')
)

# Configure application
app = Flask(__name__)
app.secret_key = 'super secret' # added for flash needs


@app.route("/", methods=["GET", "POST"])
def order():
    if request.method == "POST":

        # Get customer data
        main_dish = request.form.get("MainDish") # "steak_25"
        appetizer = request.form.get("Appetizer") # "soup_8"
        beverage = request.form.get("Beverage") # "coke_2"

        # Ensure something has ordered
        if  not (main_dish or appetizer or beverage):
            flash("Plaese Order Something")
            return redirect("/")

        # Prepare data for pushing to kafka producer
        data = {
            "main_dish": main_dish,
            "appetizer": appetizer,
            "beverage": beverage
        }

        # Push to kafka producer
        producer.send("orders", data)

        # Go back to homepage
        flash('Ordered!')
        return redirect("/")

    else:
        # Render homepage
        return render_template("index.html",)


