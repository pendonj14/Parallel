from google.cloud import pubsub_v1, firestore
from flask import Flask
import json
import threading
import time
import os

app = Flask(__name__)

project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
subscription_id = "vote-sub"

subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(project_id, subscription_id)
db = firestore.Client(database="pendon-chavo-atilano-yap")

vote_count = 0
start_time = time.time()

@app.route("/")
def health():
    return "Worker is running", 200

def process_vote(message):
    global vote_count
    try:
        vote = json.loads(message.data.decode("utf-8"))
        
        # Measure latency
        received_time = time.time()
        created_time = vote.get("timestamp", received_time)
        latency = received_time - created_time
        
        # Idempotent write
        doc_id = f"{vote['user_id']}_{vote['poll_id']}"
        
        # Add processing metadata
        vote["processed_at"] = received_time
        vote["latency_seconds"] = round(latency, 4)
        
        db.collection("votes").document(doc_id).set(vote)
        
        vote_count += 1
        elapsed = received_time - start_time
        throughput = vote_count / elapsed if elapsed > 0 else 0
        
        print(f"Processed: {vote['user_id'][:8]}... | Choice: {vote['choice']} | Latency: {latency:.4f}s | Total: {vote_count} | Throughput: {throughput:.2f} votes/sec")
        
        message.ack()
    except Exception as e:
        print(f"Error processing vote: {e}")
        message.nack()

def start_worker():
    print("Worker started. Listening for votes...")
    streaming_pull = subscriber.subscribe(subscription_path, callback=process_vote)
    try:
        streaming_pull.result()
    except Exception as e:
        print(f"Worker error: {e}")

worker_thread = threading.Thread(target=start_worker, daemon=True)
worker_thread.start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
