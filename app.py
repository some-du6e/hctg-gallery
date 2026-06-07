import components.slack as slack
import components.api as api
import threading
import uvicorn

def startApi():
    uvicorn.run(api.app, host="127.0.0.1", port=8000, reload=False)

if __name__ == "__main__":
    apiThread = threading.Thread(target=startApi)
    
    apiThread.start()
    slack.start()

    print("dont forget to do shit fat chud")