from urllib.request import urlopen as uReq
from urllib.request import Request
from bs4 import BeautifulSoup as soup
import time
import csv
import schedule
import sys


def HTTPer():
    # Establish HTTP and use BS4 to parse HTML
    try:
        uClient = Request(my_url, headers={'User-Agent': 'Mozzila/5.0'})
    except:
        print("An Error Occured")
    # Read HTML
    page_html = uReq(uClient).read()
    # Parse HTML
    page_soup = soup(page_html, "html.parser")
    return(page_soup)

def Tapper():
    Scores = []
    IDs = []

    page_soup = HTTPer()
    # Find items in the HTML
    mydivs = page_soup.findAll("div",{"class":"item"})

    mydivssearch = str(mydivs)
    items = mydivssearch.split(',')

    strSearch = "rating small"

    # Find rating within the div. 14, 15, 16 are the positions of the three digits of the rating.
    for item in items:
        if strSearch in item:
            Scores.append([item[item.find(strSearch)+14]+item[item.find(strSearch)+15]+item[item.find(strSearch)+16]])

    # Find IDs in divs.
    for div in mydivs:
        if div.get('id') != None:
            IDs.append(div.get('id').replace('checkin_',''))

        # Append everything to Scores
    for i in range(0, len(Scores)):
        Scores[i].append(IDs[i])
        Scores[i].append(time.strftime('%Y-%m-%d %H:%M'))
        Scores[i].append(beer_name)

    return(Scores)

def Write():

    try:
        scores = Tapper() #If this fails then scores wont be made so an error will be thrown later on.
    except:
        client.captureException()

    # Open data.csv
    reader = open('data.csv','r')
    toPlot = []

    flag=0

    for line in reader:
        if scores[0][1] in line:  # Check if latest data is already appended.
            flag=1
            print("Scanning for: "+beer_name+" at "+time.ctime()+" Status: NO NEW DATA")
            print("==============================================")
        theLine = line.split(",")
        if str(theLine[3]).lower().strip('\n') == str(beer_name).lower().strip('\n'):
            toPlot.append(theLine[0])

    if flag != 1: # If its new then write to csv
        print("Scanning for: "+beer_name+" at "+time.ctime()+" Status: NEW DATA FOUND - APPENDING...")
        print("==============================================")
        data = open('data.csv','a')
        with data:
            writer = csv.writer(data)
            writer.writerow(scores[0])


global my_url
global beer_name
beer_name = str(sys.argv[1])
beer_name = beer_name.replace("-"," ")
my_url = str(sys.argv[2])

Write()
