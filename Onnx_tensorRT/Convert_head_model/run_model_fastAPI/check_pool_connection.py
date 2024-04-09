import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

# Define the base URL of your API server
base_url = "http://0.0.0.0:5000"

# Define a function to create a session with connection pooling
def create_session():
    session = requests.Session()
    retries = Retry(total=5, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
    adapter = HTTPAdapter(pool_connections=10, pool_maxsize=10, max_retries=retries)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session


process_id = "604ef817ef7c20fc5e52a20d"
# Create a session with connection pooling
session = create_session()

# Define the endpoint URL
endpoint = "/yolov5/predict/share_memory"

# Define the data to be sent in the request
data = {"share_key": process_id}

# Send POST request to the endpoint using the session
response = session.post(base_url + endpoint, json=data)

# Process the response
print(response.json())

# Close the session
session.close()