from PIL import Image
import os
import shutil


def convert_image_to_jpg(img_path):
    image = Image.open(img_path)

    if image.format != 'JPEG':
        # Split the file name and the extension
        file_root, _ = os.path.splitext(img_path)

        # convert the image to jpg and save it
        image = image.convert('RGB')  # Convert RGBA images to RGB format
        jpg_image_path = f'{file_root}.jpg'
        image.save(jpg_image_path)

        print(f'Image saved as {jpg_image_path}')
        return jpg_image_path
    else:
        print('Image is already JPEG format')
        return img_path


def is_image_corrupt(image_path):
    try:
        img = Image.open(image_path)
        img.verify()  # verify that it is, in fact, an image
        return False
    except (IOError, SyntaxError) as e:
        print('Bad file:', e, image_path)
        return True


def rename_image(current_img_path, new_img_name):
    dir_name, old_file_name = os.path.split(current_img_path)
    old_name, file_extension = os.path.splitext(old_file_name)
    new_img_path = os.path.join(dir_name, str(new_img_name) + file_extension)

    if os.path.exists(current_img_path):
        os.rename(current_img_path, new_img_path)
        print(f"Image renamed to: {new_img_path}")
    else:
        print(f"Image at {current_img_path} does not exist.")


def process_files(dir_path):
    for root, directories, files in os.walk(dir_path):
        i = 0
        for file in files:
            file_path = os.path.join(root, file)
            print(f"Processing file: {file_path}")
            is_image_corrupt(file_path)
            convert_image_to_jpg(file_path)
            rename_image(file_path, i)
            i += 1


def zip_directory(input_dir, output_filename):
    shutil.make_archive(output_filename, 'zip', input_dir)
    print(f"Directory {input_dir} zipped into {output_filename}.zip")

cwd = os.getcwd()
cwd = os.path.join(cwd, 'schilderijen')

process_files(cwd)
zip_directory(cwd, 'schilderijen')
