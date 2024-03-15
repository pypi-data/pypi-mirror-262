import os

# Get the directory path where the .txt files are located
txt_dir_path = os.path.dirname(os.path.realpath(__file__))

# Define functions to print the code from .txt files
def cgan():
    read_file(os.path.join(txt_dir_path, 'cgan.txt'))

def mod1():
    read_file(os.path.join(txt_dir_path, 'mod1.txt'))

def diffusion():
    read_file(os.path.join(txt_dir_path, 'diffusion.txt'))

def rcnn():
    read_file(os.path.join(txt_dir_path, 'rcnn.txt'))

def rcnnc():
    read_file(os.path.join(txt_dir_path, 'rcnnc.txt'))

def face():
    read_file(os.path.join(txt_dir_path, 'face.txt'))

def image():
    read_file(os.path.join(txt_dir_path, 'image.txt'))

def stable():
    read_file(os.path.join(txt_dir_path, 'stable.txt'))

def vae():
    read_file(os.path.join(txt_dir_path, 'vae.txt'))

def yoloc():
    read_file(os.path.join(txt_dir_path, 'yoloc.txt'))

def yolo():
    read_file(os.path.join(txt_dir_path, 'yolo.txt'))

def read_file(filename):
    with open(filename, 'r') as file:
        print(file.read())
