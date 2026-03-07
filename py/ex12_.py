import tkinter as tk
from tkinter import messagebox
import pandas as pd
import matplotlib.pyplot as plt

# Sample Data
accident_data = {
    "Location": ["Delhi", "Gurgaon", "Manesar", "Bawal", "Shahjahanpur"],
    "Accidents": [10, 14, 5, 3, 8]
}

# Function to display accident data
def display_data():
    df = pd.DataFrame(accident_data)
    plt.bar(df['Location'], df['Accidents'], color='blue')
    plt.xlabel('Locations')
    plt.ylabel('Number of Accidents')
    plt.title('Live Road Accident Analysis of NH-8 Highway')
    plt.show()

# Exit application function
def exit_app():
    if messagebox.askokcancel("Quit", "Do you really want to quit?"):
        root.destroy()

# Create main window
root = tk.Tk()
root.title("Live Road Accident Analysis of NH-8 Highway")
root.geometry("500x300")
root.resizable(False, False)

# Header label
label = tk.Label(root, text="Live Road Accident Analysis", font=("Times New Roman", 14, 'bold'))
label.pack(pady=20)

# Button to display data
display_button = tk.Button(root, text="Display Accident Data", command=display_data)
display_button.pack(pady=10)

# Exit button
exit_button = tk.Button(root, text="Exit", command=exit_app)
exit_button.pack(pady=10)

# Start the GUI
root.mainloop()
