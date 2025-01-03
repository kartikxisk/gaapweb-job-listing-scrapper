# Gaapweb Job Listings Scraper

This project is a web scraping script designed to extract job listing details from the [Gaapweb](https://www.gaapweb.com/) website. The script uses Python and Selenium to navigate the website, extract relevant job details, and save the data to a CSV file. It adheres to ethical scraping practices by respecting the `robots.txt` file and implementing rate limiting.

## Features

- **Data Extraction**: Scrapes job titles, company names, locations, salaries, and job posting dates.
- **Pagination Handling**: Automatically navigates through multiple pages of job listings.
- **Headless Mode**: Runs in headless mode for efficiency and reduced resource consumption.
- **Data Output**: Outputs the scraped data as a CSV file for further analysis.

## Requirements

Before running the script, ensure you have the following installed:

- Python 3.8 or later
- Google Chrome browser
- ChromeDriver (compatible with your Chrome version)
- Required Python libraries: `selenium`, `pandas`, `datetime`

After installing the dependencies run using this command:
```
python first-scrap.py
```

## Contributing
Contributions are welcome! Feel free to open issues or submit pull requests.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Disclaimer
This script is for educational and personal use only. Ensure you have permission to scrape the website before running the script.
