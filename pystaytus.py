from bs4 import BeautifulSoup
import requests
import time

# Four statuses:
    # "online" - site is up and respoonding and page is loading properly
    # "unstable" - site is responding but is taking longer than usual to respond
    # "down" - site is down (this includes timeouts, bad response codes, and page not loading properly)
    # "unknown" - something is wrong with the status checker (status checker did not work as intended)

STAYTUS_HEADERS = {
    'X-Auth-Token': '', # FILL IN THIS FIELD
    'X-Auth-Secret': '', # FILL IN THIS FIELD
    'Content-Type': 'application/json'
}
STAYTUS_URL = "" # URL to Staytus page ex. https://demo.staytus.co << NO trailing slash


def check_status(url, permalink, tag_to_find, attr_to_find, value_to_find):
    print("Checking status for " + url + "...")
    # get response code from site
    try:
        start = time.time()
        response = requests.get(url, timeout=20)
    except requests.exceptions.SSLError:
        set_status(permalink, "unstable")
    except requests.exceptions.RequestException: # some other error occurred
        print(url + " is down.")
        set_status(permalink, "down")
    except: # set to UNKNOWN
        print("Unable to determine status of " + url + "!")
        set_status(permalink, "unknown")
    else:
        page_load_time = time.time() - start
        print(response.status_code)
        if response.status_code != 200:
            set_status(permalink, "down")
        else: # use BeautifulSoup to check that the specified element loaded
            if not html_check(response.text, tag_to_find, attr_to_find, value_to_find):
                set_status(permalink, "down")
            else:
                if page_load_time > 5:
                    set_status(permalink, "unstable")
                else:
                    set_status(permalink, "online")
        print("Page took: " + str(page_load_time) + " to load.")


def html_check(html, tag_to_find, attr_to_find, value_to_find):
    soup = BeautifulSoup(html, features="html.parser")
    if not soup.find(tag_to_find, {attr_to_find: value_to_find}):
        return False
    else:
        return True


def set_status(permalink, status):
    print("Setting status of " + permalink + " to: " + status.upper())
    data = '{"service": "' + permalink + '", "status": "' + status + '"}'
    update_status = requests.post(STAYTUS_URL + "/api/v1/services/set_status", headers=STAYTUS_HEADERS, data=data).json()


def get_status(permalink):
    data = '{"service": "' + permalink + '"}'
    status = requests.post(STAYTUS_URL + "/api/v1/services/info", headers=STAYTUS_HEADERS, data=data).json()
    return status['data']['status']['permalink']


# example run
SERVICE1 = "https://google.com"
if get_status("google") != "maintenance":
    check_status(SERVICE1, "google", "div", "id", "lga")
