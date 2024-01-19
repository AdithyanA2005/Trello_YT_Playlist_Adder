from env import TRELLO_API_KEY
from env import TRELLO_BOARD_ID
from env import TRELLO_API_TOKEN
from trello import TrelloBoard
from trello import print_available_lists
from trello import select_new_or_existing_list
from trello import add_videos_to_list
from scraper import fetch_playlist_videos


# Create a trello baord instance
trello_board = TrelloBoard(
    trello_api_key=TRELLO_API_KEY,
    trello_api_token=TRELLO_API_TOKEN,
    trello_board_id=TRELLO_BOARD_ID,
)

# Get the list of open lists in the board
lists = trello_board.get_lists()

# Print available lists and a index for it
print_available_lists(lists)

# Ask user whether to add to a new list or a existing list
selected_list = select_new_or_existing_list(trello_board, lists)

# Fetch all the videos in a public/unlisted playlist
playlist_url = input("\nEnter playlist url: ")
print("Fetching list of videos, this may take some time...")
videos = fetch_playlist_videos(playlist_url)

# Add playlist videos to the trello list
add_videos_to_list(trello_board, videos, selected_list)
