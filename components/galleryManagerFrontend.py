import components.galleryManagerBackend as be

def fakeSay(message: str):
    print(message)


def updateGalleryJSON(say=fakeSay):
    
    page = be.initBrowser(say)
    
    page, pages = be.getPageAmount(page, say)

    print(pages)
    
    say("Done updating the gallery! 🎉")


