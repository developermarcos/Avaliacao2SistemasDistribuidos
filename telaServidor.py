import ModelServidor
host = '0.0.0.0'
port= 10000

servidor = ModelServidor.Servidor(host, port, 'Servidor Sistemas Distribuidos')

servidor.createSocket()

while True:
    conn, addr = servidor.socketTCP.accept()
    print("Conexão realizada por: " + str(addr))
    servidor.arrayConexoes.append(conn)
    servidor.createThreading(conn)