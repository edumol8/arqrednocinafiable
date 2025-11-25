import socket        # Importa el módulo 'socket' para trabajar con conexiones de red (TCP/IP)
import random        # Importa el módulo 'random' para generar números aleatorios (se usa para simular fallos de red)
import time          # Importa el módulo 'time' para poder usar pausas (sleep) y simular tiempo de procesamiento

# Variable para llevar la cuenta del dinero
saldo = 500          # Define la variable 'saldo' con un valor inicial de 500, representando el dinero en el "banco"

HOST = '127.0.0.1'   # IP Local: '127.0.0.1' es la dirección de loopback (la misma máquina)
PORT = 65432         # Puerto de comunicación donde el servidor va a escuchar conexiones

# Crea un socket TCP utilizando IPv4
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:  # Crea el socket 's' y asegura que se cierre al final del bloque
    s.bind((HOST, PORT))  # Asocia el socket a la IP y al puerto definidos (HOST, PORT)
    s.listen()            # Pone el socket en modo escucha, preparado para aceptar conexiones entrantes
    print(f"Banco (Servidor) esperando en {HOST}:{PORT}. Saldo inicial: ${saldo}")  # Muestra un mensaje indicando que el servidor está listo

    conn, addr = s.accept()  # Acepta una conexión entrante; 'conn' es el nuevo socket para esa conexión y 'addr' es la dirección del cliente
    with conn:               # Usa 'with' para asegurar que la conexión se cierre correctamente al salir del bloque
        print(f"Conexión de: {addr}")  # Imprime la dirección del cliente que se ha conectado
        while True:                    # Bucle infinito para seguir recibiendo mensajes mientras el cliente esté conectado
            data = conn.recv(1024)     # Recibe hasta 1024 bytes de datos desde el cliente
            if not data:               # Si no se recibe nada (data está vacío), significa que el cliente cerró la conexión
                break                  # Sale del bucle 'while' y termina la comunicación
            
            mensaje = data.decode()    # Decodifica los bytes recibidos a texto (string) usando UTF-8 por defecto
            print(f"\nRECIBIDO: {mensaje}")  # Muestra en pantalla el mensaje recibido desde el cliente
            
            # --- SIMULACIÓN DEL ERROR DE RED (PAQUETE PERDIDO) ---
            if random.random() < 0.9:  # Genera un número aleatorio entre 0 y 1; si es menor que 0.9 (90% de probabilidad) se simula un fallo
                print("--- 🔴 ¡FALLA DE RED SIMULADA! Ignorando el paquete. ---")  # Indica que se simuló una falla de red
                # No enviamos ACK (Acknowledge/Confirmación), simulando pérdida.
                continue               # Vuelve al inicio del bucle 'while' sin procesar el mensaje ni enviar confirmación

            # Si el paquete no se pierde, se procesa
            if "RESTAR_100" in mensaje:   # Verifica si el texto "RESTAR_100" aparece dentro del mensaje recibido
                saldo -= 100              # Resta 100 al saldo (simula una transacción de débito de 100)
                print(f"✅ Transacción procesada. Nuevo saldo: ${saldo}")  # Muestra el nuevo saldo después de la transacción
                conn.sendall(b"OK_CONFIRMADO")  # Envía al cliente una respuesta en bytes indicando que la operación fue confirmada

            time.sleep(0.5)  # Pausa la ejecución 0.5 segundos para simular tiempo de procesamiento de la operación
