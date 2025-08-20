# Copyright (C) 2019 Arturs Ontuzans
# 
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

import bpy

class UI_PT_Rig_Panel(bpy.types.Panel):
    bl_idname = "UI_PT_Rig_Panel"
    bl_label = "UE4 Vehicle Base Rigging"
    bl_category = "UE4 Vehicle"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout

        scene = context.scene
        
        layout.label(text = "Vehicle rigging", icon = 'OUTLINER_OB_ARMATURE')

        if scene.dynamic_wheel_count is True:
            row = layout.row()
            row.label(text = "Vehicle Base")
            row.prop(scene, 'vehicle_base', text = "")

            row = layout.row()
            row.operator('view3d.add_another_wheel', text = "Add Wheel")
            #row.operator('view3d.remove_chosen_wheel', text = "Remove Wheel")
            for index, item in enumerate(scene.multiple_wheels):
                row = layout.row() 
                row.prop(item, 'wheel_name', text = "")
                row.prop(item, 'wheel_mesh', text = "")
                scale_row = row.row()
                scale_row.scale_x = 0.3
                scale_row.operator('view3d.remove_chosen_wheel', text = "X").id = index
        
        else:
            row = layout.row()
            row.label(text = "Vehicle Base")
            row.prop(scene, 'vehicle_base', text = "")

            row = layout.row()
            row.label(text = "Wheel FR")
            row.prop(scene, 'wheel_FR', text = "")

            row = layout.row()
            row.label(text = "Wheel RR")
            row.prop(scene, 'wheel_RR', text = "")

            row = layout.row()
            row.label(text = "Wheel FL")
            row.prop(scene, 'wheel_FL', text = "")

            row = layout.row()
            row.label(text = "Wheel RL")
            row.prop(scene, 'wheel_RL', text = "")

        layout.separator()
        layout.label(text = "Brake Calipers", icon = 'MESH_CYLINDER')
        
        row = layout.row()
        row.label(text = "Brake Caliper FR")
        row.prop(scene, 'brake_caliper_FR', text = "")

        row = layout.row()
        row.label(text = "Brake Caliper FL")
        row.prop(scene, 'brake_caliper_FL', text = "")

        layout.separator()
        layout.label(text = "Dashboard Instruments", icon = 'MESH_CIRCLE')
        
        row = layout.row()
        row.label(text = "Speedometer Needle")
        row.prop(scene, 'speedometer_needle', text = "")

        row = layout.row()
        row.label(text = "Tachometer Needle")
        row.prop(scene, 'tachometer_needle', text = "")

        row = layout.row()
        row.prop(scene, 'dynamic_wheel_count')

        row = layout.row()
        row.prop(scene, 'bone_length')

        row = layout.row()
        row.operator('view3d.rig_vehicle', text = "Rig Vehicle")

class UI_PT_Scene_Setup_Panel(bpy.types.Panel):
    bl_idname = "UI_PT_Scene_Setup_Panel"
    bl_label = "UE4 Scene Setup"
    bl_category = "UE4 Vehicle"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout

        scene = context.scene

        layout.label(text = "Scene setup", icon = "SCENE_DATA")

        row = layout.row()
        row.operator('view3d.set_unit_scale', text = "Set Unit Scale")

        row = layout.row()
        row.operator('view3d.upscale_objects', text = "Upscale Objects")

class UI_PT_Additional_Rigging_Panel(bpy.types.Panel):
    bl_idname = "UI_PT_Additional_Rigging_Panel"
    bl_label = "Additional Bone Rigging"
    bl_category = "UE4 Vehicle"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout

        scene = context.scene

        layout.label(text = "Bone head location")

        column = layout.column()
        column.prop(scene, 'bone_head_location', text = "")

        row = layout.row()
        row.operator('view3d.set_bone_head_location', text = "Set Head Location")

        layout.label(text = "Bone tail location")

        column = layout.column()
        column.prop(scene, 'bone_tail_location', text = "")

        row = layout.row()
        row.operator('view3d.set_bone_tail_location', text = "Set Tail Location")

        row = layout.row()
        row.label(text = "Bone armature")
        row.prop(scene, 'armature_for_new_bone', text = "")


        if scene.armature_for_new_bone is not None:
            row = layout.row()
            row.label(text = "Parent bone")
            row.prop_search(scene, "armature_parent_bone_name", scene.armature_for_new_bone, "bones", icon = "BONE_DATA", text = "")
            
            row = layout.row()
            row.label(text = "New bone name")
            row.prop(scene, 'new_bone_name', text ="")

            row = layout.row()
            row.prop(scene, 'set_vertext_groups_to_selected')

            row = layout.row()
            row.prop(scene, 'end_in_pose_mode')
            
            row = layout.row()
            row.operator('view3d.add_bone_to_armature', text = "Add Bone")

        

