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

bl_info = {
    "name" : "Unreal Engine 4 Vehicle Rigger",
    "author" : "Arturs Ontuzans",
    "description" : "Helps to rig vehicles for Unreal Engine 4/5",
    "blender" : (3, 4, 0),
    "version" : (0, 6, 2),
    "location" : "View3D",
    "warning" : "",
    "category" : "Generic"
}

import bpy

from . rig_op import Rig_OT_Operator, Scale_Units_OT_Operator, Upscale_Objects_OT_Operator
from . rig_op import Set_Bone_Head_Location_OT_Operator, Set_Bone_Tail_Location_OT_Operator, Add_Bone_To_Armature_OT_Operator
from . rig_op import Add_Another_Wheel_OT_Operator, Remove_Chosen_Wheel_OT_Operator

from . ui_panel import UI_PT_Rig_Panel, UI_PT_Scene_Setup_Panel, UI_PT_Additional_Rigging_Panel

def object_search_poll(self, object):
    return object.type in ['MESH', 'CURVE']

class WheelItem(bpy.types.PropertyGroup):
    wheel_name: bpy.props.StringProperty()
    wheel_mesh: bpy.props.PointerProperty(type=bpy.types.Object, poll = object_search_poll, description = "Wheel mesh")

def register():
    bpy.utils.register_class(WheelItem)
    bpy.utils.register_class(Rig_OT_Operator)
    bpy.utils.register_class(Scale_Units_OT_Operator)
    bpy.utils.register_class(Upscale_Objects_OT_Operator)
    bpy.utils.register_class(Set_Bone_Head_Location_OT_Operator)
    bpy.utils.register_class(Set_Bone_Tail_Location_OT_Operator)
    bpy.utils.register_class(Add_Bone_To_Armature_OT_Operator)
    bpy.utils.register_class(Add_Another_Wheel_OT_Operator)
    bpy.utils.register_class(Remove_Chosen_Wheel_OT_Operator)
    bpy.utils.register_class(UI_PT_Rig_Panel)
    bpy.utils.register_class(UI_PT_Additional_Rigging_Panel)
    bpy.utils.register_class(UI_PT_Scene_Setup_Panel)
    bpy.types.Scene.vehicle_base = bpy.props.PointerProperty(type=bpy.types.Object, poll = object_search_poll, name= "Vehicle base mesh", description = "Vehicle Base mesh")
    bpy.types.Scene.wheel_FR = bpy.props.PointerProperty(type=bpy.types.Object, poll = object_search_poll, name= "Wheel FR", description = "Front Right Vehicle Wheel mesh")
    bpy.types.Scene.wheel_FL = bpy.props.PointerProperty(type=bpy.types.Object, poll = object_search_poll, name= "Wheel FL", description = "Front Left Vehicle Wheel mesh")
    bpy.types.Scene.wheel_RR = bpy.props.PointerProperty(type=bpy.types.Object, poll = object_search_poll, name= "Wheel RR", description = "Rear Right Vehicle Wheel mesh")
    bpy.types.Scene.wheel_RL = bpy.props.PointerProperty(type=bpy.types.Object, poll = object_search_poll, name= "Wheel RL", description = "Rear Left Vehicle Wheel mesh")
    bpy.types.Scene.brake_caliper_FR = bpy.props.PointerProperty(type=bpy.types.Object, poll = object_search_poll, name= "Brake Caliper FR", description = "Front Right Brake Caliper mesh")
    bpy.types.Scene.brake_caliper_FL = bpy.props.PointerProperty(type=bpy.types.Object, poll = object_search_poll, name= "Brake Caliper FL", description = "Front Left Brake Caliper mesh")
    bpy.types.Scene.speedometer_needle = bpy.props.PointerProperty(type=bpy.types.Object, poll = object_search_poll, name= "Speedometer Needle", description = "Speedometer Needle mesh")
    bpy.types.Scene.tachometer_needle = bpy.props.PointerProperty(type=bpy.types.Object, poll = object_search_poll, name= "Tachometer Needle", description = "Tachometer (RPM) Needle mesh")
    bpy.types.Scene.bone_length = bpy.props.FloatProperty(name = "Bone Length", description = "How long will be bones which will be added", default =  100, unit = 'LENGTH')
    bpy.types.Scene.bone_head_location = bpy.props.FloatVectorProperty(subtype = 'XYZ', unit = 'LENGTH')
    bpy.types.Scene.bone_tail_location = bpy.props.FloatVectorProperty(subtype = 'XYZ', unit = 'LENGTH')
    bpy.types.Scene.armature_for_new_bone = bpy.props.PointerProperty(type=bpy.types.Armature, description = "Armature to which new bone will be added",   
        name="Bone armature")
    bpy.types.Scene.armature_parent_bone_name = bpy.props.StringProperty(description = "Parent bone of new bone", name="Parent bone name")
    bpy.types.Scene.new_bone_name = bpy.props.StringProperty(description = "New bone name", name = "New bone name")
    bpy.types.Scene.set_vertext_groups_to_selected = bpy.props.BoolProperty(default = True, 
        description = "If checked will automatically assign selected vertices to new bone vertex group", name = "Auto Weight Selected")
    bpy.types.Scene.end_in_pose_mode = bpy.props.BoolProperty(default = False, 
        description = "After adding bone you will end up in pose mode to check bone weights", name = "End In Pose Mode")
    bpy.types.Scene.multiple_wheels = bpy.props.CollectionProperty(type = WheelItem)
    bpy.types.Scene.dynamic_wheel_count = bpy.props.BoolProperty(default = False, 
        description = "Allows to rig vehicles with more or less than 4 wheels", name = "N-Wheeled vehicle")

def unregister():
    bpy.utils.unregister_class(WheelItem)
    bpy.utils.unregister_class(Rig_OT_Operator)
    bpy.utils.unregister_class(Scale_Units_OT_Operator)
    bpy.utils.unregister_class(Upscale_Objects_OT_Operator)
    bpy.utils.unregister_class(Set_Bone_Head_Location_OT_Operator)
    bpy.utils.unregister_class(Set_Bone_Tail_Location_OT_Operator)
    bpy.utils.unregister_class(Add_Bone_To_Armature_OT_Operator)
    bpy.utils.unregister_class(Add_Another_Wheel_OT_Operator)
    bpy.utils.unregister_class(Remove_Chosen_Wheel_OT_Operator)
    bpy.utils.unregister_class(UI_PT_Rig_Panel)
    bpy.utils.unregister_class(UI_PT_Additional_Rigging_Panel)
    bpy.utils.unregister_class(UI_PT_Scene_Setup_Panel)
    del bpy.types.Scene.vehicle_base
    del bpy.types.Scene.wheel_FR
    del bpy.types.Scene.wheel_FL
    del bpy.types.Scene.wheel_RR
    del bpy.types.Scene.wheel_RL
    del bpy.types.Scene.brake_caliper_FR
    del bpy.types.Scene.brake_caliper_FL
    del bpy.types.Scene.speedometer_needle
    del bpy.types.Scene.tachometer_needle
    del bpy.types.Scene.bone_length
    del bpy.types.Scene.bone_head_location
    del bpy.types.Scene.bone_tail_location
    del bpy.types.Scene.armature_for_new_bone
    del bpy.types.Scene.armature_parent_bone_name
    del bpy.types.Scene.new_bone_name
    del bpy.types.Scene.set_vertext_groups_to_selected
    del bpy.types.Scene.end_in_pose_mode
    del bpy.types.Scene.multiple_wheels
    del bpy.types.Scene.dynamic_wheel_count
    



