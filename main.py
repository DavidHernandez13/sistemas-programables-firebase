"""
OBJETIVO: Gestión de Firebase y Dashboard de usuario para monitoreo de sensor LDR y control remoto de LED.
INTEGRANTES: 
- Aguilar Figueroa José Miguel
- Liceaga Hernández Angel Baruc
- Ibarra Muñoz Jose Francisco
- Zacarías Hernández Angel David
PROYECTO: Sistemas Programables - Firebase Realtime Database
"""

import network
import time
import urequests
import ujson
from machine import Pin, ADC

# ========== CONFIGURACIÓN - CAMBIA ESTOS DATOS ==========
SSID = "Hernandez_2.4G"           # <--- CAMBIA
PASSWORD = "11702184"  # <--- CAMBIA
FIREBASE_URL = "https://sistemas-programables-71bb0-default-rtdb.firebaseio.com/"  # <--- CAMBIA (copia tu URL)

# ========== PINES DE LOS COMPONENTES ==========
PIN_LED = 2        # LED integrado del ESP32 (o externo en GPIO2)
PIN_LDR = 34       # Sensor LDR (entrada analógica)
PIN_DHT = 23       # Sensor DHT11 (datos en GPIO23)

# ========== INICIALIZAR COMPONENTES ==========
led = Pin(PIN_LED, Pin.OUT)
ldr = ADC(Pin(PIN_LDR))
ldr.atten(ADC.ATTN_11DB)  # Para leer de 0 a 3.3V

# Inicializar DHT11
try:
    import dht
    dht_sensor = dht.DHT11(Pin(PIN_DHT))
    tiene_dht = True
    print("Sensor DHT11 detectado")
except:
    tiene_dht = False
    print("No se pudo importar DHT11. Solo funcionará el LDR.")

# ========== CONEXIÓN WIFI ==========
def conectar_wifi():
    print("\nConectando a WiFi", end="")
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    
    timeout = 20
    while not wlan.isconnected() and timeout > 0:
        print(".", end="")
        time.sleep(0.5)
        timeout -= 1
    
    if wlan.isconnected():
        print("\n✅ Conectado! IP:", wlan.ifconfig()[0])
        return True
    else:
        print("\n❌ No se pudo conectar")
        return False

# ========== LEER SENSORES ==========
def leer_ldr():
    valor = ldr.read()
    # Convertir a porcentaje (0-4095 -> 0-100%)
    porcentaje = int((valor / 4095) * 100)
    return valor, porcentaje

def leer_dht():
    if not tiene_dht:
        return None, None
    try:
        dht_sensor.measure()
        temp = dht_sensor.temperature()
        hum = dht_sensor.humidity()
        return temp, hum
    except:
        return None, None

# ========== ENVIAR DATOS A FIREBASE ==========
def enviar_a_firebase(ruta, valor):
    try:
        url = FIREBASE_URL + ruta + ".json"
        datos = ujson.dumps(valor)
        respuesta = urequests.put(url, data=datos)
        respuesta.close()
        return True
    except Exception as e:
        print(f"Error enviando {ruta}: {e}")
        return False

# ========== LEER COMANDO DEL LED DESDE FIREBASE ==========
def leer_comando_led():
    try:
        url = FIREBASE_URL + "/actuadores/led.json"
        respuesta = urequests.get(url)
        if respuesta.status_code == 200:
            if respuesta.text and respuesta.text != "null":
                valor = ujson.loads(respuesta.text)
                if valor == 1:
                    led.value(1)
                    print("🔆 LED ENCENDIDO por comando remoto")
                    return "encendido"
                else:
                    led.value(0)
                    print("⚫ LED APAGADO por comando remoto")
                    return "apagado"
        respuesta.close()
    except Exception as e:
        print(f"Error leyendo LED: {e}")
    return None

# ========== REGISTRAR EVENTO EN LOG ==========
def registrar_evento(tipo, mensaje):
    try:
        import time as t
        # Usar el timestamp de Firebase
        from urequests import post
        import ujson
        
        evento = {
            "tipo": tipo,
            "mensaje": mensaje,
            "timestamp": t.time()  # timestamp Unix
        }
        url = FIREBASE_URL + "/logs/eventos.json"
        respuesta = post(url, data=ujson.dumps(evento))
        respuesta.close()
    except Exception as e:
        print(f"Error registrando evento: {e}")

# ========== PROGRAMA PRINCIPAL ==========
print("\n" + "="*50)
print("SISTEMAS PROGRAMABLES - ESP32 CON FIREBASE")
print("="*50)

# Conectar WiFi
if not conectar_wifi():
    print("No se pudo conectar. Reinicia el ESP32.")
    while True:
        time.sleep(1)

# Configurar URL de Firebase (para este ejemplo no usamos librería externa)
print("\n📡 Conectando a Firebase...")

# Crear estructura inicial en Firebase
enviar_a_firebase("/actuadores/led", 0)
enviar_a_firebase("/estado/online", 1)
registrar_evento("SISTEMA", "ESP32 iniciado correctamente")

# Variables de control
ultimo_envio_sensores = 0
INTERVALO_SENSORES = 10  # segundos entre lecturas
contador_heartbeat = 0

print("\n" + "="*50)
print("✅ SISTEMA OPERATIVO")
print("="*50)
print("📊 Sensores que se enviarán cada 10 segundos:")
print("   - LDR (luz)")
if tiene_dht:
    print("   - DHT11 (temperatura y humedad)")
print("\n💡 Actuadores controlables:")
print("   - LED (GPIO2) mediante comando remoto")
print("\n" + "-"*50)
print("👉 Ve a la consola de Firebase y cambia:")
print("   actuadores/led = 1 para encender")
print("   actuadores/led = 0 para apagar")
print("-"*50 + "\n")

while True:
    try:
        # 1. REVISAR SI HAY COMANDOS DEL LED (siempre)
        estado_led = leer_comando_led()
        
        # 2. ENVIAR SENSORES CADA 10 SEGUNDOS
        tiempo_actual = time.time()
        if tiempo_actual - ultimo_envio_sensores >= INTERVALO_SENSORES:
            
            # Leer LDR
            valor_raw, porcentaje = leer_ldr()
            enviar_a_firebase("/sensores/LDR/raw", valor_raw)
            enviar_a_firebase("/sensores/LDR/porcentaje", porcentaje)
            print(f"📊 LDR: {valor_raw} ({porcentaje}%)")
            
            # Leer DHT11 si está disponible
            if tiene_dht:
                temp, hum = leer_dht()
                if temp is not None:
                    enviar_a_firebase("/sensores/DHT/temperatura", temp)
                    enviar_a_firebase("/sensores/DHT/humedad", hum)
                    print(f"🌡️  Temperatura: {temp}°C | Humedad: {hum}%")
                    
                    # Si temperatura es alta, generar alerta
                    if temp > 30:
                        registrar_evento("ALERTA", f"Temperatura alta: {temp}°C")
                        print("⚠️ ALERTA: Temperatura alta!")
                    elif temp < 15:
                        registrar_evento("ALERTA", f"Temperatura baja: {temp}°C")
                        print("⚠️ ALERTA: Temperatura baja!")
            
            # Enviar heartbeat (está vivo)
            enviar_a_firebase("/estado/ultima_conexion", time.time())
            enviar_a_firebase("/estado/online", 1)
            
            ultimo_envio_sensores = tiempo_actual
            contador_heartbeat = 0
            print("--- Datos enviados a Firebase ---\n")
        else:
            # Heartbeat cada 30 segundos
            contador_heartbeat += 1
            if contador_heartbeat >= 30:
                enviar_a_firebase("/estado/ultima_conexion", time.time())
                enviar_a_firebase("/estado/online", 1)
                contador_heartbeat = 0
        
        time.sleep(1)
        
    except Exception as e:
        print(f"Error en loop principal: {e}")
        time.sleep(5)