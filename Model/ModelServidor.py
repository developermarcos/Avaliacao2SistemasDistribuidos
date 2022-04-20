import socket, json
import threading

class Mensagem(object):
    def __init__(self):
        self.nome = ""
        self.mensagem = ""
        self.lista = list()
        self.tipo = ""

class Servidor:
    
    def __init__(self, host, port, serverName):
        self.host = host
        self.port = port
        self.serverName = serverName
        self.arrayConexoes = []

        self.mensagemRecebida = Mensagem()
        # cria o socket TCP do servidor (Internet,Transporte)
        self.socketTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Configura o IP e a porta que o servidor vai ficar executando
        self.socketTCP.bind((self.host,self.port))
        print('Servidor Python TCP: {}:{}'.format(self.host,self.port))
        
        # habilita o servidor para aceitar conexões
        # o parâmetro indica a quantidade máxima de solicitações de conexão que podem ser enfileiradas, antes de serem recusadas. Ex: 5 (congestionamento)
        self.socketTCP.listen(1)

    def createThreading(self, conn, ):
        t = threading.Thread(target=self.thread, args=(conn,))
        t.start()
    
    def thread(self, conn):
        while True:
            try:
                
                print('Aguardando mensagens...')
                print(conn)
                
                mensagem = conn.recv(4096)

                objectEnviar = Mensagem()

                self.mensagemRecebida = json.loads(mensagem)
                objectEnviar.mensagem = self.mensagemRecebida['mensagem']
                objectEnviar.nome = self.mensagemRecebida['nome']
                objectEnviar.tipo = self.mensagemRecebida['tipo']
                objectEnviar.lista = self.mensagemRecebida['lista']

                if objectEnviar.tipo == 'Mensagem':
                    print('É mensagem')

                if objectEnviar.tipo != '' and objectEnviar.tipo != 'sair':
                    print('Recebido {} bytes de {}'.format(objectEnviar.mensagem, conn.getpeername()))
                    self.broadcast(conn, objectEnviar)
                else:
                    print('Usuário {} bytes de {} desconectado'.format(len(objectEnviar.mensagem), conn.getpeername()))
                    break

            except:
                conn.close()
                break
        

    
    def broadcast(self, conn, data):
        data.lista = self.arrayConexoes
        mensagemSerealizada = json.dumps(data.__dict__,indent=0)
        for conexao in self.arrayConexoes:
            if conn.getpeername() != conexao.getpeername():
                conexao.send(bytes(mensagemSerealizada,encoding="utf-8"))
                