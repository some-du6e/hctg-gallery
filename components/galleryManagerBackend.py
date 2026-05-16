from playwright.sync_api import sync_playwright, Page
from dotenv import load_dotenv
import os
from time import sleep
import json

# Keep Playwright instance alive at module level
_playwright = None
_browser = None
_page = None

def getDatapage(page: Page) -> tuple[Page, dict]:
    page.wait_for_load_state("domcontentloaded", timeout=10000)

    appDiv = page.locator("#app")
    rawData = appDiv.get_attribute("data-page")
    if rawData is None:
        raise ValueError("data-page attribute is missing or empty")
    data = json.loads(rawData)
    props = data["props"]
    print(data["props"]["user"]["first_name"])
    return page, props



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
    if page.url != ("https://game.hackclub.com/auth/hca"):
        page.goto("https://game.hackclub.com/auth/hca")

    page.wait_for_load_state("domcontentloaded", timeout=10000)

    

    passedurl = page.url == "https://game.hackclub.com/home"
    passedlogin = page.get_by_text("Nice!Successfully logged in!").is_visible()

    if passedurl and passedlogin:
        print("Logged in successfully!")
        return page
    

def initBrowser() -> Page:
    global _playwright, _browser, _page
    _playwright = sync_playwright().start()
    _browser = _playwright.chromium.launch(
        headless=False
    )
    _page = _browser.new_page()
    _page = hcaLogin(_page)
    _page = hctgLogin(_page)
    if _page is None:
        raise RuntimeError("Browser page initialization failed")
    return _page
    


def getPageAmount(page: Page):
    pass

def getGalleryPageProps(page: Page, pageNum: int):
    pass


