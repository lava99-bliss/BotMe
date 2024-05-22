import os
import random


image_folder = "./PhotoChat/"

# List all files in the image folder
image_files = os.listdir(image_folder)
random_image = random.choice(image_files)
print(random_image)
