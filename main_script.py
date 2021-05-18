bl_info = {
    "name": "Toontown .egg Updater",
    "description": "Adds buttons to the top bar to fix importing toontown .egg files in Blender 2.79b.",
    "author": "blockobun",
    "version": (0, 1, 0),
    "blender": (2, 79, 0),
    "location": "Info (top panel buttons)",
    "category": "Development"}

import bpy
#from bpy_extras.io_utils import ImportHelper

#class ot_choose_folder(bpy.types.Operator, ImportHelper):
#    bl_idname = "choose.folder"
#    bl_label = "Select folder to create files"
#
#    filename_ext = "."
#    def execute(self, context):
#        exportPath = self.filepath #set file
#        exportPath = exportPath.replace(".egg", "") #gets rid of weird .egg extension added by default
#        objectImportCounter = 0
#        for obj in bpy.data.objects:
#            if obj.type == "MESH":
#                obj.select = True
#                objectImportCounter = objectImportCounter + 1 #adds 1 for each new file (so the same name isn't used multiple times)
#                bpy.ops.export_scene.fbx(filepath = exportPath + str(objectImportCounter) + ".fbx", use_selection = True) #use selection for export
#                obj.select = False
#        return {"FINISHED"}

class egg_Update(bpy.types.Operator):
    bl_idname = "egg.update"
    bl_label = "Update .egg Model"
    bl_options = {"REGISTER", "UNDO"}
    def execute(self, context):
        for mat in bpy.data.materials:
            mat.use_shadeless = True
            mat.use_transparency = True
            mat.use_vertex_color_paint = True
            mat.alpha = 0
            for tSlot in mat.texture_slots:
                if tSlot is not None:
                    tSlot.use_map_alpha = True
                    tSlot.alpha_factor = 1
        #set viewport to textured mode, to show changes
        for area in bpy.context.screen.areas:
            if area.type == "VIEW_3D":
                for space in area.spaces:
                    if space.type == "VIEW_3D":
                        space.viewport_shade = "TEXTURED"
        return {"FINISHED"}

class egg_ConvPng(bpy.types.Operator):
    bl_idname = "egg.jpg2png"
    bl_label = "Convert .jpg to .png"
    bl_options = {"REGISTER", "UNDO"}
    def execute(self, context):
        oldtype = ".jpg"
        newtype = ".png"
        for image in bpy.data.images:
            if not image.filepath.endswith(oldtype):
                continue #ignore this image if it does not end in .jpg
            image.filepath = image.filepath.replace(oldtype, newtype)
            image.name = image.name.replace(oldtype, newtype)
            image.reload() #show changes in real time
        return {"FINISHED"}

class egg_SelCol(bpy.types.Operator):
    bl_idname = "egg.selcol"
    bl_label = "Select Collision"
    bl_options = {"REGISTER", "UNDO"}
    def execute(self, context):
        bpy.ops.object.select_all(action = "DESELECT") #make sure our selection is empty (so it doesn't bug out)
        for obj in bpy.data.objects:
            if obj.type == "MESH":
                noMaterial = False
                abortedSearch = False
                for slot in obj.material_slots:
                    if slot.material == None:
                        noMaterial = True
                    else:
                        noMaterial = False
                        abortedSearch = True
                if noMaterial and not abortedSearch:
                    noMaterial = False
                    abortedSearch = False
                    obj.select = True #select the collision (so we can either hide/delete it or keep it
        return {"FINISHED"}

#class egg_ExportRBX(bpy.types.Operator):
#    bl_idname = "egg.exportrbx"
#    bl_label = "Export .egg to Roblox"
#    bl_options = {"REGISTER", "UNDO"}
#    def execute(self, context):
#        #bpy.ops.object.select_all(action = "SELECT")
#        for obj in bpy.data.objects:
#            if obj.type == "MESH":
#                context.scene.objects.active = obj
#                obj.select = True
#        
#        bpy.ops.object.join() #combine all geometry to one object
#        bpy.ops.mesh.separate(type = "MATERIAL") #separate by material, as each material contains one texture (roblox only supports one texture per mesh)
#        bpy.ops.choose.folder("INVOKE_DEFAULT")
#        return {"FINISHED"}

def selector(self, context): #basically the UI
    layout = self.layout
    column = layout.column(align = True)
    row = column.row(align = True)
    row.operator("egg.update", text = ".egg update") #btn
    row.operator("egg.jpg2png", text = ".egg jpg2png") #btn
    row.operator("egg.selcol", text = ".egg select collision") #btn
    #row.operator("egg.exportrbx", text = ".egg export to Roblox") #btn

def register():
    bpy.utils.register_class(egg_Update)
    bpy.utils.register_class(egg_ConvPng)
    bpy.utils.register_class(egg_SelCol)
    #bpy.utils.register_class(ot_choose_folder)
    #bpy.utils.register_class(egg_ExportRBX)
    bpy.types.INFO_HT_header.prepend(selector) #buttons go at the beginning, for users with small blender window
 
def unregister():
    bpy.utils.unregister_class(egg_Update)
    bpy.utils.unregister_class(egg_ConvPng)
    bpy.utils.unregister_class(egg_SelCol)
    #bpy.utils.unregister_class(ot_choose_folder)
    #bpy.utils.unregister_class(egg_ExportRBX)
    bpy.types.INFO_HT_header.remove(selector)
 
if __name__ == "__main__":
    register()