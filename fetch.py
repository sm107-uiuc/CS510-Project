import subprocess
import json

def call_api(queries):
    result = subprocess.run(["node", "get_data_cdl.js"] + queries, capture_output=True, text=True)
    output = json.loads(result.stdout)
    return output


if __name__ == "__main__":
    keywords = ['machine_learning', 'ethereum']
    out = call_api(keywords)
    print("Printing in Python file")
    print(out)