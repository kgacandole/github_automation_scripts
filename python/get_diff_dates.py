from datetime import datetime

current_date = datetime.strptime(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")
print("Date #1: ", current_date)

date_string = "2023-04-12T12:07:02+0200"
compare_date = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S%z").replace(tzinfo=None)
print("Date #2: ", compare_date)

diff = current_date - compare_date
print("Number of days : ", diff.days)