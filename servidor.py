#Importamos las librerias correspondientes
import socket
import threading
import sys
import pickle
#Crea una clase para el servidor
class Servidor():
	#Crea una funcion que contine la direccion y el puerto
	def __init__(self, host="localhost", port=9000):
		# Se crea una arreglo para almacenar a los clientes
		self.clientes = []
		#Establece el tipo de familia o socket que se ocupara puede ser TCP/IP
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.bind((str(host), int(port)))
		print ("En espara de conexiones en el puerto ", port)
		self.sock.listen(10)
		self.sock.setblocking(False)
		# Acepta la conexion entrante por parte del cliente.
		aceptar = threading.Thread(target=self.aceptarCon)
		procesar = threading.Thread(target=self.procesarCon)
		#Inicia la entrada de mensajes
		aceptar.daemon = True
		aceptar.start()

		procesar.daemon = True
		procesar.start()
		#Establece un bucle de control para cuando el servidor se desconecte.
		while True:
			msg = raw_input('->')
			if msg == 'salir':
				self.sock.close()
				print"SERVIDOR DESCONECTADO"
				sys.exit()
			else:
				pass

	# Se establecen funciones para el procesos de transmicion de informacion entre cliente-servidor.
	def msg_to_all(self, msg, cliente):
		for c in self.clientes:
			try:
				if c != cliente:
					c.send(msg)
			except:
				self.clientes.remove(c)

	def aceptarCon(self):
		
		while True:
			try:
				conn, addr = self.sock.accept()
				
				#Notificacion cada vez que un nuevo cliente se conecta.
				print"CLIENTE CONECTADO"
				conn.setblocking(False)
				self.clientes.append(conn)
			except:
				pass
	#Procesa la cantidad de conexiones				
	def procesarCon(self):
		
		while True:
			if len(self.clientes) > 0:
				for c in self.clientes:
					try:
						#Recive los datos del cliente
						data = c.recv(1024)
						
						if data:
							#Imprime los datos en pantalla que envio el cliente al servidor.
							print(data)
							self.msg_to_all(data,c)
					except:
						pass
	

s = Servidor()