# selenium allows us to interact with HTML elements, such as clicking on a page using automation; in this case we will use it for specifying location on the Costco website
from selenium import webdriver
# to let us type stuff from our code we need to import Keys:
from selenium.webdriver.common.keys import Keys
# selenium module that lets us make the web driver wait until a certain condition is met (browser is loaded enough)
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
# pandas to be used for data storage and analysis
import pandas as pd

# must specify where the web driver is located and create a variable that will call on the web driver for chrome
path = "/Applications/chromedriver-92" 
driver = webdriver.Chrome(path)
# to make code easier to read, create variable for the url you want to use
url = "https://www.costco.ca/coupons.html"

# initializing lists
names = []
prices = []
savings = []
start_dates = []
end_dates = []

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
	for i, coupon_detail in enumerate(coupons_detail):
		coupon_name = coupon_detail.find_element_by_class_name("sl1").text
		names.append(coupon_name)

		coupon_savings = coupon_detail.find_element_by_class_name("price").text
		savings.append(coupon_savings)

		price_rows = coupon_detail.find_elements_by_class_name("eco-priceTable")
		

		if price_rows: 
			coupon_price = coupon_detail.find_elements_by_class_name("eco-priceTable")[2].text
		else:
			coupon_price = None	
		prices.append(coupon_price)
	
		# valid dates
		start_date = coupon_detail.find_element_by_xpath("//span[@class='CLP-validdates']/time[1]").text
		start_dates.append(start_date)
		end_date = coupon_detail.find_element_by_xpath("//span[@class='CLP-validdates']/time[2]").text
		end_dates.append(end_date)

# after it has collected all of the coupon data, close web driver
finally:
	driver.quit()

# creating a data frame
coupons = pd.DataFrame({
 	'Start Date' : start_dates,
 	'End Date' : end_dates,
 	'Product' : names,
  	'New Price' : prices,
 	'Savings' : savings,
 	})

coupons.to_csv('/Users/anjawu/Code/costco-deal-hunter/costco-coupons.csv')

# creating a new column that contains a number based on the location of where the search word is found (-1 returned if not found)
coupons["Search"] = coupons["Product"].str.find(key_word)
# searching for corresponding rows with key word
relevant_coupons = coupons.loc[coupons['Search'] > -1].copy()

#check if any row had a key word in it:
if not relevant_coupons.empty:
	# dropping the search column that we created, in order to make results look better.
	relevant_coupons = relevant_coupons.drop(['Search'], axis = 1)
	print(relevant_coupons)
	print("\n ------------------------------------------------------------------------------------------ \n")
else:
	print("No coupons found")
	print("\n ------------------------------------------------------------------------------------------ \n")

relevant_coupons.to_csv('/Users/anjawu/Code/costco-deal-hunter/relevant-costco-coupons.csv')

