import os
import subprocess

file_directory = os.path.dirname(os.path.abspath(__file__))
uis_directory = os.path.join(file_directory, "uis")

ui_files = [file for file in os.listdir(uis_directory) if file.endswith(".ui")]
qrc_files = [file for file in os.listdir(uis_directory) if file.endswith(".qrc")]

for ui_file in ui_files:
    print(ui_file)
    command = f"pyuic5 yeni_gui/uis/{ui_file} -o yeni_gui/uis/{ui_file.replace('.ui', '.py')}"
    subprocess.run(command, shell=True)
print("Conversion completed for all .ui files.")
print()

for qrc_file in qrc_files:
    print(qrc_file)
    command = f"pyrcc5 yeni_gui/uis/{qrc_file} -o yeni_gui/uis/{qrc_file.replace('.qrc', '_rc.py')}"
    subprocess.run(command, shell=True)
print("Conversion completed for all .qrc files.")