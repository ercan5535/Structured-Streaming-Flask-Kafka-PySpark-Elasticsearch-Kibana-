from pyspark import SparkContext
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import StructType, StringType

# Create Schema
schema = (
        StructType()
        .add("main_dish", StringType())
        .add("appetizer", StringType())
        .add("beverage", StringType())
    )

# Create Spark Session
spark = SparkSession.builder.appName("StructuredStreaming").getOrCreate()
spark.sparkContext.setLogLevel('ERROR')

# Read data from Kafka topic
df = spark \
  .readStream \
  .format("kafka") \
  .option("kafka.bootstrap.servers", "127.0.0.1:9092") \
  .option("subscribe", "orders") \
  .option("startingOffsets", "earliest") \
  .load()

df.printSchema()
#root
# |-- key: binary (nullable = true)
# |-- value: binary (nullable = true)
# |-- topic: string (nullable = true)
# |-- partition: integer (nullable = true)
# |-- offset: long (nullable = true)
# |-- timestamp: timestamp (nullable = true)
# |-- timestampType: integer (nullable = true)

# Convert Vale byte format to string format
df = df.selectExpr("CAST(value AS STRING)", "timestamp")
# +--------------------+--------------------+
# |               value|           timestamp|
# +--------------------+--------------------+
# |{"main_dish": "ha...|2022-12-24 15:04:...|
# |{"main_dish": nul...|2022-12-24 15:04:...|

# Parse values from Json
df = df.select(from_json(col("value").cast("string"), schema).alias("parsed_value"), "timestamp")
# +--------------------+--------------------+
# |        parsed_value|           timestamp|
# +--------------------+--------------------+
# |{hamburger_15, so...|2022-12-24 15:04:...|
# |{null, null, coke_2}|2022-12-24 15:04:...|

# Parsed values with seperated columns
df = df.select("parsed_value.*", "timestamp")
# +------------+---------+--------+--------------------+
# |   main_dish|appetizer|beverage|           timestamp|
# +------------+---------+--------+--------------------+
# |hamburger_15|   soup_8|    null|2022-12-24 15:04:...|
# |        null|     null|  coke_2|2022-12-24 15:04:...|

# Process data to create price and name columns
# First split every column with name and price
# Split main_dish column as main_name and main_price
df = df.withColumn("main_name", when(df["main_dish"].isNull(), None)
                          .otherwise(split(df["main_dish"], "_").getItem(0)))
df = df.withColumn("main_price", when(df["main_dish"].isNull(), None)
                          .otherwise(split(df["main_dish"], "_").getItem(1)))

# Split appetizer column as appetizer_name and appetizer_price
df = df.withColumn("appetizer_name", when(df["appetizer"].isNull(), None)
                          .otherwise(split(df["appetizer"], "_").getItem(0)))
df = df.withColumn("appetizer_price", when(df["appetizer"].isNull(), None)
                          .otherwise(split(df["appetizer"], "_").getItem(1)))

# Split beverage column as beverage_name and beverage_price
df = df.withColumn("beverage_name", when(df["beverage"].isNull(), None)
                          .otherwise(split(df["beverage"], "_").getItem(0)))
df = df.withColumn("beverage_price", when(df["beverage"].isNull(), None)
                          .otherwise(split(df["beverage"], "_").getItem(1)))

# +------------+---------+--------+--------------------+---------+----------+--------------+---------------+-------------+--------------+
# |   main_dish|appetizer|beverage|           timestamp|main_name|main_price|appetizer_name|appetizer_price|beverage_name|beverage_price|
# +------------+---------+--------+--------------------+---------+----------+--------------+---------------+-------------+--------------+
# |hamburger_15|   soup_8|    null|2022-12-24 15:04:...|hamburger|        15|          soup|              8|         null|          null|
# |        null|     null|  coke_2|2022-12-24 15:04:...|     null|      null|          null|           null|         coke|             2|

# Drop initial columns and get only name, price and timestamp columns
df_final = df.drop("main_dish", "appetizer", "beverage")
# +--------------------+---------+----------+--------------+---------------+-------------+--------------+
# |           timestamp|main_name|main_price|appetizer_name|appetizer_price|beverage_name|beverage_price|
# +--------------------+---------+----------+--------------+---------------+-------------+--------------+
# |2022-12-24 15:04:...|hamburger|        15|          soup|              8|         null|          null|
# |2022-12-24 15:04:...|     null|      null|          null|           null|         coke|             2|

# Write to consol
query = \
    df_final \
    .writeStream \
    .format("console") \
    .outputMode("append") \
    .trigger(processingTime="5 seconds") \
    .start()


# Write to elasticsearch
query = df_final.writeStream \
    .outputMode("append") \
    .format("org.elasticsearch.spark.sql") \
    .option("checkpointLocation", "tmp/") \
    .option("es.resource", "orders_index") \
    .option("es.nodes", "localhost") \
    .option("es.port", "9200") \
    .start()

#.option("checkpointLocation", "/tmp/") \
query.awaitTermination()


