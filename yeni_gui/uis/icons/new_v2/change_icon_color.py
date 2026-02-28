import os
from PIL import Image



# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Loop through all files in the directory
for filename in os.listdir(script_dir):
    filename, file_extension = os.path.splitext(filename)
    if file_extension == ".png" and not filename.endswith("_white") and not os.path.exists(os.path.join(script_dir, filename + "_white.png")):
        print(filename)
        file_path = os.path.join(script_dir, filename + ".png")

        # Open the image file
        with Image.open(file_path) as img:
            img = img.convert("RGBA")
            data = img.getdata()

            new_data = []
            for item in data:
                # Change all non-transparent pixels to white
                if item[3] != 0:
                    new_data.append((255, 255, 255, 255))
                else:
                    new_data.append(item)

            img.putdata(new_data)
            # img.save(file_path)
            new_filename = filename + "_white.png"
            new_file_path = os.path.join(script_dir, new_filename)
            img.save(new_file_path)