import socket
import tkinter as tk

def send_guess():
    guess = guess_entry.get()
    if guess.lower() == 'quit':
        root.destroy()
        return

    try:
        guess_int = int(guess)
        client_socket.sendall(str(guess_int).encode())
        result = client_socket.recv(1024).decode()
        result_label.config(text=result)
    except ValueError:
        result_label.config(text="Invalid input. Please enter a number between 1 and 100.")

def main():
    global client_socket, guess_entry, result_label, root

    # Create a socket and connect to the server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 8000))

    # Create the GUI
    root = tk.Tk()
    root.title("Guessing Game")
    root.geometry("400x200")

    # Create the widgets
    guess_label = tk.Label(root, text="Enter your guess (between 1 and 100):")
    guess_entry = tk.Entry(root)
    send_button = tk.Button(root, text="Send", command=send_guess)
    result_label = tk.Label(root, text="")
    quit_button = tk.Button(root, text="Quit", command=root.destroy)

    # Add the widgets to the window
    guess_label.pack()
    guess_entry.pack()
    send_button.pack()
    result_label.pack()
    quit_button.pack()

    # Start the GUI event loop
    root.mainloop()

    # Close the socket
    client_socket.close()

if __name__ == '__main__':
    main()
