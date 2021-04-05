import bpy
import bmesh
import math

mesh_sizeX = 30
mesh_sizeY = 14
mesh_sizeZ = 20
cell_sizeX = 2
cell_sizeY = 2
cell_sizeZ = 1.5
collumn_number = math.ceil(mesh_sizeX/cell_sizeX)
row_number = math.ceil(mesh_sizeY/cell_sizeY)
layer_number = math.ceil(mesh_sizeZ/cell_sizeZ)


Selected_Faces = []
#Selected_Faces.append("faces")
# get current mesh
current_mesh = bpy.context.object.data
# create empty bmesh, add current mesh into empty bmesh
current_bm = bmesh.new()
current_bm.from_mesh(current_mesh)



bpy.ops.object.mode_set(mode = 'EDIT')
bpy.ops.mesh.select_all(action='DESELECT')
for layer in range(layer_number):
    print("Layer" + str(layer))
    ZFloor = (layer*cell_sizeZ)-(layer_number*cell_sizeZ/2)
    ZCeil = ((layer+1)*cell_sizeZ)-(layer_number*cell_sizeZ/2)
    for collumn in range(collumn_number) :
        print("Collumn" + str(collumn))
        XFloor = (collumn*cell_sizeX)-(collumn_number*cell_sizeX/2)
        XCeil = ((collumn+1)*cell_sizeX)-(collumn_number*cell_sizeX/2)
        for line in range(row_number) :
            YFloor = (line*cell_sizeY)-(row_number*cell_sizeY/2)
            YCeil = ((line+1)*cell_sizeY)-(row_number*cell_sizeY/2)
            for obj in current_bm.faces :
                obj.select = False
            #print("line" + str(line))
            for face in current_bm.faces :
                face_location = face.calc_center_median()
                if XFloor <= face_location[0] <= XCeil:
                    if YFloor <= face_location[1] <= YCeil:
                        if ZFloor <= face_location[2] <= ZCeil:
                            face.select = True

            bpy.ops.object.mode_set(mode = 'OBJECT')
            current_bm.to_mesh(current_mesh)
            bpy.ops.object.mode_set(mode = 'EDIT')
            try:
                bpy.ops.mesh.separate(type='SELECTED')
                bpy.ops.mesh.delete()
                bpy.ops.object.mode_set(mode = 'OBJECT')
                current_bm.to_mesh(current_mesh)
                bpy.ops.object.mode_set(mode = 'EDIT')
                bpy.ops.mesh.select_all(action='DESELECT')
            except:
                pass
                
bpy.ops.object.mode_set(mode = 'OBJECT')
current_bm.to_mesh(current_mesh)

current_bm.free()