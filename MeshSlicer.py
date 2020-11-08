import bpy, bmesh
from bpy import context
from  mathutils import Vector
# bounding box helper methods
def bbox(ob):
    return (Vector(b) for b in ob.bound_box)

def bbox_center(ob):
    return sum(bbox(ob), Vector()) / 8

def bbox_axes(ob):
    bb = list(bbox(ob))
    return tuple(bb[i] for i in (0, 4, 3, 1))

def slice(bm, start, end, segments):
    if segments == 1:
        return
    def geom(bm):
        return bm.verts[:] + bm.edges[:] + bm.faces[:]
    planes = [start.lerp(end, f / segments) for f in range(1, segments)]
    #p0 = start
    plane_no = (end - start).normalized() 
    while(planes): 
        p0 = planes.pop(0)                 
        ret = bmesh.ops.bisect_plane(bm, 
                geom=geom(bm),
                plane_co=p0, 
                plane_no=plane_no)
        bmesh.ops.split_edges(bm, 
                edges=[e for e in ret['geom_cut'] 
                if isinstance(e, bmesh.types.BMEdge)])


bm = bmesh.new()
ob = context.object
me = ob.data
bm.from_mesh(me)

o, x, y, z = bbox_axes(ob)        

x_segments = 2
y_segments = 2
z_segments = 1

slice(bm, o, x, x_segments)
slice(bm, o, y, y_segments)
slice(bm, o, z, z_segments)    
bm.to_mesh(me)

bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.separate(type='LOOSE')
bpy.ops.object.mode_set() 



class SliceMesh(bpy.types.Operator):
    """Reorder LOD decimations"""  # Use this as a tooltip for menu items and buttons.
    bl_idname = "object.unity_export_slice_mesh"        # Unique identifier for buttons and menu items to reference.
    bl_label = "Slice Mesh"         # Display name in the interface.
    bl_options = {'REGISTER','UNDO'}  # Enable undo for the operator.
    
    def execute(self, context):        # execute() is called when running the operator.
        scene = context.scene

        return {'FINISHED'} 