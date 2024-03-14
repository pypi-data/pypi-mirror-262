# RedXClient

RedXClient is a client for the RedX server. It is written in Python and uses the `requests` and `pydantic` to communicate with the server and validate data.

It also returns the data as convenient Python objects.

## Installation

```bash
pip install redxclient
```

## Usage

```python
from redxclient import RedXClient

client = RedXClient(api_key="your_api_key")

parcel = client.get_parcel_details("parcel_id")
print(parcel)
```
