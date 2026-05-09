import requests
import uuid
import random
import time
import sys

# Replace with your actual Cloud Run API URL
API_URL = "https://vote-api-108304418208.asia-southeast1.run.app/vote"

# Each group member uses a different node_id (1, 2, 3, or 4)
NODE_ID = int(sys.argv[1]) if len(sys.argv) > 1 else 1



