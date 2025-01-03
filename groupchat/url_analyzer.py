# filename: url_analyzer.py
import urllib.parse

def analyze_url(url):
    # Parse the URL
    parsed_url = urllib.parse.urlparse(url)
    
    # Print the URL components
    print("URL:", url)
    print("Scheme:", parsed_url.scheme)
    print("Netloc:", parsed_url.netloc)
    print("Path:", parsed_url.path)

    # Check if the URL is from a known news website
    known_news_websites = ["ndtv.com", "bbc.com", "cnn.com", "aljazeera.com"]
    if parsed_url.netloc in known_news_websites:
        print("The URL is from a known news website.")
    else:
        print("The URL is not from a known news website.")

# Execute the function
url = "https://www.ndtv.com/india-news/nitish-kumars-folded-hands-response-to-lalu-yadavs-doors-open-remark-7383348"
analyze_url(url)