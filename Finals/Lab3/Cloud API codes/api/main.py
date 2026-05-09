from flask import Flask, request, jsonify
from google.cloud import pubsub_v1
import json
import os

app = Flask(__name__)

project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
topic_id = "vote-topic"
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)

@app.route("/vote", methods=["POST"])
def receive_vote():
    vote = request.get_json()

    # Validate incoming vote
    if not vote or "user_id" not in vote or "poll_id" not in vote or "choice" not in vote:
        return {"error": "Invalid payload"}, 400

    try:
        # Publish validated vote to Pub/Sub
        data = json.dumps(vote).encode("utf-8")
        publisher.publish(topic_path, data)
        print(f"Vote received: {vote['user_id']} | Choice: {vote['choice']}")
        return {"status": "accepted"}, 200
    except Exception as e:
        return {"error": str(e)}, 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
