import socket
import threading
import tkinter as tk

def handle_client(client_socket, secret_number):
    # Receive and handle guesses from this client
    while True:
        try:
            data = client_socket.recv(1024).decode()
            if not data:
                break

            guess = int(data)

            if guess == secret_number:
                result = "Congratulations! You guessed the number!"
            elif guess < secret_number:
                result = "Your guess is too low. Try again."
            else:
                result = "Your guess is too high. Try again."

            client_socket.sendall(result.encode())
        except ValueError:
            pass

    client_socket.close()

def start_server():
    global secret_number, server_socket, status_label

    # Get the secret number from the server user
    secret_number = None
    while secret_number is None:
        try:
            secret_number = int(secret_number_entry.get())
            if secret_number < 1 or secret_number > 100:
                raise ValueError
        except ValueError:
            status_label.config(text="Invalid input. Please enter a number between 1 and 100.")
            return

    # Create a server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to a port
    server_socket.bind(('localhost', 8000))

    # Listen forincoming connections
    server_socket.listen()

    # Update the GUI to show that the server is running
    status_label.config(text="Server is running.")

    # Handle incoming connections
    while True:
        # Accept a new client connection
        client_socket, client_address = server_socket.accept()

        # Handle the client's guesses in a new thread
        client_thread = threading.Thread(
            target=handle_client, args=(client_socket, secret_number))
        client_thread.start()


if __name__ == '__main__':
    # Create the GUI
    root = tk.Tk()
    root.title("Guessing Game Server")
    root.geometry("400x200")

    # Create the widgets
    secret_number_label = tk.Label(root, text="Enter the secret number (between 1 and 100):")
    secret_number_entry = tk.Entry(root)
    start_button = tk.Button(root, text="Start Server", command=start_server)
    result_label = tk.Label(root, text="")
    status_label = tk.Label(root, text="Server is not running.")

    # Add the widgets to the window
    secret_number_label.pack()
    secret_number_entry.pack()
    start_button.pack()
    result_label.pack()
    status_label.pack()

    # Start the GUI event loop
    root.mainloop()

    # Close the server socket
    server_socket.close()