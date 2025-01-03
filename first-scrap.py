import time
import random
import os
import pandas as pd
from urllib import robotparser
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from datetime import datetime, timedelta

# Setup Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36")

# Initialize the driver
chrome_driver_path = os.path.join(os.getcwd(), "chromedriver")
driver = webdriver.Chrome(executable_path=chrome_driver_path, options=chrome_options)

# Base URL for the job listings
base_url = "https://www.gaapweb.com/jobs/"

# Check robots.txt to ensure scraping is allowed
def is_scraping_allowed(url, user_agent='*'):
    robots_url = "https://www.gaapweb.com/robots.txt"
    rp = robotparser.RobotFileParser()
    rp.set_url(robots_url)
    rp.read()
    return rp.can_fetch(user_agent, url)

if not is_scraping_allowed(base_url):
    print(f"Scraping is not allowed on {base_url} according to robots.txt")
    driver.quit()
    exit()

# Navigate to the first page
driver.get(base_url)

# Define a function to extract elements
def extract_element(card, selector_type, selectors, attribute=None, default_value="N/A"):
    """
    Extracts the text or attribute from a web element within a job card.
    
    Args:
    - card: The WebElement (job card) to search within.
    - selector_type: The type of selector (e.g., By.CSS_SELECTOR).
    - selector: The selector [] (e.g., ['h3.lister__header a span']).
    - attribute: Optional. If specified, the function will return the element's attribute (e.g., 'href') instead of text.
    - default_value: Optional. The default value to return if extraction fails (default is "N/A").
    
    Returns:
    - The extracted text or attribute, or the default value if extraction fails.
    """
    for selector in selectors:
        try:
            element = card.find_element(selector_type, selector)
            if attribute:
                return element.get_attribute(attribute)
            return element.text
        except Exception as e:
            print(f"Error extracting element for selector '{selector}'")
    return default_value


# Function to extract job data from a page
def extract_jobs_from_page(driver):
    job_cards = driver.find_elements(By.CSS_SELECTOR, 'li.lister__item.cf[id^="item-"]')
    jobs = []
    
    for card in job_cards:
        # Extract job details using the reusable function
        title = extract_element(card, By.CSS_SELECTOR, ['h3.lister__header a span'])
        job_url = extract_element(card, By.CSS_SELECTOR, ['h3.lister__header a'], attribute='href')
        company = extract_element(card, By.CSS_SELECTOR, ['li.lister__meta-item--recruiter'])
        location = extract_element(card, By.CSS_SELECTOR, ['li.lister__meta-item--location'])
        salary = extract_element(card, By.CSS_SELECTOR, ['li.lister__meta-item--salary'])
        
        # Handle 'span' and 'li' for date_posted
        # date_posted = extract_element(card, By.CSS_SELECTOR, [
        #     'li.job-actions__action.pipe span',  # Try to extract from span first
        #     'li.job-actions__action.pipe'        # Fallback to extracting from li if span is missing
        # ])
        
        date_posted = "N/A"

        jobs.append({
            "Title": title,
            "Company": company,
            "Salary": salary,
            "Location": location,
            "Date Posted": date_posted,
            "Job URL": job_url
        })

    return jobs

# Function to find the 'Next' button and navigate to the next page
def go_to_next_page(driver):
    try:
        next_button = driver.find_element(By.CSS_SELECTOR, 'li.paginator__item a[rel="next"]')
        next_page_url = next_button.get_attribute('href')
        if next_page_url:
            driver.get(next_page_url)
            return True
    except Exception as e:
        print(f"No next page found: {e}")
    return False

# Main scraping loop to handle pagination with rate limiting
all_jobs = []
page = 1

while True:
    print(f"Scraping page: {page}...")
    
    # Extract jobs from the current page
    jobs = extract_jobs_from_page(driver)
    all_jobs.extend(jobs)
    
    # Check if there's a next page and navigate to it
    if not go_to_next_page(driver):
        break  # Exit the loop if there's no next page
    
    # Implement rate limiting with a random delay to mimic human behavior
    delay = random.uniform(2, 10)  # Delay between 2 and 10 seconds
    print(f"Waiting for {delay:.2f} seconds before next page...")
    time.sleep(delay)  # Rate limiting to avoid overwhelming the server
    
    page += 1

# Convert the list of jobs to a DataFrame
df_jobs = pd.DataFrame(all_jobs)

# Display the DataFrame
print(df_jobs)
df_jobs.to_csv('jobs_data.csv', index=False)

# for job in jobs:
#     print(job)

# Close the browser
driver.quit()
