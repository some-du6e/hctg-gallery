from playwright.sync_api import sync_playwright, Page
from dotenv import load_dotenv
import os
from time import sleep


def login(page: Page):
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



def initBrowser():
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False
        )
        page = browser.new_page()

        page = login(page)
        return page
    

def getGalleryPageProps(page: Page, pageNum: int):
    