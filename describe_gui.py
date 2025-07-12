import subprocess
import sys
import tkinter as tk
from PIL import Image, ImageTk
import os

script_path = os.path.dirname(__file__)

command = ['python3', script_path+'/describe.py']
args = sys.argv.copy()
args.pop(0) # remove argv[0] which is the script's name

window = tk.Tk()
working_label = tk.Label(window, text="Working...")

def call_show_result():
	full_command = command + args
	result = subprocess.run(full_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

	working_label.destroy()
	# Create a label for the string
	stdout_label = tk.Label(window, text=result.stdout)
	stdout_label.pack()
	stderr_label = tk.Label(window, text=result.stderr)
	stderr_label.pack()

# GUI part
window.title("Describing "+ args[0])

image = Image.open(args[0])

# Define the maximum desired size
max_desired_width = 600
max_desired_height = 600

# Calculate the aspect ratio of the original image
original_width, original_height = image.size
aspect_ratio = original_width / original_height

# Calculate the new dimensions while maintaining the aspect ratio
if max_desired_width / max_desired_height >= aspect_ratio:
    new_width = int(max_desired_height * aspect_ratio)
    new_height = max_desired_height
else:
    new_width = max_desired_width
    new_height = int(max_desired_width / aspect_ratio)

# Resize the image
resized_image = image.resize((new_width, new_height), Image.LANCZOS)

photo = ImageTk.PhotoImage(resized_image)

# Create a label for the image
image_label = tk.Label(window, image=photo)
image_label.pack()

working_label.pack()

window.after(100,call_show_result)

# Run the application
window.mainloop()

