The code is designed to analyze a web page on the Russian Wikipedia, extract internal and external links, and display 
them in a readable format. It utilizes the requests, BeautifulSoup, and urllib.parse libraries. Three different 
solutions are provided for this task.

### First Solution:

1. Sends a GET request to the web page.
2. Parses the HTML code using BeautifulSoup.
3. Extracts all links (<a> tags) on the page.
4. Separates links into internal and external by checking for the presence of a domain in the URL.
5. Stores the links in a `defaultdict(set)`, where the keys represent link types (internal or external) and the values 
6. are sets of unique links.
6. Prints the list of internal and external links, decoding URL-encoded characters.

### Second Solution:

1. Sends a GET request to the web page.
2. Parses the HTML code using BeautifulSoup.
3. Extracts all links (<a> tags) on the page.
4. Separates links into internal and external by checking for the presence of a domain in the URL.
5. Stores internal and external links in separate sets.
6. Prints the list of internal and external links, decoding URL-encoded characters.

### Third Solution:

1. Sends a GET request to the web page.
2. Parses the HTML code using BeautifulSoup.
3. Extracts all links (<a> tags) on the page.
4. Separates links into internal and external by checking for the presence of a domain in the URL.
5. Uses functions to fetch the page content, extract links, and print them.
6. Prints the list of internal and external links, decoding URL-encoded characters.

All three solutions perform similar tasks of separating links into internal and external categories and displaying the 
results in a readable format, but they use different approaches for storing and processing the information.
