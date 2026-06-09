from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, Request
import components.jsonManager as jm
from pathlib import Path
import random

router = APIRouter()
BASE_DIR = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

sidebar_links = [
    {
        "name": "Home",
        "href": "/",
        "icon": "data:image/svg+xml,%3csvg%20width='100%25'%20height='100%25'%20overflow='visible'%20style='display:%20block;'%20viewBox='0%200%2030%2027'%20fill='none'%20xmlns='http://www.w3.org/2000/svg'%3e%3cpath%20id='Home%20Icon'%20fill-rule='evenodd'%20clip-rule='evenodd'%20d='M16.8418%200.607337C16.3152%200.213711%2015.667%200%2014.9999%200C14.3327%200%2013.6845%200.213711%2013.1579%200.607337L0.582144%2010.0045C-0.545833%2010.8505%200.0751541%2012.5872%201.50463%2012.5872H3.00009V24.1174C3.00009%2024.8819%203.31616%2025.6151%203.87876%2026.1557C4.44135%2026.6963%205.2044%2027%206.00003%2027H13.4999V16.9111C13.4999%2016.5288%2013.6579%2016.1622%2013.9392%2015.8919C14.2205%2015.6216%2014.602%2015.4698%2014.9999%2015.4698C15.3977%2015.4698%2015.7792%2015.6216%2016.0605%2015.8919C16.3418%2016.1622%2016.4998%2016.5288%2016.4998%2016.9111V27H23.9997C24.7953%2027%2025.5583%2026.6963%2026.1209%2026.1557C26.6835%2025.6151%2026.9996%2024.8819%2026.9996%2024.1174V12.5872H28.4951C29.9231%2012.5872%2030.547%2010.8505%2029.4176%2010.0059L16.8418%200.607337Z'%20fill='var(--fill-0,%20black)'/%3e%3c/svg%3e"
    },
    {
        "name": "Gallery",
        "href": "/gallery",
        "icon": "data:image/svg+xml,%3csvg%20width='100%25'%20height='100%25'%20overflow='visible'%20style='display:%20block;'%20viewBox='0%200%2028%2028'%20fill='none'%20xmlns='http://www.w3.org/2000/svg'%3e%3cpath%20id='Compass%20Icon'%20d='M14%200C21.7322%200%2028%206.2678%2028%2014C28%2021.7322%2021.7322%2028%2014%2028C6.2678%2028%200%2021.7322%200%2014C0%206.2678%206.2678%200%2014%200ZM19.9402%208.0598C19.4446%207.5656%2013.0102%209.0496%2011.0306%2011.0306C9.051%2013.0102%207.5656%2019.4446%208.0598%2019.9402C8.5554%2020.4344%2014.9898%2018.9504%2016.9694%2016.9694C18.9504%2014.9898%2020.4344%208.5554%2019.9402%208.0598ZM14%2012.6C14.3713%2012.6%2014.7274%2012.7475%2014.9899%2013.0101C15.2525%2013.2726%2015.4%2013.6287%2015.4%2014C15.4%2014.3713%2015.2525%2014.7274%2014.9899%2014.9899C14.7274%2015.2525%2014.3713%2015.4%2014%2015.4C13.6287%2015.4%2013.2726%2015.2525%2013.0101%2014.9899C12.7475%2014.7274%2012.6%2014.3713%2012.6%2014C12.6%2013.6287%2012.7475%2013.2726%2013.0101%2013.0101C13.2726%2012.7475%2013.6287%2012.6%2014%2012.6Z'%20fill='var(--fill-0,%20black)'/%3e%3c/svg%3e"
    },
    {
        "name": "Lookup",
        "href": "https://hackclub.enterprise.slack.com/archives/C0B5SA3SKJL",
        "icon": "data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20viewBox%3D%220%200%20512%20512%22%3E%3C!--!Font%20Awesome%20Free%20v7.2.0%20by%20%40fontawesome%20-%20https%3A%2F%2Ffontawesome.com%20License%20-%20https%3A%2F%2Ffontawesome.com%2Flicense%2Ffree%20Copyright%202026%20Fonticons%2C%20Inc.--%3E%3Cpath%20d%3D%22M416%20208c0%2045.9-14.9%2088.3-40%20122.7L502.6%20457.4c12.5%2012.5%2012.5%2032.8%200%2045.3s-32.8%2012.5-45.3%200L330.7%20376C296.3%20401.1%20253.9%20416%20208%20416%2093.1%20416%200%20322.9%200%20208S93.1%200%20208%200%20416%2093.1%20416%20208zM208%20352a144%20144%200%201%200%200-288%20144%20144%200%201%200%200%20288z%22%2F%3E%3C%2Fsvg%3E"
    }

]
def balance():
    return random.randint(0, 100)

@router.get("/")
async def home(request: Request):
    return templates.TemplateResponse(request, "home.html", {"sidebarlinks": sidebar_links, "page": "Home", "featured_projects": jm.getFeaturedProjects(), "balance": balance()})

@router.get("/gallery")
async def gallery(request: Request):
    return templates.TemplateResponse(request, "gallery.html", {"sidebarlinks": sidebar_links, "page": "Gallery", "balance": balance()})


@router.get("/api/projects/html/{page_num}")
def project_page_html(page_num: str, request: Request):
    projectos = jm.getGalleryPage(page_num)
    return templates.TemplateResponse(request, "page.html", {"projects": projectos, "next_page": int(page_num)+1, "iflast_page": len(projectos) < 12})