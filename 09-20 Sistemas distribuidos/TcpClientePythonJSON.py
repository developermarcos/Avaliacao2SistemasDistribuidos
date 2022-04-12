import socket, json

class Mensagem(object):
    def __init__(self):
        self.usuario = ""
        self.msg     = ""

def Main():
    host = '127.0.0.1'
    port = 10000
    mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    mySocket.connect((host,port))
    
    # cria o objeto
    objEnviar = Mensagem()
    objEnviar.usuario = input("Nome: ")
    objEnviar.msg = input("Mensagem: ")
    
    # serializa o objeto
    
    data_string = json.dumps(objEnviar.__dict__, indent=0)
    print(data_string)

    # há a __dict__ em qualquer objeto python, que é um dicionário usado para armazenar atributos (gravação) de um objeto. Podemos usar isso para trabalhar com JSON e funciona bem.
    # __dict__ é um atributo de guardar atributos de instância nos objetos

    # envia o objeto serializado para o servidor
    mySocket.send( bytes(data_string,encoding="utf-8") )

    mySocket.close()

if __name__ == '__main__':
    Main()
