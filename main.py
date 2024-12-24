from urdf2webots.importer import convertUrdfFile
from tkinter import Tk     # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import askdirectory
import os
import json
import shutil
import proto_praser as proto

Folder_Object = {'Dir': {}, 'File': []}

# ================== File Browser ==================
Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
input_path = askdirectory() # show an "Open" dialog box and return the path to the selected file
folder_name = input_path.split(r"/")[-1] # get the file name
print("Selected Folder: ", folder_name)

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
texture_path = os.path.join(input_path, "textures").replace("\\", "/")                      # get the texture path

output_path = askdirectory() # show an "Open" dialog box and return the path to the selected file

# setup mesh file and texture to relative path with the output_path
try:
    # Copy the mesh_path folder and its contents to the output_path
    shutil.copytree(mesh_path, os.path.join(output_path, "meshes_"+folder_name))
    # Copy the texture_path folder and its contents to the output_path
    shutil.copytree(texture_path, os.path.join(output_path, "textures_"+folder_name))
except Exception as e:
    print(e)

# ================== Convert URDF to PROTO ==================
# convert the urdf file to proto file
proto_Filename = file_name.replace(".urdf", ".proto").replace("_", "")          # remove the "_" in the filename
proto_Filename = os.path.join(output_path, proto_Filename).replace('\\', '/')   # replace the backslash to slash
l = convertUrdfFile(input = Urdf_File , output = output_path)                   # convert the urdf file to proto file

# read the output file and replace the mesh path to relative path
with open(proto_Filename, 'r', encoding='utf-8') as file:
    datas = file.readlines()
    # print(datas)
    try:
        for i in range(len(datas)):
            l = datas[i]
            if "url" in l:
                l = l.replace("\\", "/")
                if mesh_path in l:
                    # print(l)
                    l = l.replace(mesh_path, './meshes_'+folder_name)    # replace the mesh path to relative path
                    # l = l.replace
                    # print(l)
                datas[i] = l
    except Exception as e:
        print("error occurs:\t", e)

with open(proto_Filename, 'w', encoding='utf-8') as file:
    file.writelines(datas)

# ================== Solid Reference ==================
proto_bot = proto.proto_robot(proto_filename = proto_Filename)
l = proto_bot.search("endPoint")

# search empty solid and remove some properties
for i in l:
    Reference_Template = proto.Node(name = "endPoint", parent = None, DEF = "SolidReference {")
    
    ## Reference Template:
    ## ==========================================
    ## SolidReference {
    ##   SFString solidName ""   # any string
    ## }
    ## ==========================================
    
    n = i.search("name") #search for name property
    name = ""
    
    if len(n) >= 1: #if name property is found
        name = n[0].content #get the name
    
    # check if the node is a solid and empty
    if "Solid" in i.DEF and "Empty" in name:
        name_object = i.search("name")
        if len(name_object) >= 1:
            name_object = name_object[0].content
        else:
            name_object = None
        
        if name_object and "Ref" not in name_object:
            # print
            i.DEF = "SolidReference {"
            i.children = []
            i.add_child(proto.property(name = "solidName", parent = i, content = name_object[:-1:]+"_Ref\"", stage = i.stage+1))

# ================== Motor Torque Setting ==================
l = proto_bot.search("RotationalMotor")     # search for RotationalMotor node

for i in l:
    t = i.search("maxTorque")
    Reference_Template = proto.property(name = "maxTorque", parent = t[0].parent, content = "0.001", stage = t[0].stage)
    if t[0].stage >6:
        temp = i
        proto_bot.set_current(t[0])
        proto_bot.cursor.update(Reference_Template)   # replace the maxTorque property with the Reference_Template
        proto_bot.set_current(temp)
    # t = i.search("maxTorque")   
    # print("content: ",t[0],"\tstage: ",t[0].stage, "\tparent name: ",t[0].parent.search("name")[0])

# save the proto file
proto_bot.save_robot(proto_Filename)