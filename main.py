from urdf2webots.importer import convertUrdfFile
from tkinter import Tk     # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import askdirectory
import os
import json
import shutil
Folder_Object = {'Dir': {}, 'File': []}


Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing

input_path = askdirectory() # show an "Open" dialog box and return the path to the selected file
# lookup all the files and folders in the input_path
for root, dirs, files in os.walk(input_path):
    rt = os.path.relpath(root, input_path)
    if rt == '.':   # if the root is the input_path
        rt = ''
        for d in dirs:
            Folder_Object['Dir'][d] = {'Dir':{}, 'File':[]}
        Folder_Object['File'] = files
    else:   # if the root is not the input_path
        for d in dirs:
            temp = {d: {'Dir':[], 'File':[]} }
            Folder_Object['Dir'][rt]['Dir'].append(temp)
        Folder_Object['Dir'][rt]['File'] = files

# # debugging: print the Folder_Object
# try:
#     with open('Folder_Object.json', 'w') as f:
#         json.dump(Folder_Object, f)
# except Exception as e:
#     print(e)

file_name = list(filter(lambda x: ".urdf" in x,Folder_Object["Dir"]["urdf"]["File"]))[0]    # get the urdf file name
Urdf_File = os.path.join(input_path, "urdf", file_name ).replace("\\", "/")                 # get the urdf file path
mesh_path = os.path.join(input_path, "meshes").replace("\\", "/")                           # get the mesh path

output_path = askdirectory() # show an "Open" dialog box and return the path to the selected file

# setup mesh file to relative path with the output_path
try:
    # Copy the mesh_path folder and its contents to the output_path
    shutil.copytree(mesh_path, os.path.join(output_path, "meshes"))
except Exception as e:
    print(e)

# convert the urdf file to proto file
proto_Filename = file_name.replace(".urdf", ".proto").replace("_", "")          # remove the "_" in the filename
proto_Filename = os.path.join(output_path, proto_Filename).replace('\\', '/')   # replace the backslash to slash
l = convertUrdfFile(input = Urdf_File , output = output_path)                   # convert the urdf file to proto file

# read the output file and replace the mesh path to relative path
with open(proto_Filename, 'r', encoding='utf-8') as file:
    datas = file.readlines()
    # print(datas)
    for i in range(len(datas)):
        l = datas[i]
        if "url" in l:
            l = l.replace("\\", "/")
            if mesh_path in l:
                print(l)
                l = l.replace(mesh_path, './meshes')
                print(l)
            datas[i] = l

with open(proto_Filename, 'w', encoding='utf-8') as file:
    file.writelines(datas)

