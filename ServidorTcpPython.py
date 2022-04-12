import socket
import threading

def rodaThread(conn, arrayConexoes):
    while True:
        print('Aguardando mensagens...')
        print(conn)
        
        data = conn.recv(4096)
        if not data:
            break
        print('Recebido {} bytes de {}'.format(len(data), conn.getpeername()))
        # devolve a mensagem para o cliente
        #conn.send(data.upper())
        enviarMensagens(arrayConexoes, conn, data)

    conn.close()
    return

def enviarMensagens(arrayConexoes, conn, data):

    for conexao in arrayConexoes:
        if conn.getpeername() != conexao.getpeername():
            conexao.send(data.upper())

def Main():
    
    host = "0.0.0.0"
    port = 10000
    # cria o socket TCP do servidor (Internet,Transporte)
    socketTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Configura o IP e a porta que o servidor vai ficar executando
    socketTCP.bind((host,port))
    print('Servidor Python TCP: {}:{}'.format(host,port))
    
    # habilita o servidor para aceitar conexões
    # o parâmetro indica a quantidade máxima de solicitações de conexão que podem ser enfileiradas, antes de serem recusadas. Ex: 5 (congestionamento)
    socketTCP.listen(1)
    # fica em loop aguardando novas conexões de clientes
    arrayConexoes = []
    while True:
        # fica bloqueado aguardando a conexão de um cliente
        conn, addr = socketTCP.accept()
        print("Conexão realizada por: " + str(addr))

        arrayConexoes.append(conn)
        
        # cria e dispara a execução da thread do cliente
        t = threading.Thread(target=rodaThread, args=(conn, arrayConexoes))
        t.start()

    socket.close()

if __name__ == '__main__':
    Main()