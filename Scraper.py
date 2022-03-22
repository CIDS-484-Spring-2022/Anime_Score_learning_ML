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


PATH = "C:/Users/starm/Desktop/Anime_Score_learning_ML/Anime_Score_learning_ML/chromedriver.exe"
driver = webdriver.Chrome(PATH)
driver.get("https://myanimelist.net/topanime.php?limit=0")



#Enter the number of pages you want to scrape

Num_pages = 20



#Opens a csv file to write to
with open('malData.csv','w',newline='') as f:
    #Makes the column names
    fieldnames = ['Title','Score','Episode_count','Popularity','Studio','Source','Premiered','Members']
    thewriter = csv.DictWriter(f,fieldnames=fieldnames)
    
    #Sets the loop to scrape each page up to the Num_pages
    for x in range(Num_pages):
        #Finds the next page button for the first page since it is different than every other page
        if x == 1:
            first_next_btn = driver.find_element_by_xpath("/html/body/div[1]/div[2]/div[3]/div[2]/div[4]/h2/span[1]/a")
            first_next_btn.click()
        #Finds the next page button for every page but the first one
        elif x > 1:
            next_btn = driver.find_element_by_xpath("/html/body/div[1]/div[2]/div[3]/div[2]/div[4]/h2/span[1]/a[2]")
            next_btn.click()

        #Finds the table for the 50 shows listed
        table = driver.find_element_by_class_name("top-ranking-table")
        #Creates a list of each show in the variable anime
        anime = table.find_elements_by_class_name("ranking-list")        
            
        #For each show it will click on its link and open it in a new tab to scrape from  
        for anime in anime:
            #Clicks on elements href to bring up the anime's page
            time.sleep(1)
            url = anime.find_element_by_xpath("td[2]/div/div[2]/h3/a").get_attribute('href')
            driver.execute_script("window.open('');")
            time.sleep(1)
            driver.switch_to.window(driver.window_handles[1])
            driver.get(url)
            
            #Trys to find each element and record them in a variable to be put into a csv. Will set it to None if it does not exist
            try:
                #gets score, also waits for page to load
                score = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, score_path)))
                score_value = score.text
                #Searches for episode count
                title = driver.find_element_by_xpath("/html/body/div[1]/div[2]/div[3]/div[1]/div/div[1]/div/h1/strong")
                try:
                    episodeCount_child = driver.find_element_by_xpath(episodeCount_path)
                    episodeCount = episodeCount_child.find_element_by_xpath("..")
                    episodeCount_value = episodeCount.text
                except NoSuchElementException:
                    episodeCount_value = None
                #Searches for Premiered
                try:
                    premiered_child = driver.find_element_by_xpath(premiered_path)
                    premiered = premiered_child.find_element_by_xpath("..")
                    premiered_value = premiered.text
                except NoSuchElementException:
                    premiered_value = None
                #Searches for Studio
                try:
                    studio_child = driver.find_element_by_xpath(studio_path)
                    studio = studio_child.find_element_by_xpath("..")
                    studio_value = studio.text
                except NoSuchElementException:
                    studio_value = None
                #Searches for source
                try:
                    source_child = driver.find_element_by_xpath(source_path)
                    source = source_child.find_element_by_xpath("..")
                    source_value = source.text
                except NoSuchElementException:
                    source_value = None
                #Searches for popularity
                    #popularity= driver.find_element_by_xpath("/html/body/div[1]/div[2]/div[3]/div[2]/table/tbody/tr/td[2]/div[1]/table/tbody/tr[1]/td/div[1]/div[1]/div[1]/div[1]/div[2]/span[2]/strong")
                   # popularity_value = popularity.text
                   # print(popularity.text)
                #Searches for members
                try:
                    members_child = driver.find_element_by_xpath(members_path)
                    members = members_child.find_element_by_xpath("..")
                    members_value = members.text
                except NoSuchElementException:
                    members_value = None
                
            finally:
                thewriter.writerow({'Title' : title,'Score' : score_value,'Episode_count' : episodeCount_value,'Studio' : studio_value,'Source' : source_value,'Premiered' : premiered_value,'Members' : members_value})
                time.sleep(1)
                driver.close()
                driver.switch_to.window(driver.window_handles[0])

            

               
    


