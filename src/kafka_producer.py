# Install the required Kafka library on the cluster
%pip install confluent-kafka

from confluent_kafka import Producer
import csv
import time

# --- Configurations ---
csv_file_path = "/Volumes/zero_cost_streaming_dataops_pipeline/default/project_volume/us-states.csv"

# Confluent Kafka Details
kafka_conf = {
    'bootstrap.servers': 'pkc-9q8rv.ap-south-2.aws.confluent.cloud:9092',
    'security.protocol': 'SASL_SSL',
    'sasl.mechanisms': 'PLAIN',
    'sasl.username': 'U5VTD2QK2XK7ECZS',
    'sasl.password': 'cfltAf+X/4P3gXdRPVPwcfNdQa3ZYDwQveFitdEgGvnD9TF7GItMUZb+pP3mhUzg'
}

topic_name = "medallion_logs_topic"
producer = Producer(kafka_conf)

def delivery_report(err, msg):
    """ Called once for each message produced to indicate delivery result. """
    if err is not None:
        print(f"Message delivery failed: {err}")

print(f"Starting to stream data from {csv_file_path} to topic: {topic_name}...")

# --- Read CSV and Publish to Kafka ---
try:
    with open(csv_file_path, 'r') as file:
        reader = csv.reader(file)
        header = next(reader) # Skip the header row
        
        count = 0
        for row in reader:
            # Convert the row list back into a comma-separated string
            message_value = ",".join(row)
            
            # Fire the message to Kafka
            producer.produce(topic_name, value=message_value.encode('utf-8'), callback=delivery_report)
            
            # Trigger any available delivery report callbacks
            producer.poll(0)
            
            count += 1
            if count % 100 == 0:
                print(f"Sent {count} records...")
                time.sleep(0.5) # Half-second delay to simulate real-time streaming
                
    # Wait for any outstanding messages to be delivered
    producer.flush()
    print(f"✅ Finished streaming! Total records sent: {count}")

except Exception as e:
    print(f"❌ Error reading file or connecting to Kafka: {e}")