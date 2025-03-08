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
    # Servimos el archivo estático del login
    with open("static/index.html", "r") as file:
        return HTMLResponse(content=file.read())

# Procesamos el login
@app.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):
    # Validamos el usuario y la contraseña
    if username in fake_db and fake_db[username]["password"] == password:
        user_product = fake_db[username]["product"]
        # Redirigimos a la página correspondiente dependiendo del producto
        if user_product == "producto1":
            return RedirectResponse(url="/static/panel-producto1.html")
        elif user_product == "producto2":
            return RedirectResponse(url="/static/panel-producto2.html")
        elif user_product == "producto3":
            return RedirectResponse(url="/static/panel-producto3.html")
    return HTMLResponse(content="Login failed", status_code=401)
