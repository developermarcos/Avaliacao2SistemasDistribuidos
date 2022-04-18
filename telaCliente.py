import socket
import ModelClient
import TelaModel

host = '127.0.0.1'
port = 10000

username = input("Usuário> ")
cliente = ModelClient.Cliente(host, port, username)
cliente.createConection()
cliente.createThreading()

while True:
    retorno = cliente.sendMensage()
    if retorno == 'sair':
        break
    

cliente.closeConection()
