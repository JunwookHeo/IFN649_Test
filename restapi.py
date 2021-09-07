import time

######################################################################
## REST API Test
## Read data from a server
import requests
import json

def readFromServer():
	url_items = "https://jsonplaceholder.typicode.com/posts"
	response = requests.get(url_items)

	print(response.text)
	print(len(response.json()))
	for i, r in enumerate(response.json()):
		print(i, r["title"])
		time.sleep(1)
		# TODO: Prepocess and send data to MQTT at this point


#######################################################################
## Read data from csv file
import csv
def readFromFile():
	with open('weather.csv') as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		line_count = 0
		for row in csv_reader:
			if line_count == 0: # Display column name
				print(f'Column names are {", ".join(row)}')
				line_count += 1
			else: # Display data
				print(f'\tDate:{row[1]}, City : {row[5]}, Avg Temperature:{row[9]}')
				line_count += 1
			# TODO: Prepocess and send data to MQTT at this point
			time.sleep(1)

		print(f'Processed {line_count} lines.')

def main():
	#readFromServer()
	readFromFile()

if __name__ == '__main__':
	main()