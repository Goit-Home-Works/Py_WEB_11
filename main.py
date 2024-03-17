from fastapi import FastAPI

app = FastAPI()


@app.get("/api/healthchecker")
def root():
    return {"message": "Welcome to FastAPI!"}


@app.get("/notes/{note_id}")
async def read_note(note_id: int):
    return {"note": note_id}
