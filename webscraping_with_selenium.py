import re, json, time, argparse, sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

# local path to the driver (please change it to your local driver path)
PATH = "chromedriver.exe"
service = Service(PATH)
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(service= service, options=options)



# I added an additional argument "contact", which is set to Kontakt for accessing the contact page
# This gives the user the chance to change it to "contact" if the search in enlgish
def scrape_emails(entity_name: str, contact="Kontakt"):
    """
    function that accepts one entity name
    :param entity_name: search word "string"
    :param contact: alternative search if home page returns none
    :return: list of emails if found or empty list
    """
    driver.get("https://www.google.com/")
    driver.implicitly_wait(5)
    # google request to accept cookies before using. If logged in to google then remove the next 2 lines
    accept_cookies = driver.find_element(By.ID, "L2AGLb")
    accept_cookies.click()
    # get search bar in google .com and search for the entity name then wait 3 seconds (next 5 lines)
    search_bar = driver.find_element(By.NAME, "q")
    search_bar.send_keys(entity_name)
    driver.implicitly_wait(3)
    search_bar.send_keys(Keys.RETURN)
    driver.implicitly_wait(3)
    # get the first link of the search result
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    links = []
    search = soup.find_all('div', class_="yuRUbf")
    for h in search:
        links.append(h.a.get('href'))
    # open the first link of results and wait 5 seconds
    driver.get(links[0])
    driver.implicitly_wait(5)
    # get the page source to look for emails
    page_source = driver.page_source
    # regular expression to find emails
    EAMIL_REGEX = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    # look for all emails and save them in the out put list
    emails = []
    for match in re.finditer(EAMIL_REGEX, page_source):
        emails.append(match.group())
    # check if we got any emails
    if len(emails) != 0:
        return emails
    # try to find contact page to see if there are emails there
    else:
        try:
            contact_page = driver.find_element(By.LINK_TEXT, contact)
            contact_page.click()
            page_source = driver.page_source
            for match in re.finditer(EAMIL_REGEX, page_source):
                emails.append(match.group())
            return emails
        except:
            return emails

# same as the function above but without accepting google condition. I will use it to run multiple quries
def scrape_emails_without_accepting_google_cookies(entity_name: str, contact="Kontakt"):
    """
    function that accepts one entity name
    :param entity_name: search word "string"
    :param contact: alternative search if home page returns none
    :return: list of emails if found or empty list
    """
    driver.get("https://www.google.com/")
    driver.implicitly_wait(5)
    # get search bar in google .com and search for the entity name then wait 3 seconds (next 5 lines)
    search_bar = driver.find_element(By.NAME, "q")
    search_bar.send_keys(entity_name)
    driver.implicitly_wait(3)
    search_bar.send_keys(Keys.RETURN)
    driver.implicitly_wait(3)
    # get the first link of the search result
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    links = []
    search = soup.find_all('div', class_="yuRUbf")
    for h in search:
        links.append(h.a.get('href'))
    # open the first link of results and wait 5 seconds
    driver.get(links[0])
    driver.implicitly_wait(5)
    # get the page source to look for emails
    page_source = driver.page_source
    # regular expression to find emails
    EAMIL_REGEX = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    # look for all emails and save them in the out put list
    emails = []
    for match in re.finditer(EAMIL_REGEX, page_source):
        emails.append(match.group())
    # check if we got any emails
    if len(emails) != 0:
        return emails
    # try to find contact page to see if there are emails there
    else:
        try:
            contact_page = driver.find_element(By.LINK_TEXT, contact)
            contact_page.click()
            page_source = driver.page_source
            for match in re.finditer(EAMIL_REGEX, page_source):
                emails.append(match.group())
            return emails
        except:
            return emails


# I used the "scrape_emails" function inside this one to save repeating code
def scrape_emails_multiple_names(entity_names: list):
    """
    function that accepts lists of entity names and output the results as json file
    :param entity_names: list of nams entity
    :return: None "wrties into json file as output"
    """
    result_dic = {}
    for name in entity_names:
        if name == entity_names[0]:
            try:
                emails = scrape_emails(name)
                unique_emails = []
                for email in emails:
                    if email not in unique_emails:
                        unique_emails.append(email)
                result_dic[name] = unique_emails
                time.sleep(2)
            except:
                pass
        else:
            try:
                emails = scrape_emails_without_accepting_google_cookies(name)
                unique_emails = []
                for email in emails:
                    if email not in unique_emails:
                        unique_emails.append(email)
                result_dic[name] = unique_emails
                time.sleep(2)
            except:
                pass
    with open("results.json", "w") as outfile:
        json.dump(result_dic, outfile)
    return None

def create_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='program that merge pdf files into one file')
    parser.add_argument('input_file',
                        help='text input file with name entities',
                        type=argparse.FileType("r"),
                        default=[sys.stdin])
    return parser

def main():
    parser = create_argument_parser()
    args = parser.parse_args()
    names_list = []
    for line in args.input_file:
        names_list.append(line.strip())
    scrape_emails_multiple_names(names_list)
    driver.quit()


if __name__ == '__main__':
    main()
