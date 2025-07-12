import argparse

import PIL
from PIL import Image
#import requests
import torch
from diffusers import StableDiffusionInstructPix2PixPipeline, EulerAncestralDiscreteScheduler

parser = argparse.ArgumentParser(prog='modify', usage='%(prog)s prompt input_image_file output_image_file')
parser.add_argument("-p", "--prompt", nargs='+', required=True, help="Prompt")
parser.add_argument("-i", "--input", nargs='+', required=True, help="Input image file")
parser.add_argument("-o", "--output", nargs='+', required=True, help="output image file")
parser.add_argument("-d", "--disable_progress_bar", action='store_true', required=False, help="Disable progress bar")
args = parser.parse_args()
args.prompt=' '.join(args.prompt)
args.input=' '.join(args.input)
args.output=' '.join(args.output)

model_id = "timbrooks/instruct-pix2pix"
pipe = StableDiffusionInstructPix2PixPipeline.from_pretrained(model_id,
        torch_dtype=torch.float16,
        safety_checker=None,
        requires_safety_checker=False,
)

pipe.to("cuda")
if args.disable_progress_bar:
	pipe.set_progress_bar_config(disable=True)
pipe.scheduler = EulerAncestralDiscreteScheduler.from_config(pipe.scheduler.config)

image = Image.open(args.input)
images = pipe(args.prompt, image=image, num_inference_steps=10, image_guidance_scale=1).images
images[0].save(args.output)

