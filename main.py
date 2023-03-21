from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import time

DRIVER_PATH = r"C:\Users\hp\Desktop\google-business-scrapper\chromedriver.exe"
CITIES = ["Mumbai", "Bangalore", "Delhi", "Gurgaon", "Noida", "Chennai"]

for city in CITIES:
    QUERY_URL = f"https://www.google.com/search?q=staffing+companies+in+{city.lower()}"
    
    try:
        driver = webdriver.Chrome(executable_path=DRIVER_PATH)
        driver.maximize_window()
        driver.get(QUERY_URL)
        
        try:
            search_btn = driver.find_element_by_xpath('//*[@id="Odp5De"]/div/div/div[2]/div[1]/div[2]/g-more-link/a')
            search_btn.click()
        except NoSuchElementException:
            search_btn = driver.find_element_by_xpath('//*[@class="CHn7Qb pYouzb"]')
            search_btn.click()
        except Exception as e:
            print(f'Error in {city} --> {e}')
            continue

        page = 1
        data = []
        
        
        while page < 11:
            print(f'******* Page {page} in {city} *******')
            time.sleep(5)
            businesses = driver.find_elements_by_xpath('//*[@class="cXedhc"]')
            
            if len(businesses) > 20:
                businesses = businesses[2:]

            for business in businesses:
                business.click()
                time.sleep(5)
                
                try:
                    name = driver.find_element_by_xpath('//*[@class="SPZz6b"]').text
                except:
                    continue
                try:
                    type = driver.find_element_by_xpath('//*[@class="YhemCb"]').text
                except:
                    type = 'NA'
                try:
                    review_count = driver.find_element_by_xpath('//*[@class="Ob2kfd"]//span[@class="RDApEe YrbPuc"]').text
                    review_count = review_count.translate({ord(i): None for i in '()'})
                except:
                    review_count = 'NA'
                try:
                    rating = driver.find_element_by_xpath('//*[@class="Ob2kfd"]//span[@class="yi40Hd YrbPuc"]').text
                except:
                    rating = 'NA'
                try:
                    address = driver.find_element_by_xpath('//*[@class="LrzXr"]').text
                except:
                    address = 'NA'
                try:
                    phone = driver.find_element_by_xpath('//*[@class="LrzXr zdqRlf kno-fv"]').text
                except:
                    phone = 'NA'
                try:
                    website = driver.find_element_by_xpath('//a[@class="dHS6jb"]').get_attribute('href')
                except:
                    website = 'NA'
                    
                
                # print(phone, website)
                data.append([name, type, rating, review_count, address, phone, website])
            
            try:
                next_page = driver.find_element_by_xpath('//*[@id="pnnext"]')
                next_page.click()
                page += 1
            except NoSuchElementException:
                break
    except Exception as e:
        print(f'Exception --> {e}')
        continue
    finally:
        driver.quit()

    try:
        my_df = pd.DataFrame(data)
        headerList=['Company','Type of Business','Rating','Review Count','Address','Phone','Website']
        file_name = f'staffing/{city}.csv'	
        my_df.to_csv(file_name, index=False, header=headerList)
    except Exception as e:
        print(f'Error in Pandas in {city} --> {e}')

