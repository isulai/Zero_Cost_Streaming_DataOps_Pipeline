from pyspark.sql import SparkSession
from pyspark.sql.functions import col, split, current_timestamp

# Initialize Spark Session
spark = SparkSession.builder.getOrCreate()

# --- Configurations ---
bronze_table_name = "zero_cost_streaming_dataops_pipeline.default.bronze_covid_data"
silver_table_name = "zero_cost_streaming_dataops_pipeline.default.silver_covid_data"
checkpoint_path = "/Volumes/zero_cost_streaming_dataops_pipeline/default/project_volume/checkpoints/silver_covid"

print("-------------------------------------------------------")
print(f"🚀 PHASE 2 START: Silver Transformation Engine")
print(f"📅 Start Time: {current_timestamp}")
print("-------------------------------------------------------")

# LOG: Step 1 - Reading Data
print(f"[LOG] Step 1: Connecting to Bronze Table: {bronze_table_name}...")
bronze_stream = spark.readStream.table(bronze_table_name)

# LOG: Step 2 - Transformation Logic
print(f"[LOG] Step 2: Applying Schema Mapping (Date, State, FIPS, Cases, Deaths)...")
# Mapping exactly to your sample: 2020-03-22,North Dakota,38,30,0
silver_df = (bronze_stream
    .withColumn("temp_array", split(col("raw_csv_payload"), ","))
    .select(
        col("temp_array").getItem(0).cast("date").alias("report_date"),
        col("temp_array").getItem(1).alias("state"),
        col("temp_array").getItem(2).alias("fips_code"),
        col("temp_array").getItem(3).cast("int").alias("cases"),
        col("temp_array").getItem(4).cast("int").alias("deaths"),
        col("timestamp").alias("kafka_ingestion_time"),
        current_timestamp().alias("silver_processed_at")
    )
    .filter(col("report_date").isNotNull())
)

# LOG: Step 3 - Writing to Delta
print(f"[LOG] Step 3: Writing Stream to Silver Delta Table...")
print(f"[LOG] Checkpoint Path: {checkpoint_path}")

query = (silver_df.writeStream
    .format("delta")
    .outputMode("append")
    .option("checkpointLocation", checkpoint_path)
    .trigger(availableNow=True) 
    .toTable(silver_table_name)
)

query.awaitTermination()

# FINAL VERIFICATION LOG
print("-------------------------------------------------------")
print(f"✅ PHASE 2 SUCCESS: Silver Layer is Populated!")
silver_count = spark.table(silver_table_name).count()
print(f"📊 Total Records Cleaned and Loaded: {silver_count}")
print("-------------------------------------------------------")