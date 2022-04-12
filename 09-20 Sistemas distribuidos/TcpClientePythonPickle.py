import socket, pickle

class Mensagem(object):
    def __init__(self):
        self.usuario = ''
        self.msg     = ''

def Main():
    host = '127.0.0.1'
    port = 10000
    mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    mySocket.connect((host,port))
    
    # cria o objeto
    objEnviar = Mensagem()
    objEnviar.usuario = input("Nome: ")
    objEnviar.msg     = input("Mensagem: ")
    
    # serializa o objeto
    data_string = pickle.dumps(objEnviar)
    print(data_string)
    
    # envia o objeto serializado para o servidor
    mySocket.send(data_string)
    mySocket.close()

if __name__ == '__main__':
    Main()
