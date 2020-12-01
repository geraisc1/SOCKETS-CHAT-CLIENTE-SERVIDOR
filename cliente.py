#Importamos la libreias necesarias
import socket
# threading esta libreia en la encargada de que exista una conexion entre varios clientes al mismo tiempo.
import threading
import sys
import pickle

#Se crea una clase llamada cliente 
class Cliente():

	#Creamos una funnion la cual contiene la conexion al puerto 9000
	def __init__(self, host="localhost", port=9000):

		#Establece el tipo de familia o socket que se ocupara puede ser TCP/IP	
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		# Estalbece una conexion a traves de la variable connect
		self.sock.connect((str(host), int(port)))

		#Recibe la conexion a traves del uso de la libreria	
		msg_recv = threading.Thread(target=self.msg_recv)

		#Si la conexion es correcta inicia la trasmicion de datos.
		msg_recv.daemon = True
		msg_recv.start()

		# Establece un bucle para mostrar la opcion de entrada de datos cada vez que el cliente desee enviar un mensaje.
		while True:
			msg = raw_input('Mensaje desde Cliente a Servidor >> ')
			if msg != 'salir':
				#Envia el mensaje
				self.send_msg(msg)
				
			else:
				#Imprime los mensajes como notificacion al servidor cuando un cliente se conecta.
				print"CLIENTE DESCONECTADO"
				
				#Manda una notificacion al servidor cuando un cliente se desconecta.
				texto = "CLIENTE DESCONECTADO"
				
				self.sock.send(texto.encode())
				#Se cierra la conexion
				self.sock.close()
				sys.exit()
	#Define una funcion para recibir los datos del cliente y servidor.
	def msg_recv(self):
		while True:
			try:
				data = self.sock.recv(1024)
				if data:
					print(pickle.loads(data))
			except:
				pass
	#Define una funcion para enviar los mensajes al servidor.
	def send_msg(self, msg):
		self.sock.send(pickle.dumps(msg))


c = Cliente()
		