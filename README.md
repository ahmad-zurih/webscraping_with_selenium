# webscraping_with_selenium

This program perform webscraping to extract emails from list of name entities using selenium.

The program takes a text file with a name entity at each line and returns json file
with the name entity and the email found by performing google search on that name entity.

###### required non-standard library packages:

- selenium
- bs4 


###### Notes

- The dirver works only with chrome version 103. If you have a different version you need to download different driver.
- If you use different browser, lines 9 to 13 need to be changed depending on the browser
