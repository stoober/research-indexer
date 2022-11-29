from flask import Flask, render_template
from diophila import OpenAlex
import requests
import json

openalex = OpenAlex()

app = Flask(__name__)

def constructURL(pubISSN, fromDate):
	venue = requests.get(
		f'https://api.openalex.org/venues?filter=issn:{pubISSN}'
	).json()['results'][0]
	venueID = "host_venue.id:" + venue['id']
	
	endpoint = "works"

	filters = ",".join((
		venueID,
		"is_paratext:false",
		"type:journal-article",
		f"from_publication_date:{fromDate}"
	))

	sorting = "cited_by_count:desc"

	filtered_url = f'https://api.openalex.org/{endpoint}?filter={filters}&sort={sorting}'
	
	return filtered_url

# takes in URL and outputs studies + num of citations
def printer(filtered_url):
	toPrint = ""
	studiesReturned = requests.get(filtered_url).json()
	
	for c in studiesReturned['results']:
		toPrint = toPrint + c['title'] + " - " + str(c['cited_by_count']) + "\ntest\n"
	
	return toPrint

@app.route('/') 
def index():
	return render_template('index.html')

@app.route('/<issn>/<date>') 
def show(issn, date):
	outputText = printer(constructURL(issn, date))
	return render_template('output.html', output = outputText)
	
if __name__ == "__main__":
	app.run()
