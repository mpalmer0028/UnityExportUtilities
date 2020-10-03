import bpy
from bpy.props import StringProperty, IntProperty, CollectionProperty, FloatProperty
from bpy.types import PropertyGroup, UIList, Operator, Panel

DEFAULT_DECIMATIONS = [1, 0.5, 0.2, 0.1]

"""
OPERATIONS
"""
class Add_Decimation(bpy.types.Operator):
    """Generate decimated level of detail objects for selected objects"""  # Use this as a tooltip for menu items and buttons.
    bl_idname = "object.unity_export_add_decimation"        # Unique identifier for buttons and menu items to reference.
    bl_label = "Add LOD"         # Display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    
    def execute(self, context):        # execute() is called when running the operator.
        scene = context.scene
        print(scene.decimationField)
        dec = scene.decimations.add()
        dec.value = scene.decimationField
        bpy.ops.object.unity_export_reorder_decimations()
        return {'FINISHED'}    
    
class Reorder_Decimation(bpy.types.Operator):
    """Reorder LOD decimations"""  # Use this as a tooltip for menu items and buttons.
    bl_idname = "object.unity_export_reorder_decimations"        # Unique identifier for buttons and menu items to reference.
    bl_label = "Reorder LOD"         # Display name in the interface.
    bl_options = {'REGISTER'}  # Enable undo for the operator.
    
    def sorter(v,x):
        #print(v.name)
        #print(x.name)
        return x.value
    
    def execute(self, context):        # execute() is called when running the operator.
        scene = context.scene
        values = scene.decimations.values()
        #values.sort(key=self.sorter, reverse=False)
        
        ratios = []
        for v in values:
            ratios.append(v.value)
            
        ratios.sort(reverse=True)
        scene.decimations.clear()
        
        for r in ratios:
            dec = scene.decimations.add()
            dec.value = r
        return {'FINISHED'} 

class Remove_Decimation(bpy.types.Operator):
    """Remove LOD decimations"""  # Use this as a tooltip for menu items and buttons.
    bl_idname = "object.unity_export_remove_decimation"        # Unique identifier for buttons and menu items to reference.
    bl_label = "Remove LOD"         # Display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.
    
    def execute(self, context):        # execute() is called when running the operator.
        scene = context.scene
        values = scene.decimations.remove(scene.decimationI)
        return {'FINISHED'} 
        
"""
LAYOUT
"""
class DecimationItem(PropertyGroup): 
    value: FloatProperty(name="Value", description="Ratios for LOD decimations. Between 0-1", 
    default=1.0, min=0.000, max=1.0, step=.1, precision=4)

class DECIMATION_UL_List(UIList):
    # The draw_item function is called for each item of the collection that is visible in the list.
    #   data is the RNA object containing the collection,
    #   item is the current drawn item of the collection,
    #   icon is the "computed" icon for the item (as an integer, because some objects like materials or textures
    #   have custom icons ID, which are not available as enum items).
    #   active_data is the RNA object containing the active property for the collection (i.e. integer pointing to the
    #   active item of the collection).
    #   active_propname is the name of the active property (use 'getattr(active_data, active_propname)').
    #   index is index of the current item in the collection.
    #   flt_flag is the result of the filtering process for this item.
    #   Note: as index and flt_flag are optional arguments, you do not have to use/declare them here if you don't
    #         need them.
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index): 
        if self.layout_type in {'DEFAULT', 'COMPACT'}: 
            if item.value == 1:
                labelText = 'LOD_0 Full Detail'
                layout.label(text=labelText, icon = 'MESH_PLANE') 
            else:
                labelText = 'LOD_{} ({:.2f}%)'.format(index, item.value*100)
                layout.label(text=labelText, icon = 'MOD_DECIM') 
        elif self.layout_type in {'GRID'}: 
            layout.alignment = 'CENTER' 
            layout.label(text="", icon = 'MESH_PLANE')
            
class UNITY_EXPORT_UTILITIES_PT_PANEL(Panel):
    bl_category = "Edit"
    bl_label = "Unity Export Utilities"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_context = "objectmode"
    bl_options = {'DEFAULT_CLOSED'}

    def draw_header(self, context):
        layout = self.layout
        obj = context.object
        #layout.prop(obj, "select", text="")

    def draw(self, context):
        layout = self.layout

        obj = context.object
        scene = context.scene
        row = layout.row()
        row.label(text="Level of Detail Decimations")
        row = layout.row()
        row.template_list("DECIMATION_UL_List", "", scene, "decimations", scene, "decimationI")
        row = layout.row()
        row.prop(scene, "decimationField", text="New Decimation")
        row = layout.row()
        row.operator("object.unity_export_add_decimation", text="Add")
        row.operator("object.unity_export_remove_decimation", text="Remove")
        
def register():
    bpy.utils.register_class(Add_Decimation)
    bpy.utils.register_class(Reorder_Decimation)
    bpy.utils.register_class(Remove_Decimation)
    bpy.utils.register_class(DecimationItem)
    bpy.utils.register_class(UNITY_EXPORT_UTILITIES_PT_PANEL)
    bpy.utils.register_class(DECIMATION_UL_List)  
    bpy.types.Scene.decimationField = FloatProperty(name="decimationField", description="Enter a ratio for the LOD's decimation. Between 0-1", 
    default=0.5, min=0.000, max=1.0, step=.1, precision=4)     
    bpy.types.Scene.decimations = CollectionProperty(type=DecimationItem)
    
    
        
    bpy.types.Scene.decimationI = IntProperty(name="decimationI", description="Decimation index", default=0)
    #bpy.types.Scene.decimations.clear()
    bpy.app.handlers.scene_update_post.append(onRegister)
def unregister():
    del bpy.types.Scene.decimationField
    del bpy.types.Scene.decimations
    del bpy.types.Scene.decimationI
    bpy.utils.unregister_class(UNITY_EXPORT_UTILITIES_PT_PANEL)
    bpy.utils.unregister_class(DECIMATION_UL_List)
    bpy.utils.unregister_class(DecimationItem)
    bpy.utils.unregister_class(Add_Decimation)
    bpy.utils.unregister_class(Remove_Decimation)
    bpy.utils.unregister_class(Reorder_Decimation)


def onRegister(scene):
    for d in DEFAULT_DECIMATIONS:
        dec = bpy.context.scene.decimations.add()
        dec.value = d
    # the handler isn't needed anymore, so remove it
    bpy.app.handlers.scene_update_post.remove(onRegister)
    
#    bpy.utils.register_class(Decimation_UL_List)

if __name__ == "__main__":
    register()