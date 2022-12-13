from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import json


def trim_date(date):
    """Remove the time from the date string"""
    return date.split(' ')[0]

def scrap_upcoming_ipos(driver, url):
    # empty list to store IPO objects
    ipos = []
    driver.get(url)

    # wait for the page to load
    driver.implicitly_wait(10)
    # find the table containing the IPO information
    table = driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_divIPO')

    # find all rows in the table
    rows = table.find_elements(By.TAG_NAME, 'tr')

    # skip the first row (header row)
    for row in rows[1:]:
        # find all cells in the row
        cells = row.find_elements(By.TAG_NAME, 'td')

        # extract the information from the cells
        company = cells[0].find_element(By.TAG_NAME, 'a').get_attribute('title')
        quantity = cells[1].text
        type = cells[2].text
        open_date = cells[3].text
        close_date = cells[4].text
        issue_manager = cells[5].text
        status = cells[6].text

        # # process the dates
        open_date = trim_date(open_date)
        close_date = trim_date(close_date)

        # create an IPO object with the extracted information
        ipo = {
            'company': company,
            'quantity': quantity,
            'type': type,
            'open_date': open_date,
            'close_date': close_date,
            'issue_manager': issue_manager,
            'status': status,
        }
    
        ipos.append(ipo)
    return ipos
    


def main():

    url = 'http://www.merolagani.com'
    options = Options()
    options.headless = True
   
    driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(120)
    ipo_list = scrap_upcoming_ipos(driver, url)

    # save ipo_list to a json file. Remove duplicate files if any
    with open('ipo_list.json', 'w') as f:
        json.dump(ipo_list, f, indent=2)

    driver.quit()

if __name__ == "__main__":
    main()