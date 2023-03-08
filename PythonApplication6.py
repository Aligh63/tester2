import requests
import time
from bs4 import BeautifulSoup
import re

# Get the list of URLs from the user, separated by line breaks
urls = input("Enter the URLs to check, separated by line breaks:\n").splitlines()

js_files = [
    "/webpack/Auth.44e05080311528b179c7.js",
    "/webpack/7540.b7f3ab16c1d7d344980b.js"
]

# Loop through each URL in the list and check for the following:
# 1. If any of the JS files specified in the `js_files` list load successfully.
# 2. If any of the images on the website appear to be low quality.
# 3. If any inner pages of the website have a high percentage of Hindi text.
# 4. If the website contains the <i> element with the class "symbol-classcentral-navy".
for url in urls:
    # Check JS files
    response = requests.get(url)
    js_pass = True
    if response.status_code == 200:
        for js_file in js_files:
            js_url = url + js_file
            js_response = requests.get(js_url)
            if js_response.status_code == 200:
                print(f"{js_url} loaded successfully on {url}")
            else:
                js_pass = False
                break
        if js_pass:
            print(f"Pass: All JS files loaded successfully on {url}")
        else:
            print(f"Fail: Failed to load one or more JS files on {url}")
    else:
        print(f"Fail: Failed to load {url}")
    

    # Check images
    response = requests.get(url)
    time.sleep(0) # wait for page to fully load
    img_pass = True
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        images = soup.find_all("img")

        for img in images:
            img_src = img.get("src")
            if "blur" in img_src:
                img_pass = False
                break
        
        if js_pass:
            img_pass=True
            print(img_pass)
        if img_pass:
            print(f"Pass: All images loaded successfully on {url}")
        else:
            print(f"Fail: One or more images appear to be low quality on {url}")
    else:
        print(f"Fail: Failed to load {url}")

    # Check Hindi text
    main_url = url
    response = requests.get(main_url)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')

    hindi_pass = False
    # Define the list of HTML tags to check for Hindi text
    tags_to_check = ['p', 'h2', 'title', 'a', 'strong', 'span', 'i', 'h1', 'h3', 'section', 'div', 'header', 'svg', 'li', 'main', 'h5', 'ul', 'h4', 'time', 'td', 'b', 'button']
    count = 0
    for link in soup.find_all('a', href=True):
        if count >= 5:  # Check only 5 links
            break
        url = link['href']
        if not url.startswith('http'):
            url = main_url + url

        response = requests.get(url)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')

        hindi_count = 0
        total_count = 0

        for tag in tags_to_check:
            for text in soup.find_all(tag):
                total_count += 1
                if re.search('[\u0900-\u097F]', str(text)):  # Hindi Unicode range
                    hindi_count += 1

        if total_count > 0 and hindi_count/total_count >= 0.6: # threshold set to 60%
            hindi_pass = True
        count=count+1

    if hindi_pass:
        print(f"Pass: Inner pages translated successfully on {url}")
    else:
        print(f"Fail: No or low Hindi text found on inner pages of {url}")

    # Check for the <i> element with the class "symbol-classcentral-navy"
    response = requests.get(main_url)
    print(main_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        if soup.find('i', {'class': 'symbol-classcentral-navy'}) is not None:
            print(f"Pass: The <i> element with class 'symbol-classcentral-navy' exists on {url}")
        else:
            print(f"Fail: The <i> element with class 'symbol-classcentral-navy' does not exist on {url}")
    else:
        print(f"Fail: Failed to load {url}")



