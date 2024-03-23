import time
import os
import threading
import webbrowser
from fastapi import FastAPI, Path, Query, Depends, HTTPException, Request, status
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn

from sqlalchemy import text
from sqlalchemy.orm import Session

from db.database import get_db
from routes import contacts

app = FastAPI()

static_files_path = os.path.join(os.path.dirname(__file__), "static")
print("STATIC: ", static_files_path)
app.mount("/static", StaticFiles(directory=static_files_path), name="static")

templates_path = os.path.join(os.path.dirname(__file__), "templates")
templates = Jinja2Templates(directory=templates_path)

@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    try:
        context = {"request": request, "title": "Home Page"}
        return templates.TemplateResponse("index.html", context)
    except Exception as e:
        print(f"Error rendering template: {e}")
        raise

@app.get("/api/healthchecker")
def healthchecker(db: Session = Depends(get_db)):
    try:
        # Make request
        result = db.execute(text("SELECT 1")).fetchone()
        if result is None:
            raise HTTPException(
                status_code=500, detail="Database is not configured correctly"
            )
        return {"message": "Welcome to FastAPI on Howe Work 11!"}
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error connecting to the database",
        )

app.include_router(contacts.router, prefix="/api")

# Function to open the web browser
def open_browser():
    webbrowser.open("http://localhost:9000")

if __name__ == "__main__":
    # Start the web browser in a separate thread
    threading.Thread(target=open_browser).start()
    # Run the FastAPI application
    uvicorn.run("main:app", host="0.0.0.0", port=9000, reload=True)
