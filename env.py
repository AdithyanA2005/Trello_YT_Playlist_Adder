import os
from dotenv import load_dotenv

# Load variables from the .env file
load_dotenv()

TRELLO_BOARD_ID = os.getenv("TRELLO_BOARD_ID")
TRELLO_API_KEY = os.getenv("TRELLO_API_KEY")
TRELLO_API_TOKEN = os.getenv("TRELLO_API_TOKEN")

