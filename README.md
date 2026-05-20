# Sistemas Programables - Firebase Realtime Database

## Integrantes del equipo
- Aguilar Figueroa José Miguel
- Liceaga Hernández Angel Baruc
- Ibarra Muñoz Jose Francisco
- Zacarías Hernández Angel David

## Objetivo del programa
Implementar un sistema de almacenamiento y visualización de datos utilizando Firebase como base de datos en la nube. 
El ESP32 envía datos del sensor LDR (intensidad de luz) y recibe comandos para controlar un LED desde un dashboard web en tiempo real. 
Este proyecto es la base tecnológica para el proyecto final "Sistema de Seguridad Inteligente para Ciclista" (SafeRide), donde se integrarán GPS, MPU6050 y cámara.

## Componentes utilizados en esta práctica
| Componente | Función |
|------------|---------|
| ESP32 | Microcontrolador principal |
| Sensor LDR | Monitoreo de luz ambiental (simula control de luces automáticas) |
| LED | Actuador controlable remotamente (simula tira LED RGB) |
| Firebase Realtime Database | Almacenamiento en nube y sincronización |

## Componentes del proyecto final (a integrar después)
- ESP32-CAM con OV2640 (registro visual)
- MPU6050 (detección de impactos y caídas)
- GPS Neo-6M (geolocalización)
- Tira LED RGB WS2812B (luces de posición)
- Buzzer activo (alertas sonoras)
- Pantalla OLED 0.96" (telemetría)

## Diagrama de conexiones

ESP32                    Modulo LDR
-----                    ----------
3.3V  ------------------> VCC
GND   ------------------> GND
GPIO34 ------------------> A0

ESP32                    LED

## Configuracion de Firebase

1. Crear proyecto en Firebase Console con nombre "Sistemas Programables"
2. Habilitar Realtime Database en modo prueba
3. Configurar reglas de seguridad:
   {
     "rules": {
       ".read": true,
       ".write": true
     }
   }
4. URL de la base de datos: https://sistemas-programables-71bb0-default-rtdb.firebaseio.com/
5. Registrar aplicacion web para obtener credenciales

## Estructura de la base de datos en Firebase

{
  "actuadores": {
    "led": 0
  },
  "estado": {
    "online": 1,
    "ultima_conexion": 1712345678
  },
  "sensores": {
    "LDR": {
      "raw": 2048,
      "porcentaje": 50
    }
  },
  "logs": {
    "eventos": {
      "-Nkf7gH3": {
        "tipo": "SISTEMA",
        "mensaje": "ESP32 iniciado",
        "timestamp": 1712345678
      }
    }
  }
}


## Funcionalidades implementadas

- Conexion WiFi y Firebase
- Control remoto de LED desde dashboard web
- Monitoreo de sensor LDR en tiempo real
- Estado Online/Offline del ESP32
- Historial de eventos con timestamps
- Dashboard responsive que se actualiza automaticamente

## Problemas encontrados y soluciones aplicadas (Analisis Individual)

### Integrante 1: Aguilar Figueroa Jose Miguel

Problema: Al crear el proyecto en Firebase, no entendia la diferencia entre Realtime Database y Firestore. 
Por error cree una base de datos Firestore y perdi tiempo intentando conectarla con el ESP32. Ademas, al 
configurar las reglas de seguridad, las puse incorrectamente y el ESP32 recibia errores 403 Forbidden.

Solucion: Despues de revisar la documentacion, identifique que debia usar Realtime Database, no Firestore. 
Aprendi que la URL de conexion cambia entre ambos servicios. Para las reglas, las configure con read true 
y write true en modo prueba, lo que resolvio el error 403. Tambien guarde la URL correcta en un bloc de notas para no perderla.

Conclusion: La creacion de proyectos en Firebase requiere atencion al detalle porque servicios similares 
tienen nombres confusos. Aprendi que Realtime Database es ideal para IoT por su sincronizacion en tiempo real, 
mientras Firestore es mejor para aplicaciones con consultas complejas. Para futuros proyectos, verificare primero 
el tipo de base de datos antes de comenzar a programar.

### Integrante 2: Liceaga Hernandez Angel Baruc

Problema: Durante la configuracion de Firebase, no encontraba la API Key necesaria para el dashboard web. 
Busque en varias secciones de la consola sin exito. Ademas, al generar la clave privada para el proyecto, 
no sabia que archivo debia usar y cual era la diferencia entre la clave de la app web y la clave administrativa.

Solucion: Descubri que la API Key para aplicaciones web se encuentra en Configuracion del proyecto, en la pestaña General, 
dentro de la seccion Tus aplicaciones. Aprendi que para el dashboard HTML debo usar la configuracion de la app web, 
no la clave privada administrativa que se usa para servidores. Genere una nueva app web llamada Dashboard y copie todos los valores al archivo HTML.

Conclusion: Firebase maneja diferentes tipos de credenciales para diferentes propositos. La API Key para web es publica y 
segura de usar en el frontend, mientras la clave administrativa debe mantenerse secreta. Esta distincion es fundamental 
para la seguridad del proyecto. Entender esto me ayuda a no mezclar credenciales en el futuro.

### Integrante 3: Ibarra Muñoz Jose Francisco

Problema: El ESP32 se conectaba al WiFi correctamente pero no podia enviar datos a Firebase. Los errores indicaban que la respuesta HTTP no era 200. 
Probe cambiando la URL varias veces y verificando la conexion a internet, pero el problema persistia. Tambien note que a veces el ESP32 
se reiniciaba solo al intentar enviar datos.

Solucion: El problema era que la URL de Firebase no terminaba con diagonal al final. Agregue el slash al final de la URL en la variable 
FIREBASE_URL y el ESP32 comenzo a enviar datos exitosamente. Para el reinicio, descubri que las excepciones no estaban manejadas correctamente. 
Agregue bloques try catch en todas las funciones de red y aumente el timeout de conexion a 20 segundos.

Conclusion: La comunicacion con servicios en la nube desde el ESP32 requiere manejo robusto de errores. Un simple slash al final de una URL puede 
ser la diferencia entre exito y fracaso. Ademas, el ESP32 es sensible a errores de red y puede reiniciarse si no se capturan las excepciones. 
En proyectos futuros implementare un sistema de reconexion automatica WiFi.

### Integrante 4: Zacarias Hernandez Angel David

Problema: El dashboard web mostraba los datos del LDR correctamente pero no respondia a los botones de control del LED. Al hacer clic en Encender, 
no pasaba nada y el LED no se encendia. Revise la consola del navegador y no aparecian errores, pero los datos no cambiaban en Firebase. 
El estado del LED siempre aparecia como Desconocido.

Solucion: Descubri que el problema era que en el archivo HTML las referencias a Firebase no coincidian con la estructura que el ESP32 estaba 
creando en la base de datos. El ESP32 guardaba el LED en actuadores/led, pero el dashboard intentaba leer de actuadores/LED con mayuscula. 
Corregi la ruta en el JavaScript para que coincidiera exactamente con lo que escribia el ESP32. Tambien verifique que el metodo .set() se ejecutaba correctamente.

Conclusion: La sincronizacion entre ESP32 y dashboard web depende completamente de que las rutas en Firebase sean identicas en ambos lados. 
Una diferencia en mayusculas o minusculas rompe toda la comunicacion. Aprendi a usar la consola de Firebase para verificar la estructura de datos en tiempo real y depurar estos problemas rapidamente. Tambien aprendi a usar la consola del navegador para ver los errores de comunicacion.

## Evidencias

- Firebase Realtime Database mostrando los datos recibidos del ESP32
- Dashboard web mostrando el estado Online del sistema
- Dashboard web controlando el LED (encendido y apagado)
- Sensor LDR mostrando cambios en tiempo real al tapar el sensor
- Historial de eventos con timestamps en la seccion de alertas

## Checklist de entrega

- [x] Enlace al Repositorio
- [x] Firebase Operativo
- [x] Eventos con Timestamp
- [x] Dashboard Funcional
- [x] Control Remoto
- [x] Garantia de Privacidad
- [x] Analisis Individual

## Enlaces

- Repositorio GitHub: https://github.com/DavidHernandez13/sistemas-programables-firebase
- Firebase Console: https://sistemas-programables-71bb0-default-rtdb.firebaseio.com/

## Fecha de entrega

19 de Mayo de 2026
