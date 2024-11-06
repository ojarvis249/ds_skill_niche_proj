from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
import pandas as pd

# Initialize the Chrome driver
driver = webdriver.Chrome()

# URL to scrape from Indeed
url = "https://uk.indeed.com/q-data-scientist-jobs.html?vjk=e9bcef54d4749789"

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
except Exception:
    print("No cookies button found")

# List to store job data
jobs = []


# Function to scrape job listings from the current page
def scrape_jobs():
    # Locate job cards
    job_cards = driver.find_elements(
        By.XPATH, "//div[contains(@class, 'job_seen_beacon')]"
    )
    print(f"Found {len(job_cards)} job listings on this page.")

    # Loop through each job card
    for job_card in job_cards:
        try:
            # Click on the job card to open the job details
            job_card.click()
            time.sleep(2)  # Wait for the job details to load

            # Extract job title
            job_title = driver.find_element(
                By.XPATH,
                "//h2[contains(@class, 'jobsearch-JobInfoHeader-title')]//span",
            ).text

            # Extract company name
            company_name = driver.find_element(
                By.XPATH, "//div[contains(@data-company-name, 'true')]//a"
            ).text

            # Extract location
            location = driver.find_element(
                By.XPATH, "//div[@data-testid='inlineHeader-companyLocation']//div"
            ).text

            # Extract job description
            job_description_element = driver.find_element(
                By.XPATH, '//*[@id="jobDescriptionText"]/div'
            )
            inner_html = job_description_element.get_attribute("innerHTML")
            soup = BeautifulSoup(inner_html, "html.parser")
            job_description = soup.get_text()

            # Store the job data in a dictionary
            job_data = {
                "Job Title": job_title,
                "Company Name": company_name,
                "Location": location,
                "Job Description": job_description,
            }

            print(f"Collected data for job: {job_data}")
            jobs.append(job_data)

            # Go back to the job listings page
            driver.back()
            time.sleep(2)  # Wait for the job listings to load again

        except Exception as e:
            print("Error processing job:", e)


# Loop through pages 2 to 5
for page_number in range(2, 6):
    try:
        # Click the page number link
        next_page = driver.find_element(
            By.XPATH,
            f'//*[@id="jobsearch-JapanPage"]/div/div[5]/div/div[1]/nav/ul/li[{page_number}]/a',
        )
        next_page.click()
        time.sleep(4)  # Wait for the next page to load

        # Scrape jobs from the new page
        scrape_jobs()

    except Exception as e:
        print(f"Error navigating to page {page_number}: {e}")
        break

# Close the driver
driver.quit()

# Create a DataFrame and save to CSV
df = pd.DataFrame(jobs)
print(f"Total jobs collected: {len(df)}")
df.to_csv("indeed_jobs_data_scientist.csv", index=False)
