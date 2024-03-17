import time 
import os

import pandas as pd 
from selenium import webdriver 
from selenium.webdriver import Chrome 
from selenium.webdriver.chrome.service import Service 
from selenium.webdriver.common.by import By 
from webdriver_manager.chrome import ChromeDriverManager
import pickle

# Create a new instance of the Chrome driver
# start by defining the options 
options = webdriver.ChromeOptions() 
options.headless = False # it's more scalable to work in headless mode 
# normally, selenium waits for all resources to download 
# we don't need it as the page also populated with the running javascript code. 
options.page_load_strategy = 'none' 
# this returns the path web driver downloaded 
chrome_path = ChromeDriverManager().install() 
chrome_service = Service(chrome_path) 
# pass the defined options and service objects to initialize the web driver 
driver = Chrome(options=options, service=chrome_service) 
driver.implicitly_wait(15)

url = "https://web.uri.edu/catalog/#/courses" 
 
driver.get(url) 
time.sleep(10)

content = driver.find_element(By.CSS_SELECTOR, "div[id*='__KUALI_TLP']")
# print(content.text)
print('----------------------------')


# Get a list of the URLs for information on each class.
urls = [] # IMPORTANT: I probably missed some links here and added some unnecessary ones...
if os.path.exists("course-detail-urls"):
    print("Loading course URLs from file...")
    # Load the URLs from a pickled file.
    with open("course-detail-urls", "rb") as fp:   # Unpickling
        # Filter out links the main page.
        urls = pickle.load(fp)
        # urls = list(filter(lambda x: x == 'https://web.uri.edu/catalog/#/courses?', urls)) # TODO: Get classes between BIO and CVE rows... they were missed. Picking up from a previous run.
        
else:
    print("Gathering course URLs...")
    topic_buttons = content.find_elements(By.CSS_SELECTOR, "button[class*='md-btn--icon']")
    print(len(topic_buttons))

    # click all the buttons to get all dropdowns
    for button in topic_buttons:
        try:
            button.click()
            time.sleep(0.25)
        except Exception as e:
            print(e)
            pass
    time.sleep(20)

    links = driver.find_elements(By.TAG_NAME, "a")
    print("# Links: ", len(links))

    # If no file available, gather a list of URLs.
    url_counter = 0
    for l in links[55:]:
        _url = l.get_attribute('href')
        if _url != 'https://web.uri.edu/catalog/#/courses?':
            urls.append(_url)
            url_counter += 1
        if url_counter % 100 == 0:
            print(f"URLs found: {url_counter}. Total: {len(urls)}")

    print("Pickling course URLs to a file...")
    with open("course-detail-urls", "wb") as fp:   #Pickling
        pickle.dump(urls, fp)

print(f"URLs total: {len(urls)}")
print("URLs: ", urls)

for counter, _url in enumerate(urls):
    pre_df_dict = {
        'link': [],
        'who': [],
        'what': [],
        'when': [], 
    }
    try:
        pre_df_dict['link'].append(_url)
        driver.get(_url)
        time.sleep(0.25)

        _content = driver.find_element(By.CSS_SELECTOR, "div[id*='__KUALI_TLP']")
        course_name = _content.find_element(By.CSS_SELECTOR, "h2").text
        titles = _content.find_elements(By.CSS_SELECTOR, "h3[class*='course-view__label___FPV12']")
        info = _content.find_elements(By.CSS_SELECTOR, "div[class*='course-view__pre___2VF54']")
        what_str = "Course name: " + course_name + '\n'
        for i in range(len(titles)):
            what_str += titles[i].text + ': ' + info[i].text + '\n'
        print(what_str)
        pre_df_dict['what'].append(what_str)

        pre_df_dict['who'] = 'University of Rhode Island College of ' + info[3].text

        pre_df_dict['when'] = '2022-2023'

        # Save the data from this course to a CSV file.
        existing_df = pd.read_csv('uri_courses.csv')
        _df = pd.DataFrame.from_dict(pre_df_dict)
        combined_df = pd.concat([existing_df, _df], ignore_index=True)
        combined_df.to_csv('uri_courses.csv', index=False)
    except Exception as e:
        print(e)
        pass

