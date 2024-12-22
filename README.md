# amazon_Bot_for_deal

## Overview

This project is an advanced web scraping application crafted in Python, designed to extract valuable data from Amazon's Best Seller sections. The primary objective is to gather information on products offering discounts of over 50% and seamlessly export this data into a comprehensive CSV file. The extracted data includes:

- **Product Name**
- **Product Price**
- **Sale Discount**
- **Best Seller Rating**
- **Ship From**
- **Sold By**
- **Customer Rating**
- **Product Description**
- **Number of Units Sold in the Past Month**
- **Category Name**
- **All Available Product Images**

## Features

- Logs into Amazon using provided credentials by the user.
- If you encounter a CAPTCHA, you will need to manually solve it within the browser window. Once the CAPTCHA is successfully completed,  the  script will resume scraping automatically.
- Scrapes product details from multiple categories on Amazon Best Sellers.
- Extracts relevant product information like name, price, description, rating, images, etc.
- Filters products based on a discount of greater than 50%.
- Saves the collected data into a CSV file for easy analysis and viewing.

## Requirements

- `Python 3.12 `
- `Selenium`
- `WebDriver (e.g., ChromeDriver)`
- `webdriver-manager`
- `dotenv (for environment variables)`
- `CSV module`

## Installation

- Clone the repository:  `https://github.com/KrishnakumarModi/amazon_Bot_for_deal.git`
- Install the requirement mention above.
- Enter the email ID or phone number on the first line, followed by the password on the second line. The comment is written to guide you     through the navigation in the script.
- Enter the URL of the Best Seller page along with the desired categories.
- Run the script and you will get a `CSV` file with name `products`.

 