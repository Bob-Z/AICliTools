from PIL import Image
import torch
from torchvision import transforms
from transformers import AutoModelForImageSegmentation
import sys
import argparse

# Command line management
parser = argparse.ArgumentParser(prog='remove_bg', usage='%(prog)s input_image_file output_image_file')
parser.add_argument("input_file", help="Input image file")
parser.add_argument("output_file", help="Output image file (must be PNG file for alpha channel)")
args = parser.parse_args()

# main
model = AutoModelForImageSegmentation.from_pretrained('briaai/RMBG-2.0', trust_remote_code=True)
torch.set_float32_matmul_precision(['high', 'highest'][0])
model.to('cuda')
model.eval()

# Data settings
image_size = (1024, 1024)
transform_image = transforms.Compose([
    transforms.Resize(image_size),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

image = Image.open(args.input_file)
input_images = transform_image(image).unsqueeze(0).to('cuda')

# Prediction
with torch.no_grad():
    preds = model(input_images)[-1].sigmoid().cpu()
pred = preds[0].squeeze()
pred_pil = transforms.ToPILImage()(pred)
mask = pred_pil.resize(image.size)
image.putalpha(mask)

image.save(args.output_file)

