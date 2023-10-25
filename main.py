
import requests
from bs4 import BeautifulSoup
import spacy

# Take input from the user
user_input = input("Enter the text to check for plagiarism: ")

# Split the input into sentences using spaCy
nlp = spacy.load("en_core_web_sm")
doc = nlp(user_input)
sentences = [sent.text for sent in doc.sents]

# Perform the plagiarism check
results = []
for sentence in sentences:
    # Send a GET request to Bing with double quotes around the sentence

    search_url = f'https://www.bing.com/search?q=%22{sentence}%22&qs=n&form=QBRE&sp=-1&lq=0&pq=%22harry+potter%22&sc=10-14&sk=&cvid=581F2DF588F849CFB7E568A8C3B4B686&ghsh=0&ghacc=0&ghpl='
    print(search_url)
    headers = { "author":"www.bing.com",
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Mobile Safari/537.36"
                }

    # Add Bing request headers
    response = requests.get(search_url, headers=headers)

    # Get website URLs from search results
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        search_results = soup.find_all('h2')
        urls = [result.a['href'] for result in search_results if result.a]

    # Request websites' content
    website_contents = {}
    for url in urls:
        try:
            website_response = requests.get(url)
            if website_response.status_code == 200:
                website_contents[url] = website_response.text
        except Exception as e:
            # Handle exceptions if a website can't be accessed
            continue

    # Find exact matches in the website content
    found_match = False
    for url, content in website_contents.items():
        if sentence in content:
            result = {
                "website urls": url,
                "match": "found",
                "context": sentence
            }
            found_match = True
            break

    if not found_match:
        result = {
            "website urls": "No matching websites found",
            "match": "not found",
            "context": sentence
        }
    results.append(result)

#  Return the results (You can use a web framework like FastAPI to create an API)

# Print the results (you can return these via an API)
for result in results:
    print(result)
