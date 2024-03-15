# sentianaylib (sentimental analysis library)

## Overview
This Python package, developed by Chameleonlabs.org, performs sentiment analysis on a web page based on a specified keyword.

## Developer Credits
This package was developed by:
Riyesh Poolanchalil (@riyeshp)
Rahul Poolanchalil (@rahulp_1986)

## Installation
You can install the package via pip:



## Usage
To use the package, import the `sentianaylib` class from the package and create an instance with the required driver. Then, call the `dataprocessor()` method with the URL,keyword and current_directory parameters.

```python
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from sentianaylib import sentianaylib

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

current_directory = os.path.dirname(os.path.abspath(__file__))
# Initialize sentianalib with the appropriate driver
sentianaylib_instance = sentianaylib(driver)

# Perform sentiment analysis on a webpage
url = 'https://example.com'
keyword = 'air pollution'
sentianaylib_instance.dataprocessor(url, keyword, current_directory)
```

## Parameters

url: The URL of the webpage to analyze.
keyword: The keyword to use for sentiment analysis.
current_directory: The location of main file where other related files can generated.

## Dependencies
This package relies on the following external libraries:

Beautiful Soup: For parsing HTML content.
TextBlob: For sentiment analysis.
Selenium: For automated web browsing.


## License
This package is licensed under the MIT License. See the LICENSE file for details.

## Issues
If you encounter any issues or have suggestions for improvement, please open an issue.