#Setting Chrome driver and selenium

!pip install chromedriver-autoinstaller

import sys
sys.path.insert(0,'/usr/lib/chromium-browser/chromedriver')

import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
import chromedriver_autoinstaller

# setup chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless') # ensure GUI is off
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

# set path to chromedriver as per your configuration
chromedriver_autoinstaller.install()


# set up the webdriver
driver = webdriver.Chrome(options=chrome_options)

# SCRAPER

from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd


#convert string price to numeric
def parse_number_string(number_string):
    # Define the mapping of Indian number system terms to their numeric values
    pak_number_system = {'Crore': 10000000, 'Lakh': 100000}

    # Split the input string into value and unit
    value, unit = number_string.split()

    # Convert the value to a float and the unit to its numeric multiplier
    value = float(value)
    multiplier = pak_number_system.get(unit, 1)

    # Multiply the value by the multiplier and convert it to an integer
    result = int(value * multiplier)

    return result


#for lahore and isl conversaion
def convert_to_square_yards(input_string):
    # Define conversion factors
    marla_to_sq_yards = 25
    kanal_to_sq_yards = 500

    # Split the input string into numeric value and unit
    numeric_value, unit = input_string.split()

    # Convert the numeric value to a float
    numeric_value = float(numeric_value)

    # Perform the conversion based on the unit
    if unit.lower() == 'marla':
        result = numeric_value * marla_to_sq_yards
    elif unit.lower() == 'kanal':
        result = numeric_value * kanal_to_sq_yards
    else:
        raise ValueError("Unsupported unit. Supported units: 'Marla', 'Kanal'.")

    return int(result)

#url = "https://www.zameen.com/Residential_Plots/Karachi-2-2.html?area_min=62.709552&area_max=66.8901888&is_verified=true"

driver = webdriver.Chrome(options=chrome_options)
city = "Peshawar"
sq_yard = "auto"
max_pages = 20

dataset = []
unique_ids = []

for pg in range(1, (max_pages + 1)):

  #url = f"https://www.zameen.com/Residential_Plots/Karachi-2-{pg}.html?area_min=62.709552&area_max=418.06368000000003&is_verified=true"

  #url = f"https://www.zameen.com/Residential_Plots/Lahore-1-{pg}.html?area_min=62.709552&area_max=418.06368000000003&is_verified=true"

  url = f"https://www.zameen.com/Residential_Plots/Peshawar-17-{pg}.html?area_min=66.8901888&area_max=418.06368000000003&is_verified=true"

  # Navigate to a website
  driver.get(url)

  time.sleep(5)

  driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

  ##..........

  target_ul = WebDriverWait(driver, 10).until(
      EC.presence_of_element_located((By.XPATH, '//*[@id="body-wrapper"]/main/div[3]/div[2]/div[5]/div[1]/ul'))
  )

  # Extract all <li> elements from the <ul> using Selenium
  all_li = target_ul.find_elements(By.XPATH, '//li[@role="article"]')

  # Loop through each <li> element
  for li in all_li:

      # Scroll the target_ul into view again (if needed)
      driver.execute_script("arguments[0].scrollIntoView(true);", li)

      # Find the <article> element within the <li>

      try:
          article = li.find_element(By.TAG_NAME, 'article')
      except:
          #print('Not found article')
          continue
      # Do something with the article element (e.g., interact with it)


      if article:
          # Extract text from the <article> element

          try:
            price = article.find_element(By.XPATH, 'div[3]/div[2]/div[1]/div/div/div/div/div/span[3]')
            area = article.find_element(By.XPATH, "div[3]/div[2]/div[2]/div[2]/div/span/span/div/div/div/span")
            location = article.find_element(By.XPATH, "div[3]/div[2]/div[2]/div[1]")
            url = article.find_element(By.XPATH, "div[1]/a")
          except:
            continue

          # in zameen lahore, isl and other cities area is mentioned either in kanal or marla
          if 'marla' in area.text.lower() or 'kanal' in area.text.lower():
              area = convert_to_square_yards(area.text)
          else:
              area = area.text.split(' ')[0]


          
          price_int = parse_number_string(price.text)
          location = location.text.split(', ')
          project = location[0]
          town = location[1]

           
          # if town is not correctly mentioned
          if town.lower() == city.lower():
            continue


          # not allowing duplicate ads
          to_check = f"{price_int}-{area}-{town}"
         
          if to_check in unique_ids:
            continue

          unique_ids.append(to_check)


          print(price_int)
          print(area)
          print(project)
          print(town)
          print(url.get_attribute('href'))

          print("\n\n")

          plotData = {
              'url' : url.get_attribute('href'),
              'area': area,
              'location': town,
              'project' : project,
              'city' : city,
              'price': price_int,

          }

          dataset.append(plotData)




# save dataset
df = pd.DataFrame(dataset)
csv_file_path = f"{city}-{sq_yard}-dataset.csv"
df.to_csv(csv_file_path, index=False)

# Close the browser window
driver.quit()



