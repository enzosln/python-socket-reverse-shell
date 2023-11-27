import socket


def start_server():
    host = '0.0.0.0'
    port = 9999

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()

    print(f"[*] Serveur en écoute sur {host}:{port}")

    client, addr = server.accept()
    print(f'Connexion reçu de {addr}')
    while True:
        try:
            a = input('Entrez une commande :')
            if a != "" and a:
                client.send(a.encode('utf-8'))
            else:
                continue
            try:
                return_command = client.recv(100000).decode('utf-8')
            except:
                return_command = False
                pass
            if not return_command:
                continue
            else:
                print(return_command)
        except KeyboardInterrupt:
            client.close()
            server.close()
            print('EXITING')
            exit()
        except BrokenPipeError:
            server.close()
            client.close()
            print('La connexion a été perdu, relancement du programme server...')
            start_server()
            exit()

if __name__ == "__main__":
    start_server()
