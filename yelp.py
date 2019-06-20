# -*- coding: utf-8 -*-
"""
Created on June 20 2019
@author: Hugo Iriarte
"""

#IMPORTS
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import os
import csv
from datetime import datetime


#Chromedriver Path
desktop = os.path.join(os.environ['USERPROFILE'], 'Desktop') 
chromedriver = desktop + '/chromedriver'

#Make directory to save CSV
newPath = os.path.join(desktop, 'Yelp-Scrape')
try:
    os.mkdir(newPath)
except FileExistsError:
    pass

def main():
    """
    Main function that first navigates to retreive every city & town in the U.S.
    Then navigates to YELP quering through the URL
    Program retreives Company Names and their phone number
    """
    foundDriver = True
    #Initiate Driver & Navigate to get all cities and towns in the U.S.
    try:
        driver = webdriver.Chrome(chromedriver)
    except:
        print('#========================================================')
        input('# "Chromedriver" executable needs to be in PATH (User Desktop).\n#Please see https://sites.google.com/a/chromium.org/chromedriver/home to download\nEnter any key to quit\n#========================================================')
        exit()
        foundDriver = False
    
    if foundDriver == True:
        print('#===================================')
        print('# Do not close the chrome window')
        print('# If you see the current website visually fully loaded you can click the X button to force stop loading\n# Everything we need to scrape is already on the screen')
        print('#===================================')
        driver.get('https://www.britannica.com/topic/list-of-cities-and-towns-in-the-United-States-2023068')
        #State is the Key and Values are list of city/towns
        dictionary = {}
        length = len(dictionary)
        theRange = list(range(326620, 326670))
        #States   
        sName = driver.find_elements_by_class_name('h1')
        for i in range(len(sName)):
            #Append state as Key and Cities & Towns for 
            dictionary[sName[i].text] = [x.text for x in driver.find_elements_by_css_selector('#ref' + str(theRange[i]) + '> ul > li')]
        print('\nNext step, Yelp.')
        #YELP
        url = 'https://www.yelp.com/search?find_desc=Massage%20Therapy&find_loc=' #Change Veterinarians to what ever you're looking for

        #Lists holding companies data
        company = []
        phone = []
        state = []
        city = []
        print('\n')
        print('This will take a very very long time. Once counter reaches ' + str(length) + ', program is done.\n')
        counterReach = 1
        for x,y in dictionary.items():
            print(counterReach)
            for v in y:
                yelpURL = url + x.lower() + '%2C%20' + v.lower() + '&cflt=massage_therapy'# If you're not using this for vets remove the filter '&cflt=vet' or add your own filter
                #User output
                print('#========================')
                print('# STATE: ' + x)
                print('# CITY: ' + v)

                driver.get(yelpURL)
                dataOnPage = True
                try:
                    pages = int(driver.find_element_by_xpath('//*[@id="wrap"]/div[3]/div[2]/div[2]/div/div[1]/div[1]/div/div[1]/div/div[1]/span').text.split(' ')[-1])
                except:
                    print('# No Data on Page') #If no data is on page(No Vet in this city) loop is done
                    dataOnPage = False       
                if dataOnPage == True:
                    print('# PAGES: ' + str(pages))
                    counter = 0
                    print('#========================')
                    for page in range(pages - 1):#Loop through each page within city and append
                        try:           
                            c = driver.find_elements_by_xpath('//*[@id="wrap"]/div[3]/div[2]/div[2]/div/div[1]/div[1]/div/ul/li/div/div/div[1]/div[2]/div/div[1]/div[1]/div[1]/h3/a')
                        except:
                            print('#######################################################################')
                            print('No Company Names')
                            print('#######################################################################')
                        try:
                            p = driver.find_elements_by_xpath('//*[@id="wrap"]/div[3]/div[2]/div[2]/div/div[1]/div[1]/div/ul/li/div/div/div[1]/div[2]/div/div[2]/div/div[1]')
                        except:
                            print('#######################################################################')
                            print('No Phone Numbers')
                            print('#######################################################################')                    
                        if len(c) == len(p):
                            #Extract text from web elements
                            [company.append(i.text) for i in c]
                            [phone.append(i.text) for i in p]
                            #Append the city and state
                            for q in range(len(c)):
                                state.append(x)
                            for q in range(len(c)):
                                city.append(v)
                        else:#Skip page page array lengths dont match
                            print('Skipping Page')
                        #To get to the next page add &start= incremeting by 10
                        counter += 10
                        driver.get(yelpURL + '&start=' + str(counter))
                print('')
            counterReach += 1
        #Todays date to name CSV
        date = datetime.today().strftime('%Y-%m-%d')
        #Output data to CSV
        with open('C:/Users/Henry/Desktop/Yelp-Scrape/' + str(date) + '.csv', 'w', newline='') as f: #<------------- Change location you wish to create file
            fieldNames = ['Name', 'Phone', 'City', 'State', ]
            thewriter = csv.DictWriter(f, fieldnames = fieldNames)
            thewriter.writeheader()
            for i in range(len(company)):
                thewriter.writerow({'Name' : company[i], 'City' : city[i], 'State' : state[i], 'Phone' : phone[i]})

        input('All done your CSV can be found on your desktop folder Yelp-Scrape')

if __name__ == '__main__':
    main()