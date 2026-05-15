from playwright.sync_api import sync_playwright, Page
from dotenv import load_dotenv
import os
from time import sleep
import json

# Keep Playwright instance alive at module level
_playwright = None
_browser = None
_page = None


def hcaLogin(page: Page):
    session_token_cookie = os.environ.get("session_token")
    signed_user_token = os.environ.get("signed_user")
    if signed_user_token != None:
        cookies_to_add = [
            {
                "name": "signed_user",
                "value": signed_user_token,
                "url": "https://auth.hackclub.com/"
            },
            {
                "name": "session_token",
                "value": session_token_cookie,
                "url": "https://auth.hackclub.com/"
            }
        ]
        page.context.add_cookies(cookies_to_add) # type: ignore

    page.goto("https://auth.hackclub.com/")
    if signed_user_token != None:
        sleep(1.5)
    else:
        input("Log in and press enter when your done...")
    return page


def hctgLogin(page: Page):
    



def initBrowser():
    global _playwright, _browser, _page
    _playwright = sync_playwright().start()
    _browser = _playwright.chromium.launch(
        headless=False
    )
    _page = _browser.new_page()
    _page = login(_page)
    return _page
    

def getGalleryPageProps(page: Page, pageNum: int):
    pass


