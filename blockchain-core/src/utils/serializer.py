   # src/utils/serializer.py

import json

class Serializer:
       @staticmethod
       def serialize(data):
           """Convert data to JSON format."""
           return json.dumps(data)

       @staticmethod
       def deserialize(data):
           """Convert JSON data back to Python object."""
           return json.loads(data)