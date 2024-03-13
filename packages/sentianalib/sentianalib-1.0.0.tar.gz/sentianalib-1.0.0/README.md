# sentianalib (sentimental analysis library)

## Overview
This Python package, developed by Riyesh Poolanchalil and Rahul Poolanchalil, performs sentiment analysis on a web page based on a specified keyword.

## Installation
You can install the package via pip:



## Usage
To use the package, import the `sentianalib` class from the package and create an instance with the required driver. Then, call the `dataprocessor()` method with the URL and keyword parameters.

```python
from sentianalib import sentianalib

# Initialize sentianalib with the appropriate driver
sentianalib = sentianalib()

# Perform sentiment analysis on a webpage
url = 'https://example.com'
keyword = 'air pollution'
sentianalib.dataprocessor(url, keyword)
```

## Parameters

url: The URL of the webpage to analyze.
keyword: The keyword to use for sentiment analysis.

## Dependencies
This package relies on the following external libraries:

Beautiful Soup: For parsing HTML content.
TextBlob: For sentiment analysis.
Selenium: For automated web browsing.

## License
This package is licensed under the MIT License. See the LICENSE file for details.

## Issues
If you encounter any issues or have suggestions for improvement, please open an issue.