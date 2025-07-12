import subprocess
import sys
import tkinter as tk
from PIL import Image, ImageTk
import os

script_path = os.path.dirname(__file__)

command = ['python3', script_path+'/remove_bg.py']
args = sys.argv.copy()
args.pop(0) # remove argv[0] which is the script's name

output_tk_image = None

window = tk.Tk()

def call_show_result():
	full_command = command + args
	result = subprocess.run(full_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

	working_label.destroy()

	filename_label = tk.Label(window, text=args[1])
	filename_label.pack()

	output_image = Image.open(args[1])
	resized_output_image=resize_image(output_image)
	global output_tk_image
	output_tk_image = ImageTk.PhotoImage(resized_output_image)
	output_image_label = tk.Label(window, image=output_tk_image)
	output_image_label.pack()

	# Create a label for the string
	stdout_label = tk.Label(window, text=result.stdout)
	stdout_label.pack()
	stderr_label = tk.Label(window, text=result.stderr)
	stderr_label.pack()

def resize_image(image):
	# Define the maximum desired size
	max_desired_width = 400
	max_desired_height = 400

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
	return image.resize((new_width, new_height), Image.LANCZOS)

# GUI part
window.title("Removing background of "+ args[0])

working_label = tk.Label(window, text=args[0])
working_label.pack()

input_image = Image.open(args[0])
resized_input_image=resize_image(input_image)
input_tk_image = ImageTk.PhotoImage(resized_input_image)
input_image_label = tk.Label(window, image=input_tk_image)
input_image_label.pack()

working_label = tk.Label(window, text="Working...")
working_label.pack()

window.after(100,call_show_result)

# Run the application
window.mainloop()

