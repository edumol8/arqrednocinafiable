import socket   # Importa el módulo socket para crear conexiones de red (TCP/IP)
import time     # Importa time para usar pausas (sleep)

HOST = '127.0.0.1'   # Dirección IP del servidor (localhost)
PORT = 65432         # Puerto donde el servidor está escuchando

# Función que envía una transacción al servidor
def enviar_transaccion(msg):
    # Crea un socket TCP y se asegura de cerrarlo al finalizar con "with"
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))   # Conecta el socket al servidor usando la IP y puerto definidos
        
        # Intentos de envío y re-envío
        for intento in range(1, 3):   # Bucle que permite 2 intentos (1 y 2)
            print(f"\n--- Intento {intento} ---")  # Muestra qué intento se está realizando
            
            s.sendall(msg.encode())   # Envía el mensaje convertido a bytes al servidor
            print(f"ENVIADO: {msg}")  # Imprime qué mensaje se envió
            
            s.settimeout(2)           # Configura un máximo de 2 segundos para esperar respuesta
            
            try:
                # Intenta recibir la confirmación del servidor
                respuesta = s.recv(1024).decode()   # Recibe hasta 1024 bytes y los convierte a string
                
                # Si el servidor envía "OK_CONFIRMADO", la transacción fue exitosa
                if "OK_CONFIRMADO" in respuesta:
                    print("👍 Recibida la confirmación. Transacción exitosa.")
                    return  # Fin de la función: ya se recibió el ACK correcto

            except socket.timeout:
                # Si pasan los 2 segundos sin recibir nada, ocurre un timeout
                # Esto simula la "pérdida del paquete" y obliga a reintentar
                print("--- ⚠️ Timeout. Asumiendo paquete perdido. Re-enviando... ---")
        
        # Si se terminan los 2 intentos sin confirmación, se asume fallo total
        print("\n❌ Falló el envío después de 2 intentos.")

# Simulamos una compra del cliente enviando RESTAR_100 al servidor
enviar_transaccion("CLIENTE_A_RESTAR_100")
