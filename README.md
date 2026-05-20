# Sistemas Programables - Firebase Realtime Database

## Integrantes del equipo
- Aguilar Figueroa José Miguel
- Liceaga Hernández Angel Baruc  
- Ibarra Muñoz Jose Francisco
- Zacarías Hernández Angel David

## Objetivo del programa
Implementar un sistema de almacenamiento y visualización de datos utilizando Firebase como base de datos en la nube. 
El ESP32 envía datos del sensor LDR (intensidad de luz) y recibe comandos para controlar un LED desde un dashboard web en tiempo real. 
Este proyecto es la base tecnológica para el proyecto final "Sistema de Seguridad Inteligente para Ciclista"(SafeRide), donde se integrarán GPS, MPU6050 y cámara.

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

