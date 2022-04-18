import socket
import threading

class Servidor:
    arrayConexoes = []
    def __init__(self, host, port, serverName):
        self.host = host
        self.port = port
        self.serverName = serverName
    
    def createSocket(self):
        # cria o socket TCP do servidor (Internet,Transporte)
        self.socketTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Configura o IP e a porta que o servidor vai ficar executando
        self.socketTCP.bind((self.host,self.port))
        print('Servidor Python TCP: {}:{}'.format(self.host,self.port))
        
        # habilita o servidor para aceitar conexões
        # o parâmetro indica a quantidade máxima de solicitações de conexão que podem ser enfileiradas, antes de serem recusadas. Ex: 5 (congestionamento)
        self.socketTCP.listen(1)

    def createThreading(self, conn):
        t = threading.Thread(target=self.thread, args=(conn,))
        t.start()
    
    def thread(self, conn):
        while True:
            print('Aguardando mensagens...')
            print(conn)
            
            data = conn.recv(4096)
            if not data:
                break
            print('Recebido {} bytes de {}'.format(len(data), conn.getpeername()))
            self.broadcast(conn, data)

        conn.close()
        return
    
    def broadcast(self, conn, data):

        for conexao in self.arrayConexoes:
            if conn.getpeername() != conexao.getpeername():
                conexao.send(data.upper())