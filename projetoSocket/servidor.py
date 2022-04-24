import socket, json
import threading
from compartilhado import serializador, mensagem, conexao
from datetime import datetime

class Servidor:
    def __init__(self):
        self.host = '0.0.0.0'
        self.port = 10000
        self.serializador = serializador.Serial()
        self.arrayConexoes = list()
        
    def createSocket(self):
        # cria o socket TCP do servidor (Internet,Transporte)
        self.socketTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Configura o IP e a porta que o servidor vai ficar executando
        self.socketTCP.bind((self.host,self.port))
        print('Servidor Python TCP: {}:{}'.format(self.host,self.port))

        # habilita o servidor para aceitar conexões
        # o parâmetro indica a quantidade máxima de solicitações de conexão que podem ser enfileiradas, antes de serem recusadas. Ex: 5 (congestionamento)
        self.socketTCP.listen(1)

    def createThreading(self, addr, conn, objetoMensagem):
        t = threading.Thread(target=self.thread, args=(addr, conn,objetoMensagem))
        t.start()

    def thread(self, addr, conn, objetoMensagem):

        self.__registrarNovaConexao(addr, conn, objetoMensagem)

        while True:
            print('Aguardando mensagens...')
            print(conn)

            # Recebe mensagem do cliente
            data = conn.recv(4096)
            if not data:
                break
            
            # Deserealiza mensagem do cliente
            mensagemRecebidaDeserializada = self.serializador.deserializarMensagem(data)

            # Armazena tipo da mensagem
            tipoMensagem = mensagemRecebidaDeserializada.get("tipo")

            if tipoMensagem == 'mensagem' or tipoMensagem == 'mensagemDestinatario':
                # Monta objeto mensagem
                mensagemEnviarCliente = mensagem.Mensagem(
                mensagemRecebidaDeserializada.get("nome"),
                mensagemRecebidaDeserializada.get("mensagem"),
                'mensagem',
                '',
                mensagemRecebidaDeserializada.get("destinatario")
                )

                # Variável para estruturar log
                nomeDestinatario = 'Todos clientes'
                ipDestinatario = ''

                # Verifica tipo para montar o log
                if tipoMensagem == 'mensagemDestinatario':
                    nomeDestinatario = mensagemRecebidaDeserializada.get("destinatario")
                    ipDestinatario = '127.0.0.1'

                #Registra log de mensagem
                self.__registrarLog(
                    datetime.today(), 
                    self.host,
                    mensagemRecebidaDeserializada.get("nome"), 
                    addr, 
                    ipDestinatario, 
                    nomeDestinatario, 
                    mensagemRecebidaDeserializada.get("mensagem"))

                # Serealiza mensagem
                mensagemSerealizada = self.serializador.serealizarObjeto(mensagemEnviarCliente)

                # Envia mensagem para método broadcast
                self.__broadcast(conn, mensagemSerealizada, tipoMensagem, mensagemRecebidaDeserializada.get("destinatario"), conn)
                
            elif tipoMensagem == 'desconectar':
                self.__retiraClienteListaConectados(mensagemRecebidaDeserializada)

                # Cria lista de clientes conectados
                nomeClientesConectados = self.__criaListaConectados('desconectar')
                
                 # Variável para estruturar log
                nomeDestinatario = 'Todos clientes'
                ipDestinatario = ''

                #Registra log de mensagem
                self.__registrarLog(
                    datetime.today(), 
                    self.host,
                    mensagemRecebidaDeserializada.get("nome"), 
                    addr, 
                    ipDestinatario, 
                    nomeDestinatario, 
                    'logout')

                #Dicionario de conectados
                conectados = {
                    'tipo':'conectar',
                    'conectados':nomeClientesConectados
                }

                # Conectados serializado
                conectadosSerializado = self.serializador.serealizarMensagem(conectados)

                # Enviar lista de conectados para os clientes      
                self.__broadcast(conn, conectadosSerializado, 'desconectar', '', '')

                break

            elif tipoMensagem == 'arquivo':
                print('Arquivo')         
                
        conn.close()
        return

    #métodos privados
    #06/04/2022; 13:03; 192.168.10.50; luciano; 172.16.10.87-200.20.32.12-190.200.232.9; zé-maria-joão; msg:olá, tudo bem?
    def __registrarLog(self, dataHora, ipServidor, nomeRemetente, connRemetente, ipDestinatario, nomeDestinatario, mensagem):
        # IP e Porta do remetente
        ipRemetente, portRemetente = connRemetente
        enderecoRemetente = ipRemetente+' '+str(portRemetente)
        # Data da conexão formatada
        dataFormat = dataHora.strftime('%d/%m/%Y; %H:%M')
        # Monta o log
        separador = '; '
        log = separador.join([dataFormat, ipServidor, nomeRemetente, enderecoRemetente, ipDestinatario, nomeDestinatario, mensagem])
        
        # Le a estrutura do log
        file = open('compartilhado/log.txt', 'r')
        lines = file.readlines()
        file.close()
        # Adiciona novo log na variável
        lines.insert(1, log + '\n')
        # Altera arquivo de log
        file = open('compartilhado/log.txt', 'w')
        file.writelines(lines)
        file.close()

    def __registrarNovaConexao(self, addr, conn, objetoMensagem):
        
        # Deserealiza mensagem
        mensagemRecebidaDeserializada = self.serializador.deserializarMensagem(objetoMensagem)
        # instancia novo array conexões
        novaConexao = conexao.Conexao(datetime.today(), conn, mensagemRecebidaDeserializada.get("nome"), addr)
        # Adiciona novo array de conexoes
        self.arrayConexoes.append(novaConexao)
        #06/04/2022; 12:54; 192.168.10.50; luciano; 200.10.10.10; servidor; login
        self.__registrarLog(novaConexao.dataHora, self.host, novaConexao.nome, addr, '', 'Servidor', 'login')
        # Cria lista de conectados
        nomeClientesConectados = self.__criaListaConectados('conectar')

        #Dicionario de conectados
        conectados = {
            'tipo':'conectar',
            'conectados':nomeClientesConectados
        }
        # Conectados serializado
        conectadosSerializado = self.serializador.serealizarMensagem(conectados)

        # Enviar lista de conectados aos clientes
        self.__broadcast(conn, conectadosSerializado, 'conectar', '', '')

    def __broadcast(self, conn, data, tipo, destinatario, conexaoRemetente):
        #Laço de repetição apra enviar mensagens aos clientes conectados
        if tipo == 'mensagemDestinatario':
            for conexao in self.arrayConexoes:
                if conexao.nome == destinatario:
                    conexaoPosicao = conexao.conexao
                    conexaoPosicao.send(bytes(data,encoding="utf-8"))
        elif tipo == 'desconectar' or tipo == 'conectar': #Tratar desconexão
            print('Conectar ou desconectar')
            for conexao in self.arrayConexoes:
                conexaoPosicao = conexao.conexao
                conexaoPosicao.send(bytes(data,encoding="utf-8"))
        else:
            for conexao in self.arrayConexoes:
                conexaoPosicao = conexao.conexao
                if conn.getpeername() != conexaoPosicao.getpeername():
                    conexaoPosicao.send(bytes(data,encoding="utf-8"))

    def __criaListaConectados(self, tipo):
        # Cria array com nome dos conectados
        nomeClientesConectados = []
        for item in self.arrayConexoes:
            cliente = {'nome': item.nome, 'tipo':tipo}
            nomeClientesConectados.append(cliente)
                
        nomeClientesConectadosSerealizado = json.dumps(nomeClientesConectados, indent=0)
                    
        return nomeClientesConectadosSerealizado

    def __retiraClienteListaConectados(self, mensagemRecebidaDeserializada):
        # Retira da conexao
        for item in self.arrayConexoes:
            if item.nome == mensagemRecebidaDeserializada.get("nome"):
                self.arrayConexoes.remove(item)

    #end métodos privados


servidor = Servidor()

servidor.createSocket()

while True:
    conn, addr = servidor.socketTCP.accept()
    
    print("Conexão realizada por: " + str(addr))

    objetoMensagem = conn.recv(4096)
    
    servidor.createThreading(addr, conn, objetoMensagem)