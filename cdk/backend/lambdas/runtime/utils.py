from decimal import Decimal
import json

class DecimalEncoder(json.JSONEncoder):
  def default(self, obj):
    if isinstance(obj, Decimal):
      return str(obj)
    return json.JSONEncoder.default(self, obj)
  
  # Convert nested DynamoDB attribute types to Python data types
def convert_to_python(data):
    if isinstance(data, dict):
        if "S" in data:
            return data["S"]
        elif "N" in data:
            return int(data["N"]) if data["N"].isdigit() else float(data["N"])
        elif "L" in data:
            return [convert_to_python(item) for item in data["L"]]
        elif "M" in data:
            return {key: convert_to_python(value) for key, value in data["M"].items()}
    return data
