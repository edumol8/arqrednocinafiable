# # Simulación de Red No Confiable con Cliente–Servidor TCP (Banco y Tienda)

Este proyecto implementa un sistema **cliente–servidor** simple en Python para simular:

- Comunicación por **sockets TCP**.
- **Pérdida de paquetes** en la red (fallos de red simulados).
- **Reintentos** del cliente cuando no recibe confirmación del servidor.

La historia es:

- `banco_servidor.py` actúa como un **banco** que tiene un saldo y procesa operaciones de débito.
- `tienda_cliente.py` actúa como una **tienda** que solicita restar 100 del saldo del banco.
- La “red” es poco confiable: a veces el servidor ignora el mensaje y no responde, simulando una red con pérdida de paquetes.

---

## Estructura del proyecto

- **`banco_servidor.py`**  
  Servidor TCP que:
  - Escucha en `127.0.0.1:65432`.
  - Mantiene una variable de estado `saldo` que comienza en 500.
  - Recibe mensajes desde el cliente.
  - Simula fallos de red con una probabilidad configurable (por defecto 90%).
  - Si el mensaje contiene `"RESTAR_100"` y no hay fallo simulado:
    - Resta 100 al saldo.
    - Imprime el nuevo saldo.
    - Envía un **ACK** al cliente (`OK_CONFIRMADO`).

- **`tienda_cliente.py`**  
  Cliente TCP que:
  - Se conecta al servidor en `127.0.0.1:65432`.
  - Envía el mensaje `"CLIENTE_A_RESTAR_100"`.
  - Espera respuesta del servidor con un **timeout** de 2 segundos.
  - Si no recibe confirmación, **reintenta** el envío.
  - Tras agotar los intentos sin respuesta, declara que la operación falló.

---

## Requisitos

- **Python 3.x** instalado.
- Sistema operativo con soporte para sockets (Windows, Linux, macOS).
- No se necesitan librerías externas: solo se usan módulos estándar:
  - `socket`
  - `random`
  - `time`

---

## Cómo ejecutar el proyecto

> ⚠️ Primero se ejecuta el **servidor** y luego el **cliente**.

### 1. Ejecutar el servidor (Banco)

En una terminal, estando en la carpeta del proyecto:

```bash
python banco_servidor.py

Si todo está bien, deberías ver algo similar a:
Banco (Servidor) esperando en 127.0.0.1:65432. Saldo inicial: $500

En otra terminal, también en la carpeta del proyecto:
```bash
python tienda_cliente.py

La salida del cliente podría ser algo como:
--- Intento 1 ---
ENVIADO: CLIENTE_A_RESTAR_100
--- ⚠️ Timeout. Asumiendo paquete perdido. Re-enviando... ---

--- Intento 2 ---
ENVIADO: CLIENTE_A_RESTAR_100
👍 Recibida la confirmación. Transacción exitosa.


Mientras tanto, en la terminal del servidor podrías ver:
Banco (Servidor) esperando en 127.0.0.1:65432. Saldo inicial: $500
Conexión de: ('127.0.0.1', 54321)

RECIBIDO: CLIENTE_A_RESTAR_100
--- 🔴 ¡FALLA DE RED SIMULADA! Ignorando el paquete. ---

RECIBIDO: CLIENTE_A_RESTAR_100
✅ Transacción procesada. Nuevo saldo: $400


Este proyecto es una mini simulación de un banco (servidor) y una tienda (cliente) comunicándose sobre una red no confiable:

La tienda envía una orden para restar 100 del saldo del banco.

El banco procesa la orden solo cuando la “red” no falla.

El cliente usa timeout + reintentos para incrementar la probabilidad de que la operación llegue y se confirme.

Sirve como ejercicio práctico para entender cómo los sistemas distribuidos deben manejar los problemas clásicos de redes: mensajes perdidos, necesidad de confirmaciones y reintentos.


