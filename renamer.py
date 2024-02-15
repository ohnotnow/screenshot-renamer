import glob
import os
import re
import ollama
from yaspin import yaspin
from PIL import Image
from PIL.PngImagePlugin import PngInfo

vision_model = 'llava'
text_model = 'mistral'

def ensure_required_models_available():
    models = ollama.list()
    vision_model_available = False
    text_model_available = False
    for model in models["models"]:
        if model['name'].startswith(vision_model):
            vision_model_available = True
        if model['name'].startswith(text_model):
            text_model_available = True
    if not vision_model_available:
        with yaspin(text=f"Downloading required vision model : {vision_model} (this may take a few minutes)", color="yellow") as spinner:
            ollama.pull(vision_model)
    if not text_model_available:
        with yaspin(text=f"Downloading required text model : {text_model} (this may take a few minutes)", color="yellow") as spinner:
            ollama.pull(text_model)

def add_description_to_image_metadata(file_path, description):
    with Image.open(file_path) as img:
        pnginfo = PngInfo()
        pnginfo.add_text("Description", description)
        img.save(file_path, "PNG", pnginfo=pnginfo)

def get_image_description(filename):
    response = ollama.chat(model=vision_model, messages=[
        {
            'role': 'user',
            'content': 'Could you give me a VERY short description of this image that I can use as a filename (I do not need the file extension). For example "image of a weather forecast", "screenshot of a website about a raspberry pi", "photo of a black cat"',
            'images': [filename]
        },
    ])
    return response['message']['content']

def remove_file_extension(filename):
    return os.path.splitext(filename)[0]

def get_filename_from_description(description):
    response = ollama.chat(model=text_model, messages=[
        {
            'role': 'user',
            'content': 'Could you give me some keywords from this text that I can use to tag a file (I DO NOT want a file extension). Reply ONLY with the keywords. <text>' + description + '</text>',
        },
    ])
    filename = response['message']['content'].strip()
    filename = remove_file_extension(filename)
    filename = filename.replace("\n", "")
    filename = re.sub(r'[^\w\s]+', '_', filename, flags=re.UNICODE).strip()
    filename = filename.strip('_')
    # filename = re.sub(r'(png|jpg|jpeg|gif|bmp|tiff|webp|svg|pdf|docx|doc|pptx|ppt|txt|csv|json|xml|html|css|js|ts|py|rb|java|c|cpp|h|hpp|cs|php|go|swift|kt|sh|bat|ps1|psm1|psd1|ps1xml|pssc|psc1)', '', filename, flags=re.UNICODE)
    return filename[:50]

def get_matching_files(pattern):
    files = glob.glob(pattern)
    pattern = re.compile(r'Screenshot 20\d{2}-\d{2}-\d{2} at \d{2}\.\d{2}\.\d{2}\.png')
    return [file for file in files if pattern.match(file)]

def main():
    ensure_required_models_available()

    pattern = "Screenshot *.png"
    matching_files = get_matching_files(pattern)
    if len(matching_files) == 0:
        print(f"No files found that match the pattern '{pattern}*'")
        exit(1)

    new_filenames = []
    for i, filename in enumerate(matching_files):
        print(f"Getting description of file {i+1} of {len(matching_files)}: {filename}")
        original_filename, file_extension = os.path.splitext(filename)
        description = get_image_description(filename)
        new_filenames.append({
            "original_filename": original_filename,
            "file_extension": file_extension,
            "description": description
        })
    for i, file in enumerate(new_filenames):
        print(f"Getting new filename for file {i+1} of {len(new_filenames)}: {file['original_filename']}")
        shorter_description = get_filename_from_description(file["description"])
        new_name = file["original_filename"] + "_" + shorter_description + file["file_extension"]
        os.rename(file['original_filename'] + file["file_extension"], f"{new_name}")
        add_description_to_image_metadata(new_name, description)
        print(f"Renamed {original_filename} to {new_name} and added description to metadata")

if __name__ == "__main__":
    main()
