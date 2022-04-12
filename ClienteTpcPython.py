import socket
import threading

def rodaThread(conn):
    while True:
        # fica em wait ate que uma mensagem chegue
        # recebe e mostra a mensagem devolvida pelo servidor
        data = conn.recv(4096)
        
        print('Recebido do servidor {}: {}'.format( conn.getpeername(),data.decode()))
        

def Main():
    # cria o socket TCP do cliente, abrindo uma porta alta
    mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #print('Cliente Python UDP: {}'.format( mySocket.getsockname ) )
    
    # define o endereço e porta do servidor de destino
    servidorDestino = ('127.0.0.1', 10000)
    
    #realiza a conexao com o servidor
    # cria e dispara a execução da thread para o servidor
    mySocket.connect(servidorDestino)
    t = threading.Thread(target=rodaThread, args=(mySocket,))
    t.start()
    # fica em loop enviando e recebendo mensagens com o servidor
    nome = "Mensagem de "
    nome += input(" -> Informe seu nome ")
    while True:
        # aguarda o usuário digitar uma mensagem
        
        message = nome+": "+input(" -> (q sair ou digite a mensagem) ")

        if message == 'q':
            break

        # envia a mensagem do usuário para o servidorDestino
        mySocket.send(message.encode())

    mySocket.close()

if __name__ == '__main__':
    Main()