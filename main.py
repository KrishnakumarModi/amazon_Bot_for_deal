from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv
import time
import csv
import os
load_dotenv()


# login setup
def login(driver,email,password):
    driver.get('https://www.amazon.com/ap/signin?openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.com%2Fsign%2Fs%3Fk%3Dsign%2Bin%26ref_%3Dnav_custrec_signin&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=usflex&openid.mode=checkid_setup&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0')
    time.sleep(20)
    try:
        email_Input = driver.find_element(By.XPATH,'//input[@id="ap_email"]')
        email_Input.send_keys(email)
        email_Input.send_keys(Keys.RETURN)
        time.sleep(2)

        password_Input = driver.find_element(By.XPATH,'//input[@id="ap_password"]')
        password_Input.send_keys(password)
        password_Input.send_keys(Keys.RETURN)
        time.sleep(2)
        # captcha to be filled by user(if any)
        time.sleep(20)
    except Exception as e:
        print("fail to login!")



# Function to go to the next page
def next_Page(driver):
    try:
        # Wait for the "Next" button to become clickable and click it
        next_Button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//li[@class="a-last"]'))
        )
        next_Button.click()
        time.sleep(3)  # Give time for the page to load
    except Exception as e:
        print(f"Error while clicking the next button: {e}")


# Function to extract product data from Amazon's Best Seller pages
def extract_product_details(driver, category_url):
    driver.get(category_url)
    time.sleep(2)
    
    products = []
    
    # Scraping the product list
    product_list = driver.find_elements(By.XPATH, '//div[@class="_cDEzb_iveVideoWrapper_JJ34T has-ive-video"]')
    for product in product_list:
        try:
            name = product.find_element(By.XPATH, './/div[@class="_cDEzb_p13n-sc-css-line-clamp-3_g3dy1"]').text
        except:
            name = "Not available"
        try:
            best_Seller_rating = product.find_element(By.XPATH, './/span[@class="zg-bdg-text"]').text.strip()              
        except:
            best_Seller_rating = "Not available"
        try:
            category_Name = product.find_element(By.XPATH, './/span[@class="_p13n-zg-nav-tree-all_style_zg-selected__1SfhQ"]').text
            
        except:
            category_Name = "Not available"
                            

    # Open product page
        
        product_Link = product.find_element(By.LINK_TEXT, name).get_attribute("href")
            
        driver.execute_script("window.open(arguments[0]);", product_Link)
        driver.switch_to.window(driver.window_handles[1])

        time.sleep(5)
        try:
            sold_Past_month = driver.find_element(By.XPATH, '//*[@id="social-proofing-faceout-title-tk_bought"]/span[1]').text
        except:
            sold_Past_month = "Not  available"
        try:
            description = driver.find_element(By.XPATH, '//*[@id="productDetails_techSpec_section_1"]/tbody').text
        except:
            description = "Not available"
        try:
            images = [img.get_attribute('src') for img in driver.find_elements(By.CLASS_NAME, 'a-dynamic-image a-stretch-horizontal')]
            
        except:
            images = ["Not available"]
        try:
            ship_from = driver.find_element(By.XPATH, '//*[@id="tabular-buybox"]/div[1]/div[4]/div/span').text
        except:
            ship_from = "Not available"
        try:
            sold_by = driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div[4]/div[1]/div[3]/div/div[1]/div/div/div/form/div/div/div/div/div[4]/div/div[18]/div[1]/div[1]/div[6]/div/span/a').text
        except:
                
            sold_by = "Not available"
        try:   
            price = driver.find_element(By.XPATH, '//*[@id="corePrice_feature_div"]/div/div/span[1]/span[2]/span[2]').text
        except:   
            price = "Not available"
        try:
            discount = driver.find_element(By.XPATH, '//span[@class="a-size-large a-color-price savingPriceOverride aok-align-center reinventPriceSavingsPercentageMargin savingsPercentage"]').text.replace("-","")
        except:
            discount = "Not available"
            
        try:
            rating = driver.find_element(By.XPATH, '//*[@id="acrCustomerReviewText"]')
            rating = [rating.text.replace(",","").replace(" ",",")]
            rating = rating[0]

        except:
            rating = "Not available"

        
        # Only append products with > 50% discount
        if discount!="Not available" and float(discount.replace('%'or '', '').strip()) > 50:
            products.append({
                'Product Name': name,
                'Product Price': price,
                'Sale Discount': discount,
                'Best Seller Rating': best_Seller_rating,
                'Rating': rating,
                'Ship From': ship_from,
                'Sold By': sold_by,
                'Product Description': description,
                'Number Bought in the Past Month' : sold_Past_month,
                'Category Name': category_Name,
                'Images': images
        })
    
            
            # close product page
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
                

    next_Page(driver)
            


    return products


def save_data(products, filename, file_type):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        fieldnames = ['Product Name', 'Product Price', 'Sale Discount', 'Best Seller Rating', 
                     'Rating', 'Ship From', 'Sold By', 'Product Description', 
                     'Number Bought in the Past Month', 'Category Name', 'Images']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for product in products:
            product['Images'] = ", ".join(product['Images'])
            writer.writerow(product)




# Main function
def main():
    email = os.getenv('number')
    password = os.getenv('password')    
    
    # List of categories to scrape
    categories = [
        "https://www.amazon.in/gp/bestsellers/kitchen/ref=nav_custrec_signin",
        "https://www.amazon.in/gp/bestsellers/shoes/ref=zg_bs_nav_shoes_0",
        "https://www.amazon.in/gp/bestsellers/computers/ref=zg_bs_nav_computers_0",
        "https://www.amazon.in/gp/bestsellers/toys/ref=zg_bs_toys_sm",
        "https://www.amazon.in/gp/bestsellers/beauty/ref=zg_bs_beauty_0",
        "https://www.amazon.in/gp/bestsellers/jewelry/ref=zg_bs_nav_jewelry_0",
        "https://www.amazon.in/gp/bestsellers/books/ref=zg_bs_books_0",
        "https://www.amazon.in/gp/bestsellers/dvd/ref=zg_bs_nav_dvd_0",
        "https://www.amazon.in/gp/bestsellers/music/ref=zg_bs_nav_music_0",
        "https://www.amazon.in/gp/bestsellers/watches/ref=zg_bs_watches_sm",
        # Add more category URLs
    ]
    
    # Setting up WebDriver
   
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    
    try:
        login(driver, email, password)
        all_products = []
        
        for category_url in categories:
            print(f"Scraping category: {category_url}")
            category_products = extract_product_details(driver, category_url)
            all_products.extend(category_products)
        
        save_data(all_products, 'products.csv', 'csv')
    
    finally:
        driver.quit()

if __name__ == '__main__':
    main()
