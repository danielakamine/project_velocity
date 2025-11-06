import json
import subprocess
from pathlib import Path
import config
import os

BZID = os.getenv("BZID")

def run_curl_command(beacon_id, metric, output_file):
    cmd = [
        "curl", "--location", "--request", "GET",
        f"https://bluzone.io/portal/papis/v1/history/metric/88204?beaconId={beacon_id}&metric={metric}&interval=1m&endDate={config.END_TIME_STR}&startDate={config.START_TIME_STR}&includeZeros=false&format=json&merge=false",
        "--header", "BZID: (BZID)",
        "-o", str(output_file)
    ]
    subprocess.run(cmd, check=True, shell=False)

def load_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)
