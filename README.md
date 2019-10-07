# pystaytus
A real-time site status checker written in Python for use with Staytus. https://github.com/adamcooke/staytus
# What Checks Are Performed
1. Response Time
2. HTTP Status Code Check
3. Checks to make sure a specific HTML element that should always be present is present
# Installation
pystaytus uses the BeautifulSoup Python library. Install with `pip`:
```
pip install bs4
```
# Setup
Fill in your Staytus API token and secret by visiting `/admin/api_tokens` on your Staytus admin page:
```python
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
- `url`: the site URL you want to check the status of (e.g. https://google.com)
- `permalink`: The permalink to the service on Staytus (you can check this for each of your services @ `/admin/services`)

The following three parameters are related to the HTML check on the site. Say, for example, I want to check to make sure that a specific element on is rendering properly on my site, Google. I will pick an element that should always show in the HTML when Google is loaded. Using inspect element, I found the following element:
```html
<div id="lga">...</div>
```
I would fill in the rest of the following parameters as follows:
- `tag_to_find`: `div`
- `attr_to_find`: `id`
- `value_to_find`: `lga`
Example:
```python
check_status("https://google.com", "google", "div", "id", "lga"
```
## Automating with `cron`
The following will check your service(s') statuses every minute:
```
* * * * * /path/to/python /path/to/pystaytus.py > /dev/null
```
