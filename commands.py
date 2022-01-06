PORT = 8820


def check_cmd(data):
    """Check if the command is defined in the protocol (e.g RAND, NAME, TIME, EXIT)"""
    if data == "TREE" or data == "CAM" or data == "RAND" or data == "NAME" or data == "TIME" or data == "EXIT" or data[0:3] == "DIR" \
            or data[0:3] == "DEL" or data[0:4] == "COPY" or data[0:3] == "EXE" or data[0:4] == "SCRE":
        return True
    else:
        return False


def create_msg(data):
    """Create a valid protocol message, with length field"""
    if data == "RAND":
        return "04RAND"
    elif data == "NAME":
        return ("04NAME")
    elif data == "TIME":
        return ("04TIME")
    elif data[0:3] == "DIR":
        new_data = "03" + data
        return (new_data)
    elif data[0:3] == "DEL":
        new_data = "03" + data
        return (new_data)
    elif data[0:3] == "EXE":
        new_data = "03" + data
        return (new_data)
    elif data[0:4] == "COPY":
        new_data = "04" + data
        return (new_data)
    elif data[0:4] == "SCRE":
        return ("04SCRE")
    elif data == "TREE":
        return ("03TREE")
    elif data == "EXIT":
        return ("04EXIT")
    elif data == "CAM":
        return ("04CAM")


def get_msg(my_socket):
    """Extract message from protocol, without the length field
       If length field does not include a number, returns False, "Error" """
    data = my_socket.recv(1024).decode()
    if (data[1] == "4") or (data[1] == "3"):
        return True, data[2:]
    else:
        return False, "Error"
