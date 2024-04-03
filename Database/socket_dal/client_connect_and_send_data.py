import socket
import json

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Connect to the server
SOCKET_HOST = "192.168.111.63"
SOCKET_PORT = 1111
client_socket.connect((SOCKET_HOST, SOCKET_PORT))

if __name__ == '__main__':

    """bắn data  qua socket VMS"""
    base64_encoded = "iVBORw0KGgoAAAANSUhEUgAAAAwAAAAVCAIAAAD9zpjjAAADFElEQVQoFQEJA/b8AV9eYNDMzvnw82heVjQZCP77Ab/V7MXOzd7o5fwBAQAFAQIFAgFfXmDRzc/68fRsXE4qEwgGAAjl+grGz8+5wsP6AQIABQIABAEBX15g0c3PAPf4bVg/KA8UAv0EAQoT2ubokpue9AUH/QIAAAQDAVtWVcrDyAwEBIN0XAz4/BYPE+3z/+Tt8LnDxcrb3/0DAPb7+gF8a17m3uoPCQhDQSwLAgQ2MSrY0uzo6+zM1NeesbkbIBbk7vEBlHxs+eD1Hi0krayq7+ntbmldFBEICQkY7PL3qcC87+7zzNncAaqQi9SzwDJGMvz7AO/s/qannGtnUwcJCQILDdnm7O/w9KiyugGhhofx0dghMxnFxsrj4vcmKSMJAf70+Ou3v8L6AQUlKijN198Bg25uNBAVDh4H7e3xsau99Pf0UkpSqrClKjMwKDAt2uHdoqixAScoH6x7g/D35vHo7dzV2x0dH0BAQJadn9nj4uDp5jxHN8O9ywFEPz6Da1ns4OEG/QLz7PIdHB4tLS2wuLjv+Pjq8vABDP7Ty9oBVVNa4tDAbFdOFg0SFQ0SAQMAJDMzppqc9Pr78vj4DBwSzsPTAVNVXvbi1lQ9Lw0ECAT9AhscFyEmJq+sqx8iJvH199zs6fj7BgFUVV7v5+BbPCv/9/klHiKIj5Q3NDEdIB0OERHw8PLi7/QPFx0BVFZe8/PzVTEc/fX1KSIl/v0Gnqek/v/8NDc18fHx/AYS3ujrAVRVYf79/UQjDQwFBAgACAMBA+fx7gIFAvP18vf399Hv9QcFDAFTVGQbGhslCvD+9+7h2OPy6e4RHBgNFRH+Av78/fzQ6fMHCg8BUFBin5+arZN9/fflEwoV6+Dw2OPf19/bODw4AwME0+3z/wIHATUyTK6xqLOTi/3+3hIOD9zS3QEGBgEEBvj8+/EFDePx9wEAAwFJRmJwcm/iwrjq7sknJCEJ/wvd39709Pr8Af8AGyjM1tsBAQEBjIygFBQa2L25FhHq7+7nDwgSBwcH8PT28/f5P1lmmKGmAgEBWrmEmWDL/CoAAAAASUVORK5CYII="
    data = {
        "address": "0x7d943119a760",
        "base64": base64_encoded,
        "name": "Vuong",
        "ai_module": 1,
    }

    # Convert the JSON data to a string
    json_string = json.dumps(data)
    client_socket.sendall(json_string.encode())