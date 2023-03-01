import json
import csv
import datetime
# Open the file
with open("economy.json", "r") as file:
    # Load the JSON data from file
    json_string = file.read()

# Parse the JSON string
data = json.loads(json_string)

# Get the transactions field from data
transactions = data["transactions"]

# Extract the entries with "comment" field set to "Income"
income_entries = [entry for entry in transactions if entry.get("comment", None) == "Income"]

# Get the start and end dates
start_date = datetime.datetime.strptime("22/10/10", "%y/%m/%d")
end_date = datetime.datetime.now()

# Create a dictionary to store the amounts by date
amounts_by_date = {}
last_known_amount = None

# Loop over the dates
current_date = start_date
while current_date <= end_date:
    current_amount = last_known_amount
    for entry in income_entries:
        entry_date = datetime.datetime.strptime(entry["timestamp"], "%Y-%m-%d")

        if entry_date == current_date:
            current_amount = entry["amount"]
            last_known_amount = entry["amount"]
    amounts_by_date[current_date] = current_amount

    # Move to the next date
    current_date += datetime.timedelta(days=1)

# Write the data to a CSV file
with open("transactions.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["date", "amount", "comment"])
    for entry in income_entries:
        entry_date = datetime.datetime.strptime(entry["timestamp"], "%Y-%m-%d")
        date_str = entry_date.strftime("%d/%m/%y")
        writer.writerow([date_str, entry["amount"], entry["comment"]])
