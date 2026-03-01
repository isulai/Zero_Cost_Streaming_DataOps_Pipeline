from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum, max, current_timestamp, desc

# Initialize Spark Session
spark = SparkSession.builder.getOrCreate()

# --- Configurations ---
silver_table_name = "zero_cost_streaming_dataops_pipeline.default.silver_covid_data"
gold_table_name = "zero_cost_streaming_dataops_pipeline.default.gold_covid_state_summary"
checkpoint_path = "/Volumes/zero_cost_streaming_dataops_pipeline/default/project_volume/checkpoints/gold_covid"

print("-------------------------------------------------------")
print(f"🏆 PHASE 3 START: Gold Insights Engine")
print(f"📅 Start Time: {spark.sql('SELECT current_timestamp()').collect()[0][0]}")
print("-------------------------------------------------------")

# LOG: Step 1 - Reading from Silver
print(f"[LOG] Step 1: Reading clean data from Silver Table: {silver_table_name}...")
silver_stream = spark.readStream.table(silver_table_name)

# LOG: Step 2 - Business Logic (Aggregation)
print(f"[LOG] Step 2: Calculating Latest Totals per State...")
# Since COVID data is cumulative, the "Total" is the max value recorded for each state
gold_df = (silver_stream
    .groupBy("state")
    .agg(
        max("cases").alias("total_confirmed_cases"),
        max("deaths").alias("total_deaths"),
        max("report_date").alias("last_updated_date")
    )
    .withColumn("gold_processed_at", current_timestamp())
)

# LOG: Step 3 - Writing to Gold
print(f"[LOG] Step 3: Writing Insights to Gold Delta Table...")
query = (gold_df.writeStream
    .format("delta")
    .outputMode("complete") # 'complete' is required for aggregations
    .option("checkpointLocation", checkpoint_path)
    .trigger(availableNow=True)
    .toTable(gold_table_name)
)

query.awaitTermination()

# FINAL VERIFICATION LOG
print("-------------------------------------------------------")
print(f"✅ PHASE 3 SUCCESS: Gold Insights are Ready!")
print(f"📊 Summary Table Created: {gold_table_name}")

# Show the Top 10 States by Deaths as a final "Gold" log
print("\n🔥 TOP 10 STATES BY TOTAL DEATHS (Final Insights):")
top_10 = spark.table(gold_table_name).orderBy(desc("total_deaths")).limit(10)
top_10.show()
print("-------------------------------------------------------")