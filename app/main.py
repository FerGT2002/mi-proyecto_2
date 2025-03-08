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

# Clase para el formato de datos del ADC
class ADCData(BaseModel):
    adc_value: float

# Simulamos un valor en memoria para el ADC
adc_data = ADCData(adc_value=0.0)


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
    # Guardar el valor del ADC
    adc_data.adc_value = data.adc_value  # Actualizamos el valor en memoria
    print(f"Valor del ADC recibido: {adc_data.adc_value}")

    return {"status": "success", "adc_value": adc_data.adc_value}

# Endpoint para obtener el valor del ADC (GET)
@app.get("/api/adc", response_model=ADCData)
async def get_adc_value():
    # Regresamos el valor actual del ADC
    return adc_data
