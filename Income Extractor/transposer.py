import csv
import datetime

# Load the CSV file
income_entries = []
with open("transactions.csv", "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        income_entries.append({
            "date": row["date"],
            "amount": float(row["amount"]),
            "comment": row["comment"],
        })

# Define the start and end dates
start_date = datetime.datetime.strptime("2022-10-10", "%Y-%m-%d")
end_date = datetime.datetime.strptime("2023-2-12", "%Y-%m-%d")

# Create a dictionary to store the amounts by date
amounts_by_date = {}
last_known_amount = None

# Loop over the dates
current_date = start_date
while current_date <= end_date:
    current_amount = last_known_amount
    for entry in income_entries:
        entry_date = datetime.datetime.strptime(entry["date"], "%d/%m/%Y")

        if entry_date == current_date:
            current_amount = entry["amount"]
            last_known_amount = entry["amount"]
    if current_amount is None:
        current_amount = last_known_amount
    amounts_by_date[current_date] = current_amount

    # Move to the next date
    current_date += datetime.timedelta(days=1)

# Write the data to a CSV file
with open("transactions2.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["date", "amount", "comment"])
    for date, amount in amounts_by_date.items():
        date_str = date.strftime("%d/%m/%Y")
        writer.writerow([date_str, amount, ""])
