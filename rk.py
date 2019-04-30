from bs4 import BeautifulSoup
import urllib2

AntonLink = urllib2.urlopen("https://runkeeper.com/user/AntonBjornNilsson/fitnessReports/cardio").read()
SandiLink = urllib2.urlopen("https://runkeeper.com/user/2017342092/fitnessReports/cardio").read()
OliverLink = urllib2.urlopen("https://runkeeper.com/user/2967459810/fitnessReports/cardio").read()

soup = BeautifulSoup(AntonLink,'html.parser')
#text_array = soup.find_all('text')
print(soup.text)

