import argparse

from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration

parser = argparse.ArgumentParser(prog='describe', usage='%(prog)s input_image_file')
parser.add_argument("input_file", help="Input image file")
args = parser.parse_args()

processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large",use_fast=True)
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large").to("cuda")

raw_image = Image.open(args.input_file).convert('RGB')

# conditional image captioning
#text = "a photography of"
#text = "a beautiful"
#inputs = processor(raw_image, text, return_tensors="pt").to("cuda")

#out = model.generate(**inputs)
#print(processor.decode(out[0], skip_special_tokens=True))

# unconditional image captioning
inputs = processor(raw_image, return_tensors="pt").to("cuda")

out = model.generate(**inputs)

result=processor.decode(out[0], skip_special_tokens=True)
print(result)
