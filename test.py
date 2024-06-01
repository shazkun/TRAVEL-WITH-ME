import re

# Example string
text = "ID:12 wew: 12"

# Using regular expression to extract the ID number
match = re.search(r'ID:\s*(\d+)', text)
if match:
    id_number = match.group(1)
    print("ID number:", id_number)
else:
    print("ID number not found")
