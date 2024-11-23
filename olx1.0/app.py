from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return """
    <!DOCTYPE html>
    <html>
    <head><title>OLX Monitoring App</title></head>
    <body>
        <h1>OLX Monitoring App</h1>
        <p>Welcome to the OLX Monitoring Application. Backend is running!</p>
    </body>
    </html>
    """
