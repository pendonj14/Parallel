# Distributed Voting System with Edge–Cloud Architecture and Fault Tolerance

## CS323 - Second Laboratory Activity for Final Term

---

## System Overview

This project implements a **Distributed Voting System** using Google Cloud Platform (GCP). The system follows an event-driven architecture where multiple edge nodes generate votes independently, and cloud services handle ingestion, messaging, processing, and storage. The system is designed to remain functional even when failures occur in either edge or cloud components.

### Architecture

```
Edge Node 1 (Member 1) ─┐
Edge Node 2 (Member 2) ─┤──→ Cloud Run API ──→ Pub/Sub (vote-topic) ──→ Worker Service ──→ Firestore
Edge Node 3 (Member 3) ─┤        (vote-api)       (vote-sub)             (vote-worker)     (votes collection)
Edge Node 4 (Member 4) ─┘
```

### Component Breakdown

- **Edge Nodes** — Python scripts simulating distributed user devices. Each node independently generates votes with unique user IDs, a poll selection, and timestamps. Nodes include retry logic to handle unreliable network conditions.
- **Cloud Run API (`vote-api`)** — A lightweight Flask-based REST API deployed on Cloud Run. It receives votes via HTTP POST, validates the payload, and publishes the data to Pub/Sub. It is stateless and does not perform any processing or storage.
- **Pub/Sub (`vote-topic` / `vote-sub`)** — Google Cloud Pub/Sub serves as the asynchronous messaging layer. It decouples the ingestion API from the worker service, enabling fault-tolerant message delivery and buffering during worker downtime.
- **Worker Service (`vote-worker`)** — A Cloud Run service that subscribes to Pub/Sub, processes each vote, and writes it to Firestore. It uses idempotent document IDs (`user_id_poll_id`) to prevent duplicate entries. It also tracks processing latency and throughput.
- **Firestore** — A NoSQL document database in Native Mode that serves as the final persistent storage layer. Each processed vote is stored as an individual document in the `votes` collection.

---

## Setup and Execution Instructions

### Prerequisites

- Google Cloud Platform account with billing enabled
- Python 3.x installed on local machines or GitHub Codespaces
- `requests` Python library (`pip install requests`)

### Step 1: GCP Project Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create a new project named `cs323-voting-system-groupX`
3. Enable the following APIs under **APIs & Services → Library**:
   - Cloud Run API
   - Cloud Pub/Sub API
   - Cloud Firestore API

### Step 2: Firestore Database

1. Navigate to **Firestore** in the console
2. Click **Create Database**
3. Select **Native Mode**
4. Choose region: `asia-southeast1`

### Step 3: Pub/Sub Configuration

1. Go to **Pub/Sub → Topics** → Create topic: `vote-topic`
2. Create a subscription: `vote-sub` with **Pull** delivery type

### Step 4: Deploy Cloud Run API

Open **Cloud Shell** and run:

```bash
mkdir -p ~/voting-system/api && cd ~/voting-system/api
```

Create `main.py`, `requirements.txt`, and `Dockerfile` (see `/api` folder in this repo), then deploy:

```bash
gcloud run deploy vote-api \
  --source . \
  --region asia-southeast1 \
  --allow-unauthenticated \
  --set-env-vars GOOGLE_CLOUD_PROJECT=$(gcloud config get-value project)
```

### Step 5: Deploy Worker Service

```bash
mkdir -p ~/voting-system/worker && cd ~/voting-system/worker
```

Create `main.py`, `requirements.txt`, and `Dockerfile` (see `/worker` folder in this repo), then deploy:

```bash
gcloud run deploy vote-worker \
  --source . \
  --region asia-southeast1 \
  --no-allow-unauthenticated \
  --set-env-vars GOOGLE_CLOUD_PROJECT=$(gcloud config get-value project) \
  --min-instances=1
```

### Step 6: Run Edge Nodes

Each group member runs the edge node script with their assigned node number:

```bash
pip install requests
python edge_node.py 1   # Member 1
python edge_node.py 2   # Member 2
python edge_node.py 3   # Member 3
python edge_node.py 4   # Member 4
```

### Step 7: Verify in Firestore

Go to **Firestore → votes collection** to see processed votes appearing in real time.

---

## Deployed Cloud Run API Endpoint

```
https://vote-api-108304418208.asia-southeast1.run.app/vote
```

---

## Performance Evaluation Summary

### End-to-End Latency

| Condition | Observed Latency |
|---|---|
| Normal operation | 1–5 seconds |
| After worker recovery | 300–339 seconds (queued votes) |

During normal operation, votes generated at the edge reached Firestore within a few seconds. When the worker was disabled and later restored, queued votes showed latencies of 300–339 seconds, representing the time they spent buffered in Pub/Sub.

### Fault Tolerance Results

| Test | Observation |
|---|---|
| Message duplication (3x per vote) | No duplicate documents in Firestore — idempotent writes worked correctly |
| Worker failure (scaled to 0) | API and Pub/Sub continued operating; Firestore updates paused |
| Worker recovery (scaled back to 1) | All queued votes processed automatically without manual intervention |

### Consistency Evaluation

After all tests, the number of unique documents in Firestore matched the number of unique votes generated at the edge nodes. Even with intentional duplicate transmissions and worker downtime, the system achieved eventual consistency.

---

## Individual Reflections

### Joseph Pendon

During this activity, I observed clear differences between sequential and distributed execution. In a sequential system, votes would be generated, transmitted, and processed one at a time in a predictable and linear order. In our distributed setup, four edge nodes operated independently, each generating votes at random intervals between one and three seconds. This meant that votes arrived at the Cloud Run API in an unpredictable order and at varying rates, which is exactly how real-world distributed systems behave when multiple clients interact with a shared backend.

One of the most significant observations was during the worker failure test. When the worker service was scaled down to zero instances, the edge nodes continued sending votes without encountering any errors. The Cloud Run API kept accepting requests, and Pub/Sub continued buffering incoming messages. Firestore stopped receiving new documents during this period, but no votes were lost. Once the worker was restored, it automatically reconnected to Pub/Sub and began processing all the queued messages. The recovered votes showed latencies of 300 to 339 seconds, representing the time they had spent waiting in the Pub/Sub queue. This experience demonstrated how message persistence provides fault tolerance without requiring any manual recovery or replay logic.

The duplication test was equally revealing. When each vote was intentionally transmitted three times from the edge node, the worker processed all three copies. However, Firestore only stored one document per unique vote because the document ID was constructed as a combination of the user ID and poll ID, making every write idempotent. This confirmed that even with duplicate messages flowing through the pipeline, the final state in Firestore remained consistent and correct.

The most challenging part of the activity was configuring IAM permissions in GCP. The worker service initially failed with "permission denied" errors because the default compute service account did not have the necessary roles for Pub/Sub consumption and Firestore writes. Debugging this required reading Cloud Run logs, identifying the specific missing permissions, and granting the correct IAM roles. This experience highlighted how distributed systems introduce operational complexity that goes beyond writing application code — proper configuration and infrastructure management are equally important.

In terms of trade-offs, Pub/Sub added significant reliability by decoupling the API from the worker, but it also introduced additional latency since every vote had to pass through a message queue before reaching Firestore. Cloud Run provided automatic scaling and deployment convenience, but the worker occasionally required redeployment to pick up configuration changes. Edge computing distributed the vote generation load across multiple independent sources, reducing pressure on any single node, but it also introduced variability and required network communication that a purely local system would not need. Overall, this activity reinforced that distributed systems offer powerful advantages in fault tolerance and scalability, but they require careful attention to permissions, asynchronous behavior, and system-level debugging.


