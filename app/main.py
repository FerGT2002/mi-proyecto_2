from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

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

# Clase para los datos enviados por el ESP32
class ADCData(BaseModel):
    esp_id: str
    adc_value: float

# Diccionario en memoria para almacenar los valores de ADC de cada ESP32
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

# Procesamos el login
@app.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):
    if username in fake_db and fake_db[username]["password"] == password:
        user_product = fake_db[username]["product"]
        return RedirectResponse(url=f"/static/panel-{user_product}.html", status_code=303)
    
    return HTMLResponse(content="Login failed", status_code=401)

# Endpoint para recibir datos del ADC (POST)
@app.post("/api/adc")
async def receive_adc_data(data: ADCData):
    # Guardamos el valor del ADC para el ESP correspondiente
    if data.esp_id in adc_data:
        adc_data[data.esp_id] = data.adc_value
        print(f"Valor del ADC recibido de {data.esp_id}: {data.adc_value}")
        return {"status": "success", "esp_id": data.esp_id, "adc_value": data.adc_value}
    
    return {"status": "error", "message": "ESP ID no válido"}

# Endpoint para obtener el valor del ADC de un ESP específico (GET)
@app.get("/api/adc/{esp_id}")
async def get_adc_value(esp_id: str):
    if esp_id in adc_data:
        return {"esp_id": esp_id, "adc_value": adc_data[esp_id]}
    
    return {"status": "error", "message": "ESP ID no válido"}

