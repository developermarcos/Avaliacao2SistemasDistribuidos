#!/usr/bin/env python3
import socket
import os

from tkinter import filedialog


def Main():
    mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidorDestino = ('127.0.0.1', 10000)
    mySocket.connect(servidorDestino)

    # recebe mensagem com o nome do arquivo que vai receber
    nomeArquivo = mySocket.recv(1024)

    # solicita ao usuário onde deseja salvar o arquivo recebido
    fullpath = filedialog.askdirectory(
        initialdir=os.getcwd(), title='Salvar em:')

    # cria um novo arquivo binario, vazio, para receber o arquivo enviado
    file = open(fullpath+'/new_'+nomeArquivo.decode(), "wb")

    # Receba as partes do arquivo e monta o arquivo
    RecvData = mySocket.recv(1024)
    while RecvData:
        file.write(RecvData)
        RecvData = mySocket.recv(1024)

    # Feche o arquivo aberto no lado do servidor uma vez que a cópia seja concluída
    file.close()
    print("\n O arquivo foi copiado com sucesso \n")

    mySocket.close()


if __name__ == '__main__':
    Main()
