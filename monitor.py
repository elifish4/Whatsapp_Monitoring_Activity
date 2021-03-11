from os import system, name 
import pygame
import time
import random
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import os


PlayAudio = False

def get_contactName():
	try:
		contactName = os.environ['WhatsappContactName']
	except:
		contactName = input("Enter your whatsapp contact name to monitor: ")

	return contactName

def get_MsgSendFeature():
	try:
		SendMsgFeature = os.environ['WhatsappMsgSendEnabled']
	except:
		SendMsgFeature = input("Do you want to send automatic message when online and offline? [y/n]: ")

	return SendMsgFeature


contactName = get_contactName()
SendMsgFeature = get_MsgSendFeature()
pygame.mixer.init()
onlineMessage = input ("Enter automatic text to send when online :")
offlineMessage = input ("Enter automatic text to send when offline :")


def clear(): 
     _ = system('clear')

def contactSearch():
	user_contact = WebDriverWait(driver, 60).until(
            EC.visibility_of_element_located((
                By.XPATH, "//*[@id='side']/div[1]/div/label/div/div[2]")))
	user_contact.send_keys(contactName)
	time.sleep(3)
	user_contact.send_keys(Keys.TAB)
	user_contact.send_keys(Keys.ENTER)



def messageSend(msg):
	check = WebDriverWait(driver, 60).until(
            EC.visibility_of_element_located((
                By.XPATH, "//div[contains(text(), 'Type a message')]/following-sibling::div")))
	if(SendMsgFeature == "y"):
		check.send_keys(msg)
		check.send_keys(Keys.SHIFT, Keys.ENTER)
		check.send_keys(Keys.SHIFT, Keys.ENTER)
		time.sleep(2)
		check.send_keys(Keys.ENTER)


def checkOffline():
	while True:
		try:
			print("Waiting for user to go offline")
			confirm = WebDriverWait(driver,3).until(
		            EC.visibility_of_element_located((
		                By.XPATH, "//span[starts-with(@title, 'last')]")))
			now = datetime.now()
			current_time = now.strftime("%H:%M:%S")
			print(current_time + " : User went offline" )
			messageSend(offlineMessage)
			if(PlayAudio):
				pygame.mixer.music.load("audio/offline.mp3")
				pygame.mixer.music.play()
			break
		except:
			print("Waiting for user to go offline...")
			try:
				print("Checking if last seen disabled.")
				lastSeenDisabled = driver.find_element_by_xpath("//*[@id='main']/header/div[2]/div[2]/span")
			except:
				print("Seems user has disabled last seen. User went offline")
				messageSend(offlineMessage)
				if(PlayAudio):
					pygame.mixer.music.load("audio/offline.mp3")
					pygame.mixer.music.play()
				break
			continue
	checkOnline()

def checkOnline():
	while True:
		try:
			print("Waiting for user to come online")			
			confirm = WebDriverWait(driver, 60).until(
		            EC.visibility_of_element_located((
		                By.XPATH, "//span[starts-with(@title, 'online') or starts-with(@title, 'typing...')]")))
			now = datetime.now()
			current_time = now.strftime("%H:%M:%S")
			print(current_time + " : User came online...")
			messageSend(onlineMessage)
			if(PlayAudio):
				pygame.mixer.music.load("audio/online.mp3")
				pygame.mixer.music.play()
			break
		except:
			print("I am still waiting for user to come online.")
			continue
	checkOffline()




driver = webdriver.Chrome('./chromedriver')
driver.get("https://web.whatsapp.com")
clear()
print("Searching user...")

contactSearch()


print("Chat box opened. Confirming once again...")

confirm = WebDriverWait(driver, 60).until(
            EC.visibility_of_element_located((
                By.XPATH, "//*[@id='main']/header/div[2]/div/div/span")))
if(confirm.text == contactName):
	print("Success!!")
	checkOnline()
else:
	print("Failed at confirming correct contact clicked...")
