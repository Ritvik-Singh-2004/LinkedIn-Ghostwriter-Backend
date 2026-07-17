from fastapi import FastAPI

# init an app
app=FastAPI(title="LinkedIn GhostWriter Engine")

#GET method
@app.get("/")

def read_root():
    return {
        "status":"Online",
        "message":"Welcome to the LinkedIn GhostWriter API"
    }