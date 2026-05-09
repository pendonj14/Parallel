import requests
import uuid
import random
import time
import sys

# Replace with your actual Cloud Run API URL
API_URL = "https://vote-api-108304418208.asia-southeast1.run.app/vote"

# Each group member uses a different node_id (1, 2, 3, or 4)
NODE_ID = int(sys.argv[1]) if len(sys.argv) > 1 else 1

def generate_vote():
    return {
        "user_id": str(uuid.uuid4()),
        "poll_id": "poll_1",
        "choice": random.choice(["A", "B", "C"]),
        "edge_id": f"node_{NODE_ID}",
        "timestamp": time.time()
    }


def send_vote(vote, retries=3):
    for attempt in range(retries):
        try:
            response = requests.post(API_URL, json=vote)
            if response.status_code == 200:
                print(f"[Node {NODE_ID}] Vote sent: {vote['user_id'][:8]}... | Choice: {vote['choice']}")
                return True
            else:
                print(f"[Node {NODE_ID}] Server error: {response.status_code}")
        except Exception as e:
            print(f"[Node {NODE_ID}] Attempt {attempt+1} failed: {e}")
            time.sleep(1)
    return False

def run_edge_node():
    print(f"Edge Node {NODE_ID} started. Sending votes...")
    vote_count = 0
    while True:
        vote = generate_vote()
        send_vote(vote)
        vote_count += 1
        print(f"[Node {NODE_ID}] Total votes sent: {vote_count}")
        time.sleep(random.uniform(1, 3))

if __name__ == "__main__":
    run_edge_node()