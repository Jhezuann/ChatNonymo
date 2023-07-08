#Importaciones
import tkinter as tk
import socket
import threading

#Configuración del servidor
#Direccion Ip del server y puerto que se utilizara para la conexion
HOST = '127.0.0.1'
PORT = 5000

#Crear un socket y enlazarlo al servidor
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)  # Permitir una conexión simultánea

#Lista de clientes conectados al servidor
clients = []

#Lista de mensajes enviados y recibidos
messages = []

# Función para manejar las conexiones entrantes
def handle_client(client_socket, client_address):
    # Agregar el cliente a la lista de clientes
    clients.append(client_socket)
    
    # Recibir y reenviar los mensajes del cliente
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        for client in clients:
            if client != client_socket:
                client.sendall(data)
        messages.append(data.decode('utf-8'))
    
    # Eliminar el cliente de la lista de clientes
    clients.remove(client_socket)
    client_socket.close()

# Función para iniciar el servidor
def start_server():
    while True:
        # Esperar una conexión entrante
        client_socket, client_address = server_socket.accept()
        print(f'Nueva conexión de {client_address}')
        
        # Iniciar un hilo para manejar la conexión entrante
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()

# Función para enviar un mensaje a todos los clientes conectados
def send_message(message):
    message = message.encode('utf-8')
    for client in clients:
        client.sendall(message)
    messages.append(message.decode('utf-8'))
    messages_listbox.insert(tk.END, message.decode('utf-8'))
    # Desplazarse automáticamente hasta la parte inferior de la lista
    messages_listbox.see(tk.END)  

# Función para enviar un mensaje desde la interfaz de usuario
def send_message_from_ui():
    message = input_entry.get()
    send_message(message)
    input_entry.delete(0, tk.END)

# Crear la ventana de la aplicación
root = tk.Tk()
root.title('ChatNonymo')

# Crear la lista de mensajes y la entrada de texto y el botón de enviar
messages_listbox = tk.Listbox(root, width=50)
messages_listbox.pack(side=tk.TOP, padx=5, pady=5)

scrollbar = tk.Scrollbar(root)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

messages_listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=messages_listbox.yview)

input_frame = tk.Frame(root)
input_frame.pack(side=tk.TOP, padx=5, pady=5)

input_entry = tk.Entry(input_frame, width=50)
input_entry.pack(side=tk.LEFT)

send_button = tk.Button(input_frame, text='Enviar', command=send_message_from_ui)
send_button.pack(side=tk.LEFT, padx=5)

# Enlazar la tecla "ENTER" con la función paraenviar el mensaje
input_entry.bind('ENTER', send_message_from_ui)

# Iniciar el servidor en un hilo separado
server_thread = threading.Thread(target=start_server)
server_thread.start()

# Actualizar la lista de mensajes cada 100 milisegundos
def update_messages():
    global messages
    if len(messages) > messages_listbox.size():
        for message in messages[messages_listbox.size():]:
            messages_listbox.insert(tk.END, message)
            messages_listbox.see(tk.END)
    root.after(100, update_messages)

update_messages()

root.mainloop()