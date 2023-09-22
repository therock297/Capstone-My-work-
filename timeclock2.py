import tkinter as tk
from tkinter import ttk
from datetime import datetime
import time

# Function to update the time label
def update_time():
  current_time = datetime.now().strftime("%H:%M:%S")
  time_label.config(text=current_time)
  root.after(1000, update_time)

# Function to handle the workout time selection
def start_workout():
  selected_workout = workout_var.get()
  workout_time = workout_times.get(selected_workout, 0)

  if workout_time > 0:
    time_remaining_label.config(text=f"Time Remaining: {workout_time} seconds")
    countdown(workout_time)

# Function to start the countdown timer
def countdown(seconds):
  for i in range(seconds, -1, -1):
    time_remaining_label.config(text=f"Time Remaining: {i} seconds")
    root.update()
    time.sleep(1)

# Create the main window
root = tk.Tk()
root.title("Workout Time Clock")

# Styling
root.geometry("400x300")  # Set window size
root.configure(bg="lightgreen")  # Set background color

# Create a label for the current time
time_label = tk.Label(root, text="", font=("Roboto Bold", 48), bg="lightgreen")
time_label.pack(pady=20)

# # Create an image for the background
# background_image = tk.PhotoImage(file="workout_background.png")
# background_label = tk.Label(root, image=background_image)
# background_label.pack()

# Create a dropdown menu for workout time selection
workout_times = {
  "5 minutes": 300,
  "10 minutes": 600,
  "15 minutes": 900,
  "20 minutes": 1200,
}
workout_var = tk.StringVar(root)
workout_var.set("Select Workout Time")
workout_menu = ttk.Combobox(root, textvariable=workout_var, values=list(workout_times.keys()))
workout_menu.pack(pady=10)

# Create a button to start the workout timer
start_button = tk.Button(root, text="Start Workout", command=start_workout, bg="green", fg="white", font=("Roboto Bold", 14))
start_button.pack()

# Create a label to display the remaining workout time
time_remaining_label = tk.Label(root, text="", font=("Roboto Bold", 18), bg="lightgreen")
time_remaining_label.pack(pady=20)

# Add a progress bar for the workout time
progress_bar = ttk.Progressbar(root, orient="horizontal", length=200)
progress_bar.pack(pady=10)

# Start updating the current time
update_time()

root.mainloop()