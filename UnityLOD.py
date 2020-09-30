# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name" : "Unity LOD Generator",
    "author" : "Mitchell Palmer",
    "description" : "Generate decimated level of detail objects for selected objects",
    "blender" : (2, 80, 0),
    "version" : (0, 0, 1),
    "location" : "",
    "warning" : "",
    "category" : "Object"
}

import bpy

class Generate_LODs(bpy.types.Operator):
    """Generate decimated level of detail objects for selected objects"""  # Use this as a tooltip for menu items and buttons.
    bl_idname = "object.gen_lods"        # Unique identifier for buttons and menu items to reference.
    bl_label = "Generate LODs"         # Display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    
    
    def build_LOD(self, obj, name, decimation):
        new_obj = obj.copy()
        new_obj.data = obj.data.copy()
        new_obj.animation_data_clear()
        new_mod = new_obj.modifiers.new("Decimate", "DECIMATE")
        new_mod.ratio = decimation
        new_obj.name = name
        new_obj.data.name = name
        obj.users_collection[0].objects.link(new_obj)
        
    def execute(self, context):        # execute() is called when running the operator.
        decimations = [0,.5,.2]
    
        for obj in bpy.context.selected_objects:
            # build decimated levels
            if obj is not None:
                print(obj.name)
                for i in range(1, len(decimations)):
                    self.build_LOD(obj, obj.name+"_LOD"+str(i), decimations[i])
                 
                # rename original         
                obj.name = obj.name+"_LOD0"
                obj.data.name = obj.name+"_LOD0"
        return {'FINISHED'} 
    

def menu_func(self, context):
    self.layout.operator(Generate_LODs.bl_idname)
    
def register():
    bpy.utils.register_class(Generate_LODs)
    bpy.types.VIEW3D_MT_object.append(menu_func)

def unregister():
    bpy.utils.unregister_class(Generate_LODs)
    
if __name__ == "__main__":
    register()
