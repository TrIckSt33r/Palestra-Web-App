from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from core.database import get_db
from models import user, course, shop, fitness

from routers import fitness as router_fitness

app = FastAPI(title="GymCloud Sinergy", version="1.0.0")


app.include_router(router_fitness.router)

@app.get("/")
def read_root():
    return {"status": "online", "message": "Backend pronto e router fitness attivo!"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {
        "status": "online", 
        "message": "Il backend della palestra è pronto e i modelli sono caricati!"
    }

@app.get("/test-db")
def test_db(db: Session = Depends(get_db)):
    try:
        # Esegue una query di test per vedere se MySQL risponde
        db.execute(text("SELECT 1"))
        return {"status": "success", "message": "Connessione a MySQL (XAMPP) riuscita e modelli verificati!"}
    except Exception as e:
        return {"status": "error", "message": f"Errore di connessione: {str(e)}"}