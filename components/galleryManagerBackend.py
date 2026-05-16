from playwright.sync_api import sync_playwright, Page
from dotenv import load_dotenv
import os
from time import sleep
import json

# Keep Playwright instance alive at module level
_playwright = None
_browser = None
_page = None

def fakeSay(message: str):
    print(message)


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



def hcaLogin(page: Page, say=fakeSay):
    say("hcaLogin: adding cookies from .env...")
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
    say("hcaLogin: going to hca auth page")
    if signed_user_token != None:
        sleep(0.75)
    else:
        say("hcaLogin: :bang: NOT LOGGED IN :bang: ")
        input("Log in and press enter when your done...")

    say("hcaLogin: everything lgtm, returning page")
    return page


def hctgLogin(page: Page, say=fakeSay):
    if page.url != ("https://game.hackclub.com/auth/hca"):
        say("hctgLogin: not on hca auth page, going there now...")
        page.goto("https://game.hackclub.com/auth/hca")

    page.wait_for_load_state("domcontentloaded", timeout=10000)

    

    passedurl = page.url == "https://game.hackclub.com/home"
    passedlogin = page.get_by_text("Nice!Successfully logged in!").is_visible()

    if passedurl and passedlogin:
        say("hctgLogin: yeah lgtm its logged in, returning page")
        return page
    

def initBrowser(say=fakeSay) -> Page:
    global _playwright, _browser, _page
    say("initBrowser: starting playwright...")
    _playwright = sync_playwright().start()
    _browser = _playwright.chromium.launch(
        headless=False
    )
    say("initBrowser: starting new page")
    _page = _browser.new_page()
    say("initBrowser: logging with hca")
    _page = hcaLogin(_page, say)
    say("initBrowser: logging to hctg")
    _page = hctgLogin(_page, say)

    say("initBrowser: returning page")
    if _page is None:
        raise RuntimeError("Browser page initialization failed")
    return _page
    


def getPageAmount(page: Page):
    pass

def getGalleryPageProps(page: Page, pageNum: int):
    pass


