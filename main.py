from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import time

DRIVER_PATH = r"C:\Users\hp\Downloads\chromedriver_win32\chromedriver.exe"
CITIES = ["India"]

for city in CITIES:
    QUERY = 'payroll contract staffing Engineering technical staffing businesses' # Write here what you want to search
    
    QUERY_URL = f"https://www.google.com/search?q={QUERY.lower().replace(' ', '+')}+in+{city.lower()}"
    
    try:
        driver = webdriver.Chrome(executable_path=DRIVER_PATH)
        driver.maximize_window()
        driver.get(QUERY_URL)
        time.sleep(5)
        
        try:
            search_btn = driver.find_element_by_xpath('//*[@class="CHn7Qb pYouzb"]')
            search_btn.click()
        except NoSuchElementException:
            search_btn = driver.find_element_by_xpath('//*[@id="rso"]/div[3]/div/div/div[1]/div[5]/div/div[1]/a/div')
            search_btn.click()
        except Exception as e:
            print(f'Error in {city} --> {e}')
            continue

        page = 1
        data = []
        
        
        while page < 11:
            print(f'******* Page {page} in {city} *******')
            time.sleep(5)
            businesses = driver.find_elements_by_xpath('//*[@data-test-id="organic-list-card"]')
            
            if len(businesses) > 20:
                businesses = businesses[2:]
                
            print(f'Found {len(businesses)} businesses')
            for business in businesses:
                print('Clicking')
                business.click()
                time.sleep(5)
                
                try:
                    name = driver.find_element_by_xpath('//*[@class="rgnuSb tZPcob"]').text
                except:
                    continue
                    
                
                print(name)
                data.append([name])
            
            try:
                next_page = driver.find_element_by_xpath('//*[@class="VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-INsAgc VfPpkd-LgbsSe-OWXEXe-dgl2Hf Rj2Mlf OLiIxf PDpWxe P62QJc LQeN7 sspfN Ehmv4e cLUxtc"]')
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
        headerList=['Company']
        file_name = f'companies.csv'	
        my_df.to_csv(file_name, index=False, header=headerList)
    except Exception as e:
        print(f'Error in Pandas in {city} --> {e}')

