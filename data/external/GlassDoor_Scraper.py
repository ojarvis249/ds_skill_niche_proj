#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 09:32:36 2020

author: Kenarapfaik
url: https://github.com/arapfaik/scraping-glassdoor-selenium
"""


from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import re
import pandas as pd


driver = webdriver.Chrome()

urls = ["https://www.glassdoor.co.uk/Job/data-science-jobs-SRCH_KO0,12.htm"]

jobs = []


def loadAllJobs():
    while True:
        try:
            more = driver.find_element(
                by=By.CSS_SELECTOR,
                value=".JobsList_buttonWrapper__ticwb > button:nth-child(1)",
            )
            more.click()
            time.sleep(2)
            try:
                close = driver.find_element(by=By.CSS_SELECTOR, value=".CloseButton")
                close.click()
                print("Popup closed")
            except:  # noqa: E722
                print("No popup to close")
        except Exception as e:
            print("All jobs loaded or button not found:", e)
            break


def closeCookies():
    try:
        cookies = driver.find_element(
            by=By.XPATH, value='//*[@id="onetrust-accept-btn-handler"]'
        )
        cookies.click()
    except:
        print("No cookies button found")


def get_jobs(url):
    print(f"Looking for jobs in {url}")
    driver.get(url)
    time.sleep(4)
    closeCookies()
    loadAllJobs()

    job_listings = driver.find_elements(
        by=By.CLASS_NAME, value="JobCard_jobCardContainer___hKKI"
    )
    print(f"Found {len(job_listings)} job listings")

    for job_card in job_listings:
        try:
            job_card.click()
            time.sleep(1)

            deets = driver.find_element(
                by=By.XPATH, value="//header/div[1]"
            ).text  # Updated XPath for flexibility
            lines = deets.split("\n")

            employer = lines[0] if lines else "null"
            title = lines[2] if len(lines) > 2 else "null"
            location = lines[3] if len(lines) > 3 else "null"
            rating = re.findall(r"\b\d+\.\d+\b", deets) or ["null"]

            try:
                salary = driver.find_element(
                    by=By.CSS_SELECTOR, value=".SalaryEstimate_medianEstimate__fOYN1"
                ).text
            except:
                salary = "null"

            try:
                size = driver.find_element(
                    by=By.CSS_SELECTOR,
                    value="div.JobDetails_overviewItem__cAsry:nth-child(1) > div:nth-child(2)",
                ).text
            except:
                size = "null"

            try:
                founded = driver.find_element(
                    by=By.CSS_SELECTOR,
                    value="div.JobDetails_overviewItem__cAsry:nth-child(2) > div:nth-child(2)",
                ).text
            except:
                founded = "null"

            try:
                job_desc = driver.find_element(
                    by=By.CSS_SELECTOR, value=".JobDetails_showMore___Le6L"
                ).text
                job_desc += driver.find_element(
                    by=By.XPATH, value="//section/div[2]/div[1]"
                ).text
            except:
                job_desc = "null"

            skills = ""  # Initialize skills; modify as needed based on job description

            job_data = {
                "Job Title": title,
                "Company Name": employer,
                "Salary Estimate": salary,
                "Rating": rating[0],
                "Job Description": job_desc,
                "Skills": skills,
                "Location": location,
                "Founded": founded,
                "Size": size,
            }

            print(f"Collected data for job: {job_data}")
            jobs.append(job_data)

        except Exception as e:
            print("Error processing job:", e)


for url in urls:
    get_jobs(url)

driver.quit()

# Create a DataFrame and save to CSV
df = pd.DataFrame(jobs)
print(f"Total jobs collected: {len(df)}")
df.to_csv("glassdoor_jobs.csv", index=False)
