# -*- coding: utf-8 -*-
"""
Created on Sun Mar 20 17:31:03 2022

@author: starm
"""
import selenium
import time
import csv
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

#Creates xpaths for each element
score_path= "//span[@itemprop='ratingValue']"
ratingCount= "//span[@itemprop='ratingCount']"
rank_path= "//span[@itemprop='ratingValue']"
popularity_path= "//*[text()='Popularity:']"
members_path="//*[text()='Members:']"
episodeCount_path= "//*[text()='Episodes:']"
premiered_path= "//*[text()='Premiered:']"
studio_path= "//*[text()='Studios:']"
source_path="//*[text()='Source:']"
favorites_path="//*[text()='Favorites:']"


PATH = "C:/Users/starm/Desktop/Anime_Score_learning_ML/Anime_Score_learning_ML/chromedriver.exe"
driver = webdriver.Chrome(PATH)
driver.get("https://myanimelist.net/topanime.php?limit=900")
original_window = driver.current_window_handle



#Enter the number of pages you want to scrape

Num_pages = 200

next_btn = [None] * Num_pages


#Opens a csv file to write to
with open('malData.csv','w',newline='') as f:
    #Makes the column names
    fieldnames = ['Title','Score','Episode_count','Studio','Source','Premiered','Members','Favorites','Popularity']
    thewriter = csv.DictWriter(f,fieldnames=fieldnames)
    
    #Sets the loop to scrape each page up to the Num_pages
    for x in range(Num_pages):

        #Finds the next page button for the first page since it is different than every other page
        if x == 1:
            first_next_btn = driver.find_element_by_xpath("//a[@class='link-blue-box next']")
            #first_next_btn = driver.find_element_by_xpath("/html/body/div[1]/div[2]/div[3]/div[2]/div[4]/h2/span[1]/a")
            first_next_btn.click()
        #Finds the next page button for every page but the first one
        elif x > 1:
            next_btn[x] = driver.find_element_by_id('contentWrapper')
            next_btn[x] = next_btn[x].find_element_by_xpath("//a[@class='link-blue-box next']")
            #next_btn[x] = driver.find_element_by_xpath("/html/body/div[1]/div[2]/div[3]/div[2]/div[4]/h2/span[1]/a[2]")
            next_btn[x].click()

        #Finds the table for the 50 shows listed
        table = driver.find_element_by_class_name("top-ranking-table")
        #Creates a list of each show in the variable anime
        anime = table.find_elements_by_class_name("ranking-list")
        
        
        url = [None] * 50
        y = 0
        for anime in anime:
            url[y] = anime.find_element_by_xpath("td[2]/div/div[2]/h3/a").get_attribute('href')
            y = y+1
        
        #For each show it will click on its link and open it in a new tab to scrape from  
        for url in url:
            time.sleep(1)
            
            driver.execute_script("window.open('');")
            driver.switch_to.window(driver.window_handles[1])
            driver.get(url)
            
            
            score = None
            title = None
            episodeCount_child = None
            premiered_child = None
            studio_child = None
            source_child = None
            member_child = None
            popularity_value = None
            
            #Trys to find each element and record them in a variable to be put into a csv. Will set it to None if it does not exist
            try:
                #gets score, also waits for page to load
                score = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, score_path)))
                score_value = score.text
                
                #Gets Title of the Show
                content = driver.find_element_by_id('contentWrapper')
                title = content.find_element_by_xpath("//div[@itemprop='name']")
                titleClean = title.text.encode("ascii", "ignore")
 
                #Searches for episode count
                try:
                    episodeCount_child = driver.find_element_by_xpath(episodeCount_path)
                    episodeCount = episodeCount_child.find_element_by_xpath("..")
                    episodeCount_value = episodeCount.text.encode("ascii", "ignore")
                except NoSuchElementException:
                    episodeCount_value = None
                #Searches for Premiered
                try:
                    premiered_child = driver.find_element_by_xpath(premiered_path)
                    premiered = premiered_child.find_element_by_xpath("..")
                    premiered_value = premiered.text.encode("ascii", "ignore")
                except NoSuchElementException:
                    premiered_value = None
                #Searches for Studio
                try:
                    studio_child = driver.find_element_by_xpath(studio_path)
                    studio = studio_child.find_element_by_xpath("..")
                    studio_value = studio.text.encode("ascii", "ignore")
                except NoSuchElementException:
                    studio_value = None
                #Searches for source
                try:
                    source_child = driver.find_element_by_xpath(source_path)
                    source = source_child.find_element_by_xpath("..")
                    source_value = source.text.encode("ascii", "ignore")
                except NoSuchElementException:
                    source_value = None
                #Searches for popularity
                try:
                    popularity_child = driver.find_element_by_xpath(popularity_path)
                    popularity = popularity_child.find_element_by_xpath("..")
                    popularity_value = popularity.text.encode("ascii", "ignore")
                except NoSuchElementException:
                    popularity_value = None
                #Searches for members
                try:
                    members_child = driver.find_element_by_xpath(members_path)
                    members = members_child.find_element_by_xpath("..")
                    members_value = members.text.encode("ascii", "ignore")
                except NoSuchElementException:
                    members_value = None
                try:
                     favorites_child = driver.find_element_by_xpath(favorites_path)
                     favorites = favorites_child.find_element_by_xpath("..")
                     favorites_value = favorites.text.encode("ascii", "ignore")
                except NoSuchElementException:
                     favorites_value = None   
                
            finally:
                thewriter.writerow({'Title' : titleClean,'Score' : score_value,'Episode_count' : episodeCount_value, 'Studio' : studio_value,'Source' : source_value,'Premiered' : premiered_value,'Members' : members_value,'Favorites' : favorites_value,'Popularity': popularity_value,})
                #time.sleep(1)
                #driver.switch_to.window(driver.window_handles[1])
                driver.close()
                driver.switch_to.window(original_window)

            

    


