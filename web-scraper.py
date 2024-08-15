########## Since UofT account logins require Duo MFA, web scraping is not possible, so this code is not functional ##########
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Setup Chrome WebDriver
service = Service()
driver = webdriver.Chrome()

# Open ProQuest login page and automate login
driver.get('http://myaccess.library.utoronto.ca/login?qurl=https://www.proquest.com/docview/2708678275?accountid=14771&bdid=56474&_bd=7fsOp%2FSMnb33oXYt%2BttB%2FAsrQLE%3D')

# Automate login 
login_button1 = driver.find_element(By.CLASS_NAME, 'loginButton')
login_button1.click()
username = driver.find_element(By.ID, 'username')
password = driver.find_element(By.ID, 'password')
username.send_keys('usrn') # Your username`
password.send_keys('pswd') # Your password
login_button2 = driver.find_element(By.ID, 'login-btn')
login_button2.click()

# This is where the website asks for Duo MFA, so unless the user clicks allow on their device, the code below will not run

# Wait for the article page to load
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, 'documentTitle'))
)

# Pass the page source to BeautifulSoup for parsing
soup = BeautifulSoup(driver.page_source, 'html.parser')
# Extract and print the title of the page
title = soup.title.string
print(f"Title: {title}")
# Extract and print all paragraphs
paragraphs = soup.find_all('p')
for i, paragraph in enumerate(paragraphs, start=1):
    print(f"Paragraph {i}: {paragraph.get_text()}")
# Extract the article text
article_div = soup.find('div', class_='article-body')
# Check if the div was found
if article_div is not None:
    # Extract and print the text content
    article_text = article_div.get_text()
else:
    # Handle the case where the div was not found
    article_text = ""
    print("No article body found.")

driver.quit()