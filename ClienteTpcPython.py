import socket
import threading

def Main():
    mySocket = createConection('127.0.0.1', 10000)
    t = threading.Thread(target=receiveMesages, args=(mySocket,))
    t.start()
    # fica em loop enviando e recebendo mensagens com o servidor
    username = input("Usuário> ")
    while True:
        retorno = sendMensage(mySocket, username)
        if retorno == 'sair':
            break

    mySocket.close()

def createConection(host, port):
    # cria o socket TCP do cliente, abrindo uma porta alta
    mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # define o endereço e porta do servidor de destino
    servidorDestino = (host, port)
    
    #realiza a conexao com o servidor
    # cria e dispara a execução da thread para o servidor
    mySocket.connect(servidorDestino)
    return mySocket

def receiveMesages(conn):
    while True:
        # fica em wait ate que uma mensagem chegue
        # recebe e mostra a mensagem devolvida pelo servidor
        data = conn.recv(4096).decode()
        print(data)


def sendMensage(mySocket, username):
    # aguarda o usuário digitar uma mensagem
    message = input("('s' sair ou digite a mensagem)> ")

    if message == 's':
        return 'sair'

    # envia a mensagem do usuário para o servidorDestino
    mensagemServidor = ": ".join([username, message])
    mySocket.send(mensagemServidor.encode('utf-8'))
    return 'continue'



if __name__ == '__main__':
    Main()