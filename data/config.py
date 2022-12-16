import os
from dotenv import load_dotenv
load_dotenv()
EMAIl = str(os.getenv('EMAIl'))
PASSWORD = str(os.getenv('PASSWORD'))
MIN_DELAY = 1
MAX_DELAY = 5
DELAY = 20
