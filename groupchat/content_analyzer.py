# filename: content_analyzer.py
import requests
from bs4 import BeautifulSoup

def analyze_content(url):
    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content of the webpage
        soup = BeautifulSoup(response.content, 'html.parser')

        # Print the title of the webpage
        print("Title:", soup.title.string)

        # Print the first paragraph of the webpage
        print("First paragraph:")
        for paragraph in soup.find_all('p'):
            print(paragraph.text)
            break

    else:
        print("Failed to retrieve the webpage.")

# Execute the function
url = "https://www.ndtv.com/india-news/nitish-kumars-folded-hands-response-to-lalu-yadavs-doors-open-remark-7383348"
analyze_content(url)