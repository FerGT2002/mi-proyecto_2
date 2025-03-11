from fastapi import FastAPI, Form, Response, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Instancia de FastAPI
app = FastAPI()

# Configuración de CORS (Evita bloqueos en navegadores móviles)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir cualquier origen
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Servir archivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

# Base de datos simulada de usuarios
fake_db = {
    "user1": {"password": "pass123", "product": "producto1"},
    "user2": {"password": "pass456", "product": "producto2"},
    "user3": {"password": "pass789", "product": "producto3"},
}

# Diccionario en memoria para almacenar valores del ADC
adc_data = {
    "esp1": 0.0,
    "esp2": 0.0,
    "esp3": 0.0
}

# Página de inicio (Login)
@app.get("/", response_class=HTMLResponse)
async def login_page():
    with open("static/index.html", "r", encoding="utf-8") as file:
        return HTMLResponse(content=file.read())

# Procesar el login y devolver una cookie de sesión
@app.post("/login")
async def login(response: Response, username: str = Form(...), password: str = Form(...)):
    if username in fake_db and fake_db[username]["password"] == password:
        user_product = fake_db[username]["product"]

        # Guardamos la sesión en una cookie
        response.set_cookie(key="user", value=username, httponly=True, max_age=3600)

        return JSONResponse(
            content={"message": "Login exitoso", "redirect_url": f"/static/panel-{user_product}.html"},
            status_code=200
        )
    
    raise HTTPException(status_code=401, detail="Login failed")

# Verificar sesión antes de permitir el acceso al panel
@app.get("/check-session")
async def check_session(request: Request):
    user = request.cookies.get("user")
    if user and user in fake_db:
        return {"status": "ok", "user": user}
    return {"status": "error", "message": "No autorizado"}

# Modelo para recibir datos del ADC
class ADCData(BaseModel):
    esp_id: str
    adc_value: float

# Recibir datos del ADC (POST)
@app.post("/api/adc")
async def receive_adc_data(data: ADCData):
    if data.esp_id in adc_data:
        adc_data[data.esp_id] = data.adc_value
        print(f"Valor del ADC recibido de {data.esp_id}: {data.adc_value}")
        return {"status": "success", "esp_id": data.esp_id, "adc_value": data.adc_value}
    
    return {"status": "error", "message": "ESP ID no válido"}

# Obtener el valor del ADC de un ESP específico (GET)
@app.get("/api/adc/{esp_id}")
async def get_adc_value(esp_id: str):
    if esp_id in adc_data:
        return {"esp_id": esp_id, "adc_value": adc_data[esp_id]}
    
    return {"status": "error", "message": "ESP ID no válido"}
