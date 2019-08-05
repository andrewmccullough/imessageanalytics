import datetime
import csv
import re

############
# SETTINGS #
############

input_file = "in.csv"
output_file = "out.csv"
include_reacts = True

##########
# SCRIPT #
##########

# regular expression to identify reactions (versus text and photo messages)
pattern = re.compile("Liked “.*”|Emphasized “.*”|Laughed at “.*”|Disliked “.*”|Loved “.*”")

f = open(input_file)

counts = {}
people = {}
total = 0

i = datetime.datetime(2018, 5, 1, 0, 0, 0)     # TODO : self identify initial date

while i != datetime.datetime(2019, 3, 15, 0, 0, 0):     # TODO : up to today
	counts[datetime.datetime.strftime(i, "%Y-%m-%d")] = [0, 0]  # 0 incoming, 0 outgoing
	i += datetime.timedelta(days = 1)

for line in f:
	try:
		array = line.split(",")
		# [0] date sent  [1] date delivered  [2] date read  [3] service  [4] type  [5] sender ID  [6] sender name  [7] status  [8] subject  [9] message text  [10] attachments  [11] attachment type

		obj = datetime.datetime.strptime(array[0], "%Y-%m-%d %H:%M:%S")
		date = datetime.datetime.strftime(obj, "%Y-%m-%d")

		if array[4] == "Incoming":
			counts[date][0] += 1
			total += 1
		elif array[4] == "Outgoing":
			counts[date][1] += 1
			total += 1

		match = pattern.fullmatch(array[9])
		if match:
			# reaction
			pass
		else:
			# message
			# pass

			if array[6] in people:
				people[array[6]] += 1
			else:
				people[array[6]] = 0

	except Exception as e:
		print(e)
		continue

f.close()

f = open("out.csv", "w")
writer = csv.writer(f)

# writer.writerow(["Date", "Incoming", "Outgoing", "Both"])
# for date, count in counts.items():
# 	writer.writerow([date, count[0], count[1], count[0] + count[1]])

writer.writerow(["Name", "Messages Sent"])
for person, count in people.items():
	writer.writerow([person, count])

print(total)
f.close()
