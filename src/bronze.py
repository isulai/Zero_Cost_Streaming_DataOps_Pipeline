from pyspark.sql import SparkSession

# Initialize Spark Session
spark = SparkSession.builder.getOrCreate()

# --- Configurations ---
# Pointing to your dedicated project catalog
bronze_table_name = "zero_cost_streaming_dataops_pipeline.default.bronze_covid_data"
checkpoint_path = "/Volumes/zero_cost_streaming_dataops_pipeline/default/project_volume/checkpoints/bronze_covid"

# Confluent Kafka Details
kafka_bootstrap_servers = "pkc-9q8rv.ap-south-2.aws.confluent.cloud:9092"
kafka_api_key = "U5VTD2QK2XK7ECZS"
kafka_api_secret = "cfltAf+X/4P3gXdRPVPwcfNdQa3ZYDwQveFitdEgGvnD9TF7GItMUZb+pP3mhUzg"
topic_name = "medallion_logs_topic"

print(f"Starting Bronze Ingestion from Kafka topic: {topic_name}...")

# 1. Read Raw Stream from Confluent Kafka
raw_stream = (spark.readStream
    .format("kafka")
    .option("kafka.bootstrap.servers", kafka_bootstrap_servers)
    .option("kafka.security.protocol", "SASL_SSL")
    .option("kafka.sasl.jaas.config", f"kafkashaded.org.apache.kafka.common.security.plain.PlainLoginModule required username='{kafka_api_key}' password='{kafka_api_secret}';")
    .option("kafka.sasl.mechanism", "PLAIN")
    .option("subscribe", topic_name)
    .option("startingOffsets", "earliest")
    .load()
)

# 2. Cast raw binary Kafka payload to String
# Kafka stores data as binary bytes, so we cast it to string to see the actual CSV row
bronze_df = raw_stream.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING) as raw_csv_payload", "timestamp")

# 3. Write to Bronze Delta Table (Using our Free-Tier Serverless Hack!)
query = (bronze_df.writeStream
    .format("delta")
    .outputMode("append")
    .option("checkpointLocation", checkpoint_path)
    .trigger(availableNow=True)  # <--- Bypasses continuous cluster costs!
    .toTable(bronze_table_name)
)

query.awaitTermination()
print(f"✅ Bronze Ingestion completed successfully! Data saved to {bronze_table_name}")