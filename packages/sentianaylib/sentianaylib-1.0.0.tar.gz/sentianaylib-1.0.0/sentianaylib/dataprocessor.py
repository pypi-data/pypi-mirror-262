import os
import time
from bs4 import BeautifulSoup
from textblob import TextBlob
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService


class sentianaylib:
    def __init__(self, driver):
        self.driver = driver

    def dataprocessor(self, url, keyword,current_directory):
        # Initialize the WebDriver with the downloaded ChromeDriver
        driver = webdriver.Chrome(self.chrome_driver_path)

        # Open the webpage
        self.driver.get(url)

        # Get initial page height
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        print(last_height)

        time.sleep(2)
        # Scroll down and wait for some time for more content to load
        while True:
            # Scroll down to the bottom
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # Wait for some time to let the page load
            time.sleep(2)
            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                # If heights are the same, no more new content is loaded, exit the loop
                break
            last_height = new_height

        # Get the HTML content of the page
        html_content = self.driver.page_source

        # Save the HTML content into a file
        output_file_path = os.path.join(current_directory, 'output.html')
        with open(output_file_path, 'w+', encoding='utf-8') as output_file:
            output_file.write(html_content)

        # Close the WebDriver
        self.driver.quit()
        input_file_path = 'output.html'
        with open(input_file_path, 'r+', encoding='utf-8') as input_file:
            html_content = input_file.read()


        # Parse the HTML content
        soup = BeautifulSoup(html_content, 'html.parser')

        search_word = keyword
        # Find all <a> tags with href attribute
        links = soup.find_all('a', href=True)

        # Word to search for in the link text

        # Log file path
        log_file_path = 'log.txt'
        matching_file_path = 'matching_links.txt'
        non_matching_file_path = 'non_matching_links.txt'
        sentiments = []
        total_score = 0


        # Open files for writing
        with open(matching_file_path, 'w', encoding='utf-8') as matching_file, \
            open(non_matching_file_path, 'w', encoding='utf-8') as non_matching_file:

        # Loop through each link
            for link in links:
                # Check if the link text contains the search word
                if search_word in link.text.lower():
                    # Print the href attribute and the link text
                    print('URL:', link['href'])
                    print('Text:', link.text.strip())
                    print()
                    analysis = TextBlob(link.text.strip())
                    sentiment_score = analysis.sentiment.polarity
                    total_score = total_score + sentiment_score
                    if sentiment_score > 0:
                        sentiment = 'Positive'
                    elif sentiment_score < 0:
                        sentiment = 'Negative'
                    else:
                        sentiment = 'Neutral'
                    print('Sentiment:', sentiment)
                    print()
                    matching_file.write(f'sentiment_score:{sentiment_score}, sentiment: {sentiment}, text: {link.text.strip()}\n')
                else:
                    non_matching_file.write(f'Non-Matching Link Text: {link.text.strip()}\n')
            if total_score > 0:
                print(f'The word {search_word} is positive today' )
            elif total_score < 0:
                print(f'The word {search_word} is Negative today' )
            else:
                print(f'The word {search_word} is neutral today' )


        pass

if __name__ == "__main__":
    print("Library file cant be run individually")
