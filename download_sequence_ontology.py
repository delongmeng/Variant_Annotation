'''
This program sets up the chrome driver and scrapes the sequence ontology table from an Ensembl webpage.
The data is saved to a local csv file for future use.
To use this program, make sure there is a chromedriver app in the same folder. If not, please download it from its official website.
Alternatively, you can also change the CHROMEDRIVER_PATH to be the path of the chromedriver.
Make sure packages (such as selenium, pandas) are installed, and then simply type the following code in command line:
python download_sequence_ontology.py 
'''

import requests
import pandas as pd
from selenium import webdriver 
from selenium.webdriver.chrome.options import Options

def main():

	# set up the chrome driver, use the headless mode
	CHROMEDRIVER_PATH = './chromedriver'
	options = Options()
	options.headless = True
	driver = webdriver.Chrome(CHROMEDRIVER_PATH, options=options)

	# request the sequence ontology table from the html file and extract the content of the table
	so_url = "https://m.ensembl.org/info/genome/variation/prediction/predicted_data.html"
	driver.get(so_url)
	so_table = pd.read_html(driver.page_source)
	driver.quit()

	# briefly clean the data and save to 
	so_table[0].drop('*', axis = 1).to_csv("sequence_ontology.csv")

# Call the main function to run the program
if __name__ == "__main__":
    main()

