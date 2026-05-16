import components.galleryManagerBackend as be

def updateGalleryJSON():
    page = be.initBrowser()
    page.pause()
    page = be.getDatapage(page)


