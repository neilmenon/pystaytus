# pystaytus
A real-time site status checker written in Python for use with Staytus. https://github.com/adamcooke/staytus
# What Checks Are Performed
1. Response Time
2. HTTP Status Code Check
3. Checks to make sure a specific HTML element that should always be present is present
# Setup
Fill in your Staytus API token and secret by visiting `/admin/api_tokens` on your Staytus admin page:
```
STAYTUS_HEADERS = {
    'X-Auth-Token': '', # FILL IN THIS FIELD
    'X-Auth-Secret': '', # FILL IN THIS FIELD
    'Content-Type': 'application/json'
}
```
On `/admin/service_statuses`, match your statuses to the following, which are used by pystaytus. Especially make sure the permalinks match up:
```
Name: Online | Permalink: "online" | site is up and respoonding and page is loading properly
Name: Unstable | Permalink: "unstable" | site is responding but is taking longer than usual to respond
Name: Down | Permalink: "down" | site is down (this includes timeouts, bad response codes, and page not loading properly)
Name: Unknown | Permalink: "unknown" | something is wrong with the status checker (status checker did not work as intended)
[OPTIONAL] Name: Maintenance | Permalink: "maintenance"
```
# Usage
Run the `check_status` function, which works as described below:
```
check_status(url, permalink, tag_to_find, attr_to_find, value_to_find)
```
- url: 
# Installation
pystaytus uses the BeautifulSoup Python library. Install with `pip`:
```
pip install bs4
```
