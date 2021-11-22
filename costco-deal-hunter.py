# selenium allows us to interact with HTML elements, such as clicking on a page using automation; in this case we will use it for specifying location on the Costco website
from selenium import webdriver
# to let us type stuff from our code we need to import Keys:
from selenium.webdriver.common.keys import Keys
# selenium module that lets us make the web driver wait until a certain condition is met (browser is loaded enough)
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# pandas to be used for data storage and analysis
import pandas as pd

# must specify where the web driver is located and create a variable that will call on the web driver for chrome
path = "/Applications/chromedriver-96" 
driver = webdriver.Chrome(path)
# to make code easier to read, create variable for the url you want to use
url = "https://www.costco.ca/coupons.html"

# initializing lists: "instead of initializing 5 lists and appending each column of data into them, you can initialize one list"
products_list = []

print("automated")

# make the word search into a list of words, and change search to be iterated over list
key_word = "chicken"

# to pull open the webpage:
driver.get(url)

# navigating Costco's webpage to select ON as region for flyer.
select_region = driver.find_element_by_xpath("//input[@value = 'ON']").click()
set_region = driver.find_element_by_xpath("//input[@value = 'Set Language and Region']").click()

# to make sure the webpage is loaded with the correct page after the clicks from above we use try.
try:
	all_coupons = WebDriverWait(driver, 10).until(
		EC.presence_of_element_located((By.ID, "coupons-lp"))
	)
	
	# collecting the product details from each coupon for name, price and savings
	coupons_detail = all_coupons.find_elements_by_xpath("//div[@class='CLpbulkcoup']")
	# iterating through each coupon to get the name and the savings
	for coupon_detail in coupons_detail:
		coupon_name = coupon_detail.find_element_by_class_name("sl1").text

		coupon_savings = coupon_detail.find_element_by_class_name("price").text

		price_rows = coupon_detail.find_elements_by_class_name("eco-priceTable")
		
		# some of the prices might be missing because they only include a % off depending on what you get, so we must account for that
		if price_rows: 
			coupon_price = coupon_detail.find_elements_by_class_name("eco-priceTable")[2].text
		else:
			coupon_price = None	
	
		# valid dates
		start_date = coupon_detail.find_element_by_xpath("//span[@class='CLP-validdates']/time[1]").text
		end_date = coupon_detail.find_element_by_xpath("//span[@class='CLP-validdates']/time[2]").text

		# creating dictionary to be able to append once, as opposed to for each data point pulled
		data = {
			'Start Date' : start_date,
 			'End Date' : end_date,
			'Product' : coupon_name,
			'New Price' : coupon_price,
			'Savings' : coupon_savings,
		}

		# appending each dictionary entry to our list
		products_list.append(data)

# after it has collected all of the coupon data, close web driver
finally:
	driver.quit()

# creating a data frame
coupons = pd.DataFrame(products_list)


coupons.to_csv('/Users/anjawu/Code/costco-deal-hunter/costco-coupons.csv')

# searching for corresponding rows with key word: number is based on the location of where the search word is found (-1 returned if not found)
relevant_coupons = coupons[coupons["Product"].str.find(key_word) > -1]

#check if any row had a key word in it:
if not relevant_coupons.empty:
	print(relevant_coupons)
	print("\n ------------------------------------------------------------------------------------------ \n")
else:
	print("No coupons found")
	print("\n ------------------------------------------------------------------------------------------ \n")

relevant_coupons.to_csv('/Users/anjawu/Code/costco-deal-hunter/relevant-costco-coupons.csv')

