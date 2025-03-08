from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

# Creamos la instancia de FastAPI
app = FastAPI()

# Montamos la carpeta "static" para servir los archivos HTML estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

# Simulamos una base de datos de usuarios con sus productos
fake_db = {
    "user1": {"password": "pass123", "product": "producto1"},
    "user2": {"password": "pass456", "product": "producto2"},
    "user3": {"password": "pass789", "product": "producto3"},
}

# Página de inicio (Login)
@app.get("/", response_class=HTMLResponse)
async def login_page():
    with open("static/index.html", "r", encoding="utf-8") as file:
        return HTMLResponse(content=file.read())

# Procesamos el login
@app.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):
    if username in fake_db and fake_db[username]["password"] == password:
        user_product = fake_db[username]["product"]
        return RedirectResponse(url=f"/static/panel-{user_product}.html", status_code=303)
    
    return HTMLResponse(content="Login failed", status_code=401)
