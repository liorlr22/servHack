import os
import socket
import commands
import datetime
import random
import shutil
from os import remove
from os import listdir
from os.path import isfile, join
from PIL import ImageGrab
import pickle
import cv2


def cam():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ip = "0.0.0.0"
    port = 8080
    s.bind((ip, port))
    while True:
        x = s.recvfrom(1000000)
        clientip = x[1][0]
        data = x[0]
        data = pickle.loads(data)
        data = cv2.imdecode(data, cv2.IMREAD_COLOR)
        cv2.imshow('server', data)
        if cv2.waitKey(10) == 27:
            break
    cv2.destroyAllWindows()
    s.close()
    return


def create_server_rsp(data, ms, cs):
    if data == "RAND":
        num = random.randint(1, 10)
        return num
    elif data == "NAME":
        return "ProServer"
    elif data == "TIME":
        return datetime.datetime.now().strftime("%c")
    elif data == "TREE":
        return os.system("start /wait cmd /c tree C://")
    elif data == "EXIT":
        return "EXIT"
    elif data[0:3] == "DIR":
        try:
            dir = data[4:]
            return [f for f in listdir(dir) if isfile(join(dir, f))]
        except:
            return "Folder Not Found"
    elif data[0:3] == "DEL":
        try:
            path = data[4:]
            remove(path)
            return "File Deleted"
        except:
            return "File Not Found"
    elif data[0:4] == "COPY":
        try:
            chunks = data.split(' ')
            from_dir = chunks[1]
            to_dir = chunks[2]
            shutil.copy(from_dir, to_dir)
            return "File Copied"
        except:
            return "File Not Found"
    elif data[0:3] == "EXE":
        try:
            file = data[4:]
            os.startfile(file)
            return "File Opened"
        except:
            return "File Not Found"


def main():
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(("0.0.0.0", commands.PORT))
        server_socket.listen()
        print("Server is up and running")
        (client_socket, client_address) = server_socket.accept()
        print("Client connected")

        while True:
            valid_msg, cmd = commands.get_msg(client_socket)
            if valid_msg:
                print("server1", cmd)
                if commands.check_cmd(cmd):
                    print("server2 in")
                    if cmd == "EXIT":
                        create_server_rsp(cmd, server_socket, client_socket)
                        break
                    elif cmd == "CAM":
                        cam()

                    elif cmd == "SCRE":
                        try:
                            image = ImageGrab.grab()
                            image.save('screenshot.jpg', 'JPEG')
                            with open('screenshot.jpg', 'rb') as fs:
                                while True:
                                    data = fs.read(1024)
                                    print('Sending data')
                                    client_socket.send(data)
                                    print('Sent data')
                                    if not data:
                                        print('Breaking from sending data')
                                        print("sent")
                                        break
                                fs.close()
                            client_socket.send(b'Done')
                        except:
                            client_socket.send(b'A Problem Occurred')
                    else:
                        print("server3 in")
                        client_socket.send(str(create_server_rsp(cmd, server_socket, client_socket)).encode())
                else:
                    response = "Wrong command"
                    client_socket.send(response.encode())
            else:
                response = "Wrong protocol"
                client_socket.send(response.encode())
                client_socket.recv(1024)

        print("Closing")
        client_socket.close()
        server_socket.close()
    except Exception as e:
        print("Connect Disconnected, Closing Socket", e)
        server_socket.close()


if __name__ == "__main__":
    main()
