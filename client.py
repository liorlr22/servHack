import socket
import commands
import cv2
import os
import pickle
import keyboard


def cam():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 10000000)
    serverip = "127.0.0.1"
    serverport = 8080
    cap = cv2.VideoCapture(0)
    while True:
        ret, photo = cap.read()

        cv2.imshow('streaming', photo)

        ret, buffer = cv2.imencode(".jpg", photo, [int(cv2.IMWRITE_JPEG_QUALITY), 30])
        x_as_bytes = pickle.dumps(buffer)

        s.sendto(x_as_bytes, (serverip, serverport))

        if cv2.waitKey(10) == 13:
            break

    cv2.destroyAllWindows()
    cap.release()


def main():
    global my_socket
    my_socket.connect(("127.0.0.1", commands.PORT))
    cap = cv2.VideoCapture(0)

    while True:
        user_input = input("Enter command\n")
        valid_cmd = commands.check_cmd(user_input)

        if valid_cmd:
            my_socket.send(commands.create_msg(user_input).encode())
            if user_input == "SCRE":
                with open('Screen.jpg', "wb") as fw:
                    while True:
                        data = my_socket.recv(1024)
                        if data == b'Done' or data == b'A Problem Occurred':
                            break
                        fw.write(data)
                    fw.close()
                    if (data != b'A Problem Occurred'):
                        print("Image Saved")
                    else:
                        print(data.decode())
            if user_input == "CAM":
                cam()
            elif user_input == "EXIT":
                break
            else:
                print(my_socket.recv(1024).decode())

        else:
            print("Not a valid command")

    print("Closing")
    my_socket.close()


if __name__ == "__main__":
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    main()
