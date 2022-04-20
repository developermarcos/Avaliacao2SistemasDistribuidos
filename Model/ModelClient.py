import socket
import threading

class Cliente:
    def __init__(self, host, port, username):
        self.ConectParameter = (host, port)
        self.username = username
        # cria o socket TCP do cliente, abrindo uma porta alta
        self.Conection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        #realiza a conexao com o servidor
        self.Conection.connect(self.ConectParameter)

        self.Threading = threading.Thread(target=self.receiveMesages, args=())
        
        self.Threading.start()

    def receiveMesages(self, tela):
        while True:
            # fica em wait ate que uma mensagem chegue
            # recebe e mostra a mensagem devolvida pelo servidor
            data = self.Conection.recv(4096).decode()
            print()
            print(data)
            print("('s' sair ou digite a mensagem)> ")

    def sendMensage(self):
        # aguarda o usuário digitar uma mensagem
        message = input("('s' sair ou digite a mensagem)> ")

        if message == 's':
            return 'sair'

        # envia a mensagem do usuário para o servidorDestino
        mensagemServidor = ": ".join([self.username, message])

        self.Conection.send(mensagemServidor.encode('utf-8'))

        return 'continue'

    def closeConection(self):
        self.Conection.close()