import subprocess
import sys
import tkinter as tk
from PIL import Image, ImageTk
import os
import argparse

script_path = os.path.dirname(__file__)

command = ['python3', script_path+'/modify.py']
cli_args = sys.argv.copy()
cli_args.pop(0) # remove argv[0] which is the script's name

parser = argparse.ArgumentParser(prog='modify_gui', usage='%(prog)s -i input_image_file -o output_image_file')
parser.add_argument("-i", "--input", nargs='+', required=True, help="Input image file")
parser.add_argument("-o", "--output", nargs='+', required=True, help="output image file")
args = parser.parse_args()
args.input=' '.join(args.input)
args.output=' '.join(args.output)

output_tk_image = None
output_image_label = None
stdout_label = None
stderr_label = None

window = tk.Tk()

def processing():
	#button.destroy()

	full_command = command + cli_args + ["--prompt",textbox.get("1.0", tk.END), "--disable_progress_bar"]
	result = subprocess.run(full_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

	filename_label = tk.Label(window, text=args.output)
	filename_label.pack()

	global output_tk_image
	global output_image_label
	global stdout_label
	global stderr_label

	if output_image_label is not None:
		output_image_label.destroy()
		stdout_label.destroy()
		stderr_label.destroy()

	output_image = Image.open(args.output)
	resized_output_image=resize_image(output_image)
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
window.title("Modifying "+ args.input)

working_label = tk.Label(window, text=args.input)
working_label.pack()

input_image = Image.open(args.input)
resized_input_image=resize_image(input_image)
input_tk_image = ImageTk.PhotoImage(resized_input_image)
input_image_label = tk.Label(window, image=input_tk_image)
input_image_label.pack()

tips_label = tk.Label(window, text=("Use \"Make this like ...\" or \"Turn this into ...\""))
tips_label.pack()

textbox = tk.Text(window, width=100, height=1)
textbox.pack()

button = tk.Button(window, width=10, height=1, text='MODIFY', command=processing)
button.pack()

# Run the application
window.mainloop()

