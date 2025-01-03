# Web Scraping Documentation

## 1. Introduction
This document outlines the procedure for extracting key job details from job listings on the Gaapweb website. It includes information on how to:
- Extract data.
- Handle pagination.
- Run the script in headless mode.
- Display the extracted data as a DataFrame.
- Adhere to best practices while scraping.

---
## 2. Run
``` python first_script.py```
## 3. Procedure for Extracting Key Details

### 2.1 Extracting Key Job Details
The following details are extracted from each job listing:
- **Job Title**: The title of the job position.
- **Company Name**: The name of the company offering the job.
- **Location**: The geographical location of the job.
- **Salary**: The offered salary, if available.
- **Date Posted**: The time elapsed since the job was posted, formatted as a date.
- **Job URL**: The link to the job listing for more information (*not found on the page*).

To extract these details, Selenium is used to locate the relevant elements in the HTML structure of the webpage. Below is the relevant Python code snippet:

```python
# Code snippet for extracting job details
from selenium import webdriver
from selenium.webdriver.common.by import By

# Example: Extracting Job Title
job_titles = driver.find_elements(By.CLASS_NAME, 'job-title-class')
for title in job_titles:
    print(title.text)

