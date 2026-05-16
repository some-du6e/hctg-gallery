import components.galleryManagerBackend as be


def updateGalleryJSON(say=None):
    if say:
        say("Initializing browser...")
    
    page = be.initBrowser(say)
    page.pause()

    page, data = be.getDatapage(page)
    page.pause()
    
    if say:
        say("Done updating the gallery! 🎉")


