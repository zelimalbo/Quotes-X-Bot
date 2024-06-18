import schedule # type: ignore
import time
import subprocess
import os
from dotenv import load_dotenv # type: ignore

# Load environment variables from .env file if not in Docker
if os.getenv('ISDOCKER') != "true":
    load_dotenv()


# Global variables
file_path = None

# Function to generate file
def get_file_to_serve():
    global file_path
    result = subprocess.run(['python3', './ehb_modules/generate_file.js'], capture_output=True, text=True)
    if result.returncode != 0:
        raise SystemExit('File generator module has encountered an error! EHB will now close.')
    file_path = result.stdout.strip()

def get_payload():
    get_file_to_serve()
    return file_path

def run_job():
    timestamp = int(time.time() * 1000)  # UNIX time in milliseconds
    print('Starting new run at UNIX time ' + str(timestamp))
    file_payload = get_payload()
    if os.getenv('USE_TWITTER') == "true":
        subprocess.Popen(['python3', 'C:\\CS\\Python\\xBot\\xBot.py'], stdin=subprocess.PIPE).communicate(input=file_payload.encode())

if os.getenv('DEBUG_MODE') == "true":
    print('!!!!!!DEBUG MODE ON --- BYPASSING TIMER AND EXITING AFTER EXECUTION!!!!!!')
    run_job()
else:
    # Schedule the job to run every hour at the 0th minute
    schedule.every(10).seconds.do(run_job)

    while True:
        schedule.run_pending()
        time.sleep(1)  # Wait a second before checking the schedule again
