import requests
from bs4 import BeautifulSoup
import time
import json
import re

#functions for retries mechanism and data scrapping 
def fetch_data_with_retries(url, retries=3, delay=2):
    """
    fetching data from url with retries in case of failure! 
    """
    for attempt in range(retries):
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1} failed : {e}")
            if attempt < retries - 1:
                time.sleep(delay * (attempt + 1))  #exponential backoff
            else:
                raise

#function to extract data from beautifulsoup and regular expression
def extract_data_from_html(html_content):
    """
    Extracting the relevant data (all the links containing python in it) from the html content
    """
    if not html_content :
        raise ValueError("Html Content is not available or valid!!")
    
    soup = BeautifulSoup(html_content, 'html.parser')
    titles = []

    #Regular expression to find all the links conating python 
    for link in soup.find_all('a', href=True):
        title = link.get_text()
        if re.match(r'.*python.*', title , re.IGNORECASE):  #looking for links containing python
            titles.append(title) 
    return titles
    
#function to save data in json format
def save_data_to_json(data, filename="scrapped_data.json"):
    """
    saved the extracted data to json file
    """
    try:
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)
        print(f"Data has been saved to {filename}")
    except Exception as e:
        print(f"Error in saving data as json file : {e}")

#URL to scrapp
url = "https://docs.python.org/3/"

#fetch, extract and save the data in json format
html_content = fetch_data_with_retries(url)
extracted_data = extract_data_from_html(html_content)
save_data_to_json(extracted_data)

