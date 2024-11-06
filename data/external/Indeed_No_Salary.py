#!/usr/bin/python3

from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup

# Initialize the Chrome driver
driver = webdriver.Chrome()

# URL to scrape from Indeed
url = "https://uk.indeed.com/jobs?q=data+science&l=United+Kingdom&from=searchOnDesktopSerp&vjk=2a9c8f6904f2a734"

# Open the Indeed page
driver.get(url)
time.sleep(4)  # Wait for the page to load

# Accept cookies if prompted
try:
    cookies_button = driver.find_element(
        By.XPATH, '//*[@id="onetrust-accept-btn-handler"]'
    )
    cookies_button.click()
    time.sleep(1)  # Wait for the button click action
except:
    print("No cookies button found")

# Locate the first job title, company name, location elements in the search results
try:
    # Job title
    job_title = driver.find_element(
        By.XPATH, "//h2[contains(@class, 'jobsearch-JobInfoHeader-title')]//span"
    ).text
    print("First Job Title:", job_title)
except Exception as e:
    print("Error locating job title:", e)

try:
    # Company name
    company_name = driver.find_element(
        By.XPATH, "//div[contains(@data-company-name, 'true')]//a"
    ).text
    print("Company Name:", company_name)
except Exception as e:
    print("Error locating company name:", e)

# Try to locate the location
try:
    location = driver.find_element(
        By.XPATH, "//div[@data-testid='inlineHeader-companyLocation']//div"
    ).text
    print("Location:", location)
except Exception as e:
    print("Error locating location:", e)


# Try to locate the job description
try:
    job_description_element = driver.find_element(
        By.XPATH, '//*[@id="jobDescriptionText"]/div'
    )
    # Get the inner HTML
    inner_html = job_description_element.get_attribute("innerHTML")
    # Use BeautifulSoup to parse and extract text
    soup = BeautifulSoup(inner_html, "html.parser")
    job_description = soup.get_text()
    print("Job Description:", job_description)
except Exception as e:
    print("Error locating job description:", e)

# Close the driver
driver.quit()
