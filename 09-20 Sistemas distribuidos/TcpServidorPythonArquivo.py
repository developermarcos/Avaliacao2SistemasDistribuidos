#!/usr/bin/env python3
import socket
import os
from tkinter import filedialog, Tk


def Main():
    host = "0.0.0.0"
    port = 10000
    socketTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socketTCP.bind((host, port))
    print('Servidor Python TCP: {}:{}'.format(host, port))
    socketTCP.listen(5)

    # ao receber a conexao de um novo cliente, escolhe e envia um arquivo para ele
    while True:
        conn, addr = socketTCP.accept()
        print("Conexão realizada por: {}".format(str(addr)))

        # abre tela para escolha de um arquivo
        root = Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename(
            initialdir="/", title="Escolha um arquivo", filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))
        print(file_path)

        # envia mensagem com o nome do arquivo que vai ser enviado
        conn.send(os.path.basename(file_path).encode())

        
        #abre o arquivo escolhido, e vai enviando para o cliente por partes
        with open( file_path , 'rb') as f:
            conn.sendfile(f, 0)


        '''
        file = open(file_path, "rb")
        SendData = file.read(1024)
        while SendData:
            # envie o conteúdo do arquivo
            conn.send(SendData)
            SendData = file.read(1024)
        '''


        conn.close()

        print('Arquivo enviado.')


if __name__ == '__main__':
    Main()
