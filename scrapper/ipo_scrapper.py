from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import sys


def trim_date(date):
    """Remove the time from the date string"""
    return date.split(' ')[0]

def scrap_table(driver, tableId ):
    table_datas = []
     # find the table containing the IPO information
    table = driver.find_element(By.ID, tableId)
    # find all rows in the table
    rows = table.find_elements(By.TAG_NAME, 'tr')
    # skip the first row (header row)
    for row in rows[1:]:
        # find all cells in the row
        cells = row.find_elements(By.TAG_NAME, 'td')
        # extract the information from the cells
        symbol = cells[1].find_element(By.TAG_NAME, 'a').text
        company = cells[2].find_element(By.TAG_NAME, 'a').text
        if tableId == 'myTableErs':
            ratio = cells[3].text
            unit = cells[4].text
            price = cells[5].text
            opening_date = cells[6].text
            closing_date = cells[7].text
            issue_manager = cells[10].text
        else:
            unit = cells[3].text
            price = cells[4].text
            opening_date = cells[5].text
            closing_date = cells[6].text
            issue_manager = cells[9].text


        # create an IPO object with the extracted information
        if tableId == 'myTableErs':
            ipo = {
                'symbol': symbol,
                'company': company,
                'ratio': ratio,
                'unit': unit,
                'price': price,
                'opening_date': opening_date,
                'closing_date': closing_date,
                'issue_manager': issue_manager,
            }
        else:
            ipo = {
                'symbol': symbol,
                'company': company,
                'unit': unit,
                'price': price,
                'opening_date': opening_date,
                'closing_date': closing_date,
                'issue_manager': issue_manager,
            }
    
        table_datas.append(ipo)
    return table_datas


def scrap_upcoming_ipos(driver, url):
    print('Scraping upcoming ipos from {}'.format(url))
    # empty list to store IPO objects
    ipos = []
    driver.get(url)
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "ipo"))
    )
    ipo_list =  scrap_table(driver, 'myTableEip')


    driver.find_element(By.LINK_TEXT, "Right Share").click()
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//*[@id='myTableErs']/tbody/tr"))
    )
    right_share_list = scrap_table(driver, 'myTableErs')



    driver.find_element(By.LINK_TEXT, "FPO").click()
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//*[@id='myTableEfp']/tbody/tr"))
    )
    fpo_list = scrap_table(driver, 'myTableEfp')


    driver.find_element(By.LINK_TEXT, "IPO-Local").click()
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//*[@id='myTableEipl']/tbody/tr"))
    )
    ipo_local = scrap_table(driver, 'myTableEipl')


    driver.find_element(By.LINK_TEXT, "Mutual Fund").click()
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//*[@id='myTableEmf']/tbody/tr"))
    )
    mutual_fund = scrap_table(driver, 'myTableEmf')

    driver.find_element(By.LINK_TEXT, "Bonds/Debentures").click()
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//*[@id='myTableEbd']/tbody/tr"))
    )
    bonds_debentures = scrap_table(driver, 'myTableEbd')


    driver.find_element(By.LINK_TEXT, "IPO to Migrant Workers").click()
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//*[@id='myTableEim']/tbody/tr"))
    )
    ipo_to_migrant_workers = scrap_table(driver, 'myTableEim')
    

    #create key value pair for the list

    ipos = {
        'ipo_list': ipo_list,
        'right_share_list': right_share_list,
        'fpo_list': fpo_list,
        'ipo_local': ipo_local,
        'mutual_fund': mutual_fund,
        'bonds_debentures': bonds_debentures,
        'ipo_to_migrant_workers': ipo_to_migrant_workers
    }
    return ipos 


def main():

    url = 'https://www.sharesansar.com/existing-issues'
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