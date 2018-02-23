#!/usr/bin/python3

import socket

def suma(x, y):
	return x + y
	
def resta(x, y):
	return x - y

def multiplica(x, y):
	return x * y

def divide(x, y):
	return x / y
	
operations = {"sumar": suma, "restar": resta,
				"multiplicar": multiplica, "dividir": divide}
				
codes = {'200': 'OK', '404': 'Not Found'}

def send_response(Code, Body):
	response = ("HTTP/1.1" + " " + Code + " " + codes[Code] + "\r\n\r\n" +
				"<html><body>" + Body + "</body></html>")
	return response

# ESTABLECIMIENTO DE LA COMUNICACIÓN
mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
mySocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
mySocket.bind(('localhost', 1234))
mySocket.listen(5)

try:
	while True:
		# SERVIDOR SE P0NE A ESCUCHAR
		print('Waiting for connections...')
		(recvSocket, address) = mySocket.accept()
        
		# PARTE DE ANALIZAR EL RECURSO
		request = str(recvSocket.recv(2048), 'utf-8')
		resource = request.split()[1]
		nothing, operator1, operation, operator2 = resource.split("/")
        
        # PARTE DE PROCESAR EL RESULTADO
		if operation in operations:
			
			try:
				result = operations[operation](float(operator1), float(operator2))
				message = str(operator1) + " " + operation + " " + str(operator2) + " = " + str(result)
			except ZeroDivisionError:
				print("ZeroDivisionError")
				message = "Undefined"
				
			coment = send_response('200', message)
		else:
			# Asumo como rescurso no válido una operación no contemplada
			# en el diccionario.
			coment = send_response('404', "Not Found!")
							
		# ENVIAMOS LOS RESULTADOS
		recvSocket.send(bytes(coment, 'utf-8'))
		print("Sending...")
		recvSocket.close()
			   
except KeyboardInterrupt:
    print("Closing binded socket")
mySocket.close()
