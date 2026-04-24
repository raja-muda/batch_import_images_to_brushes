bl_info = {
    "name": "Batch Import Images to Brushes",
    "author": "Raja Muda",
    "description": "Import multiple images as texture paint and sculpt brushes",
    "blender": (4, 4, 0),
    "version": (1, 0, 1),
    "location": "File > Import > Images as Brushes",
    "category": "Import-Export",
}

import bpy
from bpy.props import *
import pathlib
import os
import tempfile

ALLOWED_FILE_TYPES = ['PNG', 'JPEG', 'JPEG2000', 'BMP', 'TIFF', 'TARGA', 'WEBP', 'HDR']

# ==========================================================
# Properties Group for Brush Settings
# ==========================================================

class ImportImagesAsBrushesProperties(bpy.types.PropertyGroup):
    use_name_prepost: BoolProperty(
        name="Use name prefix / suffix", 
        default=False,
        description="Prepend/append strings to brush names"
    )
    name_pre: StringProperty(
        name="Name Prefix",
        description="Prepend this to brush names"
    )
    name_post: StringProperty(
        name="Name Suffix", 
        description="Append this to brush names"
    )
    img_fake_user: BoolProperty(
        name="Fake User", 
        default=True,
        description="Assign Fake User to images"
    )
    img_use_existing: BoolProperty(
        name="Use Existing Image", 
        default=True,
        description="Use existing image if available"
    )
    texture_calculate_alpha: BoolProperty(
        name="Calculate Alpha", 
        default=True
    )
    texture_invert_alpha: BoolProperty(
        name="Invert Alpha", 
        default=False
    )
    texture_fake_user: BoolProperty(
        name="Fake User", 
        default=True
    )
    texture_interpolation: BoolProperty(
        name="Interpolation", 
        default=True
    )
    brush_type: EnumProperty(
        name="Brush Type",
        items=[
            ('TEXTURE_PAINT', "Texture Paint", "Create texture paint brushes"),
            ('SCULPT', "Sculpt", "Create sculpt brushes"),
            ('BOTH', "Both", "Create both brush types")
        ],
        default='BOTH'
    )
    tp_strength: FloatProperty(
        name="Strength", 
        default=1.0, 
        min=0.0, 
        max=2.0
    )
    tp_size: IntProperty(
        name="Size", 
        default=50, 
        min=1, 
        max=500
    )
    sculpt_strength: FloatProperty(
        name="Strength", 
        default=0.5, 
        min=0.0, 
        max=2.0
    )
    sculpt_size: IntProperty(
        name="Size", 
        default=50, 
        min=1, 
        max=500
    )
    sculpt_tool: EnumProperty(
        name="Tool",
        items=[
            ('DRAW', "Draw", "Draw brush"),
            ('CLAY', "Clay", "Clay brush"),
            ('SMOOTH', "Smooth", "Smooth brush"),
            ('CREASE', "Crease", "Crease brush"),
            ('FLATTEN', "Flatten", "Flatten brush"),
            ('FILL', "Fill", "Fill brush"),
        ],
        default='DRAW'
    )
    generate_preview: BoolProperty(
        name="Generate Preview",
        default=True,
        description="Generate brush preview thumbnail from image"
    )

# ==========================================================
# Main Import Operator
# ==========================================================

class IMPORT_OT_images_as_brushes(bpy.types.Operator):
    bl_idname = "import_images.as_brushes"
    bl_label = "Import Images as Brushes"
    bl_options = {'REGISTER', 'UNDO'}

    directory: StringProperty(subtype='DIR_PATH')
    files: CollectionProperty(type=bpy.types.OperatorFileListElement)

    def execute(self, context):
        props = context.scene.import_images_as_brushes_props
        created_count = 0
        
        for file in self.files:
            if self.load_image_as_brush(file, context, props):
                created_count += 1
        
        if created_count > 0:
            self.report({'INFO'}, f"Successfully created {created_count} brush(es)")
            self.refresh_brush_ui(context)
        else:
            self.report({'WARNING'}, "No brushes were created")
        
        return {'FINISHED'}

    def generate_brush_preview(self, brush, image, props):
        """Generate a preview thumbnail for the brush from the image texture"""
        if not props.generate_preview:
            return
        
        try:
            # Mark as asset first
            if hasattr(brush, 'asset_mark'):
                brush.asset_mark()
            
            # Create a scaled copy of the image for icon
            temp_image = image.copy()
            temp_image.name = f"__temp_icon_{brush.name}"
            
            # Scale to reasonable icon size (256x256)
            if temp_image.size[0] > 256 or temp_image.size[1] > 256:
                temp_image.scale(256, 256)
            
            # Save to temporary file
            temp_dir = tempfile.gettempdir()
            icon_filename = f"bl_brush_{brush.name.replace('.', '_')}.png"
            icon_filepath = os.path.join(temp_dir, icon_filename)
            temp_image.filepath_raw = icon_filepath
            temp_image.save()
            
            # Set custom icon for brush (Blender 3.x/4.x method)
            if hasattr(brush, 'use_custom_icon'):
                brush.use_custom_icon = True
                brush.icon_filepath = icon_filepath
            
            # Generate asset preview (Blender 3.0+)
            if hasattr(bpy.ops.ed, 'lib_id_generate_preview'):
                try:
                    override = {'id': brush}
                    bpy.ops.ed.lib_id_generate_preview(override, accept=True)
                except:
                    pass
            
            # Blender 5.x specific method
            if bpy.app.version >= (5, 0, 0):
                try:
                    with bpy.context.temp_override(id=brush):
                        bpy.ops.ed.lib_id_load_custom_preview(filepath=icon_filepath)
                except:
                    pass
            
            # Clean up temp image
            if temp_image.name in bpy.data.images:
                bpy.data.images.remove(temp_image)
            
        except Exception as e:
            print(f"Preview generation warning for {brush.name}: {e}")

    def load_image_as_brush(self, file, context, props):
        # Generate brush name
        base_name = pathlib.Path(file.name).stem
        # Remove problematic characters from name
        base_name = "".join(c for c in base_name if c.isalnum() or c in ' _-')
        
        if props.use_name_prepost:
            base_name = props.name_pre + base_name + props.name_post
        
        # Check for duplicate
        if base_name in bpy.data.brushes:
            self.report({'WARNING'}, f"Brush '{base_name}' already exists")
            return False
        
        # Load image
        filepath = os.path.join(self.directory, file.name)
        try:
            image = bpy.data.images.load(filepath, check_existing=props.img_use_existing)
            image.use_fake_user = props.img_fake_user
            image.name = base_name
            
            # Ensure image is packed
            if not image.packed_file and image.filepath:
                image.pack()
                
        except Exception as e:
            self.report({'ERROR'}, f"Failed to load {file.name}: {e}")
            return False
        
        # Create texture
        texture = bpy.data.textures.new(base_name, 'IMAGE')
        texture.use_calculate_alpha = props.texture_calculate_alpha
        texture.invert_alpha = props.texture_invert_alpha
        texture.use_fake_user = props.texture_fake_user
        texture.use_interpolation = props.texture_interpolation
        texture.image = image
        
        # Create brushes based on type
        created = False
        
        if props.brush_type in {'TEXTURE_PAINT', 'BOTH'}:
            try:
                brush = bpy.data.brushes.new(name=base_name, mode='TEXTURE_PAINT')
                brush.color = (1.0, 1.0, 1.0)
                brush.strength = props.tp_strength
                brush.size = props.tp_size
                brush.texture = texture
                
                self.generate_brush_preview(brush, image, props)
                
                self.report({'INFO'}, f"Created texture paint brush: {base_name}")
                created = True
            except Exception as e:
                self.report({'ERROR'}, f"Failed to create texture paint brush: {e}")
        
        if props.brush_type in {'SCULPT', 'BOTH'}:
            try:
                brush = bpy.data.brushes.new(name=base_name, mode='SCULPT')
                brush.strength = props.sculpt_strength
                brush.size = props.sculpt_size
                if hasattr(brush, 'tool'):
                    brush.tool = props.sculpt_tool
                brush.texture = texture
                
                self.generate_brush_preview(brush, image, props)
                
                self.report({'INFO'}, f"Created sculpt brush: {base_name}")
                created = True
            except Exception as e:
                self.report({'ERROR'}, f"Failed to create sculpt brush: {e}")
        
        return created

    def refresh_brush_ui(self, context):
        """Force UI refresh to show new brushes and previews"""
        for window in context.window_manager.windows:
            for area in window.screen.areas:
                if area.type in {'FILE_BROWSER', 'VIEW_3D', 'PROPERTIES'}:
                    area.tag_redraw()
        
        try:
            current_mode = context.mode
            if current_mode == 'PAINT_TEXTURE':
                bpy.ops.paint.texture_paint_toggle()
                bpy.ops.paint.texture_paint_toggle()
            elif current_mode == 'SCULPT':
                bpy.ops.sculpt.sculptmode_toggle()
                bpy.ops.sculpt.sculptmode_toggle()
        except Exception:
            pass

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

# ==========================================================
# Menu Classes
# ==========================================================

class IMPORT_MT_images_as_brushes_menu(bpy.types.Menu):
    bl_label = "Images as Brushes"
    bl_idname = "IMPORT_MT_images_as_brushes_menu"
    
    def draw(self, context):
        self.layout.operator(IMPORT_OT_images_as_brushes.bl_idname, icon='BRUSHES_ALL')

def menu_func_import(self, context):
    self.layout.operator(IMPORT_OT_images_as_brushes.bl_idname, icon='BRUSHES_ALL')

# ==========================================================
# Settings Panel
# ==========================================================

class IMPORT_PT_images_as_brushes_settings(bpy.types.Panel):
    bl_label = "Brush Settings"
    bl_idname = "IMPORT_PT_images_as_brushes_settings"
    bl_space_type = 'FILE_BROWSER'
    bl_region_type = 'TOOL_PROPS'
    
    @classmethod
    def poll(cls, context):
        return context.area and context.area.type == 'FILE_BROWSER'
    
    def draw(self, context):
        layout = self.layout
        props = context.scene.import_images_as_brushes_props
        
        box = layout.box()
        box.label(text="Brush Creation", icon='BRUSH_DATA')
        box.prop(props, "brush_type", expand=True)
        
        if props.brush_type in {'TEXTURE_PAINT', 'BOTH'}:
            box = layout.box()
            box.label(text="Texture Paint Settings", icon='TPAINT_HLT')
            box.prop(props, "tp_strength")
            box.prop(props, "tp_size")
        
        if props.brush_type in {'SCULPT', 'BOTH'}:
            box = layout.box()
            box.label(text="Sculpt Settings", icon='SCULPTMODE_HLT')
            box.prop(props, "sculpt_strength")
            box.prop(props, "sculpt_size")
            box.prop(props, "sculpt_tool")
        
        box = layout.box()
        box.label(text="Naming", icon='SORTALPHA')
        box.prop(props, "use_name_prepost")
        if props.use_name_prepost:
            row = box.row()
            row.prop(props, "name_pre")
            row.prop(props, "name_post")
        
        box = layout.box()
        box.label(text="Preview Settings", icon='IMAGE_DATA')
        box.prop(props, "generate_preview")

# ==========================================================
# Registration
# ==========================================================

classes = (
    ImportImagesAsBrushesProperties,
    IMPORT_OT_images_as_brushes,
    IMPORT_MT_images_as_brushes_menu,
    IMPORT_PT_images_as_brushes_settings,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    
    bpy.types.Scene.import_images_as_brushes_props = PointerProperty(type=ImportImagesAsBrushesProperties)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)
    
    print("Batch Import Images to Brushes addon registered successfully")

def unregister():
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)
    del bpy.types.Scene.import_images_as_brushes_props
    
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    
    print("Batch Import Images to Brushes addon unregistered successfully")

if __name__ == "__main__":
    register()
