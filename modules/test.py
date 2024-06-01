import re
from database import *

# # Example string
# text = "ID: 22222 WEW >"

# # Using regular expression to extract the text after "ID:" without numbers
# match = re.search(r'ID:\s*(?:\d+\s*)?([^\d\s]+)', text)
# if match:
#     remaining_text = match.group(1)
#     print("Remaining text without numbers:", remaining_text)
# else:
#     print("No match found for remaining text")
db = DatabaseHandler('user_clients.db')
for i in db.fetch_user_packages_one(1,1):
    print(i['cost'])