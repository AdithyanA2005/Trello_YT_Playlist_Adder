import json
import requests


def print_available_lists(lists):
    if len(lists) > 0:
        print("The available lists are:")
    else:
        print("There are no available lists")

    for i in range(len(lists)):
        # This will give index prefix with zeroes (1 -> 001)
        zero_filled_index = str(i).zfill(3)

        list_id = lists[i]["id"]
        list_name = lists[i]["name"]

        print(f"\t{zero_filled_index} - {list_id} - {list_name}")


def select_new_or_existing_list(trello_board, lists):
    def opt_for_new_or_existing():
        while True:
            option = "new"

            # Add option for selecting a existing list if any exists
            if len(lists) > 0:
                print("\nDo you want to select a new list or an existing list:")
                print("\t0 - New List")
                print("\t1 - Existing List")
                usr_inp = input("\tEnter Option: ")

                # User entered a invalid value
                if usr_inp not in ["0", "1"]:
                    print("\tINVALID OPTION ENTERED")
                    continue

                # Set option according to user input
                if usr_inp == "0":
                    option = "new"
                else:
                    option = "existing"

            # Show conformation message according to user input
            if option == "new":
                print("\nProceed to create a new list:")
            else:
                print("\nProceed to select an existing list:")

            # Take user conformation
            if input("\tEnter (y/n): ").lower() == "y":
                return option
            else:
                continue

    def create_new_list():
        while True:
            print("\nCreate a new list:")
            list_name = input("\tEnter list name: ")

            if input(f"\tCreate list with name - '{list_name}' (y/n): ").lower() == "y":
                break

        list = trello_board.create_list(list_name)
        return list

    def select_existing_list():
        while True:
            print("\nSelect a existing list:")
            list_index = input("\tEnter list index: ")
            list_name = lists[int(list_index)]["name"]

            if not list_index.isdigit() or not int(list_index) in range(0, len(lists)):
                print("\tINVALID OPTION ENTERED")
                continue

            if input(f"\tSelect list with name - '{list_name}' (y/n): ").lower() == "y":
                break

        list = lists[int(list_index)]
        return list

    usr_opt = opt_for_new_or_existing()

    if usr_opt == "new":
        list = create_new_list()
    else:
        list = select_existing_list()

    return list


def add_videos_to_list(trello_board, videos, list):
    list_id = list["id"]

    for video in videos:
        video_title = video["title"]
        video_url = f"https://www.youtube.com/watch?v={video['id']}"

        trello_board.create_card(list_id, video_url)
        print(f"Added - {video_title}")


class TrelloBoard:
    trello_base_url = "https://api.trello.com/1"

    def __init__(self, trello_api_key, trello_api_token, trello_board_id):
        self.api_key = trello_api_key
        self.api_token = trello_api_token
        self.board_id = trello_board_id
        self.headers = {"Accept": "application/json"}
        self.query = {
            "key": "0252e272f6e88da8a055b5bac40d5f7b",
            "token": "ATTA80783096968093c6dea798d351c54d05c3a5e98d03da219d19bc76cf50647f94091B4BB0",
        }

    def __trello_url(self, url):
        # This private function will prefix any giver url with the base url
        return f"{self.trello_base_url}{url}"

    def get_lists(self):
        url = self.__trello_url(f"/boards/{self.board_id}/lists")
        response = requests.get(url, headers=self.headers, params=self.query)
        lists = json.loads(response.text)
        lists = [list for list in lists if not list["closed"]]
        return lists

    def create_list(self, list_name):
        url = self.__trello_url(f"/boards/{self.board_id}/lists")
        query = {"name": list_name, **self.query}
        response = requests.post(url, headers=self.headers, params=query)
        list = json.loads(response.text)
        return list

    def create_card(self, idList, urlSource):
        url = self.__trello_url("/cards")
        query = {"idList": idList, "urlSource": urlSource, **self.query}
        response = requests.post(url, headers=self.headers, params=query)
        return response.status_code
