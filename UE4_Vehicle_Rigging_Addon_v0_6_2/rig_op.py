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

import bpy, math
from mathutils import Vector, Matrix


def check_and_unlink_objects(object_array):
    for index, mesh in enumerate(object_array):
        for other_mesh in object_array[index+1:]:
            if mesh.data == other_mesh.data:
                other_mesh.data = mesh.data.copy()

def clear_old_armature_modifiers(mesh):
        for modifier in mesh.modifiers:
            if modifier.type == 'ARMATURE':
                mesh.modifiers.remove(modifier)

class Rig_OT_Operator(bpy.types.Operator):
    bl_idname = "view3d.rig_vehicle"
    bl_label = "Rig Vehicle"
    bl_description = "Rigs Vehicle for UE4"
    bl_options = {'REGISTER', 'UNDO'}

    def set_vertex_group(self, mesh, vertex_group):
        #Make a new list for all vertice indexes
        index_list = [0]*len(mesh.data.vertices)
        #Populate index list with vertice indexes
        mesh.data.vertices.foreach_get('index', index_list)   
        #Set mesh vertex group
        mesh.vertex_groups[vertex_group].add(index_list, 1, 'REPLACE')
        #Make all vertex group array
        all_vertex_groups = mesh.vertex_groups.keys()
        #Remove group which will not be removed
        all_vertex_groups.remove(vertex_group)
        #Remove unneeded vertex groups
        for group in all_vertex_groups:
            mesh.vertex_groups[group].add(index_list, 1, 'SUBTRACT')

    
    def add_child_bone(self, bone_name, parent_bone, wheel_mesh, armature_data, bone_length):
        #Create a new bone
        new_bone = armature_data.data.edit_bones.new(bone_name)
        #Set bone's parent
        new_bone.parent = parent_bone
        #Set bone's position and rotation to match mesh transform
        mesh_matrix = wheel_mesh.matrix_world
        new_bone.head = mesh_matrix.translation
        # Apply mesh rotation to bone tail direction
        tail_offset = mesh_matrix.to_3x3() @ Vector((0, bone_length, 0))
        new_bone.tail = mesh_matrix.translation + tail_offset
        return new_bone

    @classmethod
    def poll(cls, context):
        unit_length = bpy.context.scene.unit_settings.scale_length
        unit_system = bpy.context.scene.unit_settings.system
        return (((context.scene.vehicle_base is not None 
            and context.scene.wheel_FR is not None 
            and context.scene.wheel_FL is not None 
            and context.scene.wheel_RR is not None 
            and context.scene.wheel_RL is not None 
            and context.scene.dynamic_wheel_count is False) or (
            context.scene.vehicle_base is not None 
            and context.scene.dynamic_wheel_count is True and 
            all(item.wheel_mesh is not None for item in context.scene.multiple_wheels))) 
            and math.isclose(unit_length, 0.01, abs_tol=0.001)
            and unit_system == 'METRIC')

    def execute(self, context):
        scene = context.scene

        C = bpy.context 
        D = bpy.data
        O = bpy.ops

        #Set variables for vehicle base and wheel meshes
        vehicle_base = scene.vehicle_base
        wheel_RL = scene.wheel_RL
        wheel_RR = scene.wheel_RR
        wheel_FL = scene.wheel_FL
        wheel_FR = scene.wheel_FR
        
        #Set variables for brake calipers and dashboard instruments
        brake_caliper_FR = scene.brake_caliper_FR
        brake_caliper_FL = scene.brake_caliper_FL
        speedometer_needle = scene.speedometer_needle
        tachometer_needle = scene.tachometer_needle

        #Set vehicle base as active
        C.view_layer.objects.active = vehicle_base

        #Select all vehicle meshes
        vehicle_base.select_set(state=True)
        
        if scene.dynamic_wheel_count is True:
            for wheel_item in scene.multiple_wheels:
                wheel_item.wheel_mesh.select_set(state=True)
        else:
            wheel_RL.select_set(state=True)
            wheel_RR.select_set(state=True)
            wheel_FL.select_set(state=True)
            wheel_FR.select_set(state=True)

        #Select brake calipers if they exist
        if brake_caliper_FR is not None:
            brake_caliper_FR.select_set(state=True)
        if brake_caliper_FL is not None:
            brake_caliper_FL.select_set(state=True)
            
        #Select dashboard instruments if they exist
        if speedometer_needle is not None:
            speedometer_needle.select_set(state=True)
        if tachometer_needle is not None:
            tachometer_needle.select_set(state=True)

        #Set object mode
        O.object.mode_set(mode='OBJECT', toggle=True)

        #Set all object origins to geometry center
        O.object.origin_set(type='ORIGIN_GEOMETRY', center = 'BOUNDS')

        #making wheel mesh array
        wheel_mesh_array = []

        if scene.dynamic_wheel_count is True:
            wheel_mesh_array = [wheel_item.wheel_mesh for wheel_item in scene.multiple_wheels]
        else:
            wheel_mesh_array = [wheel_RL, wheel_FL, wheel_RR, wheel_FR]

        #making additional mesh array for brake calipers and instruments
        additional_mesh_array = []
        if brake_caliper_FR is not None:
            additional_mesh_array.append(brake_caliper_FR)
        if brake_caliper_FL is not None:
            additional_mesh_array.append(brake_caliper_FL)
        if speedometer_needle is not None:
            additional_mesh_array.append(speedometer_needle)
        if tachometer_needle is not None:
            additional_mesh_array.append(tachometer_needle)

        #checking for linked meshes and unlinking them
        check_and_unlink_objects(wheel_mesh_array + additional_mesh_array)
        
        #remove old armature modifiers from meshes
        clear_old_armature_modifiers(vehicle_base)
        for wheel in wheel_mesh_array:
            clear_old_armature_modifiers(wheel)
        for mesh in additional_mesh_array:
            clear_old_armature_modifiers(mesh)

        #get all armature type objects
        armature_objects = list(filter(lambda o: o.type == 'ARMATURE', D.objects))

        #remove armature if there's no armature object linked to it
        for armature in D.armatures[:]:
            if not any(x.data == armature for x in armature_objects):
                D.armatures.remove(armature)

        #Apply object transform
        O.object.transform_apply(location = False, rotation = True, scale = True)

        #Create armature object
        armature = D.armatures.new('Armature')
        armature_object = D.objects.new('Armature', armature)

        #Link armature object to our scene
        C.collection.objects.link(armature_object)

        #Make armature variable
        armature_data = D.objects[armature_object.name]

        #Set armature active
        C.view_layer.objects.active = armature_data

        #Set armature selceted
        armature_data.select_set(state=True)

        #Set edit mode
        O.object.mode_set(mode='EDIT', toggle=False)

        #Set bones In front and show axis
        armature_data.show_in_front = True
        armature_data.data.show_axes = True

        #Add root bone
        root_bone = armature_data.data.edit_bones.new('Root')
        #Set its orientation and size
        root_bone.head = (0,0,0)
        root_bone.tail = (0,scene.bone_length,0)
        #Set its location to vehicle base mesh
        root_bone.matrix = vehicle_base.matrix_world

        #Add wheel bones to armature
        if scene.dynamic_wheel_count is True:
            for wheel_item in scene.multiple_wheels:
                wheel_item.wheel_name = self.add_child_bone(wheel_item.wheel_name, root_bone, wheel_item.wheel_mesh, armature_data, scene.bone_length).name
        else:
            wheel_RL_bone = self.add_child_bone('RL', root_bone, wheel_RL, armature_data, scene.bone_length)
            wheel_RR_bone = self.add_child_bone('RR', root_bone, wheel_RR, armature_data, scene.bone_length)
            wheel_FL_bone = self.add_child_bone('FL', root_bone, wheel_FL, armature_data, scene.bone_length)
            wheel_FR_bone = self.add_child_bone('FR', root_bone, wheel_FR, armature_data, scene.bone_length)
                
        #Add brake caliper bones as children of root bone (not wheels)
        if brake_caliper_FR is not None:
            self.add_child_bone('Brake_Caliper_FR', root_bone, brake_caliper_FR, armature_data, scene.bone_length)
        if brake_caliper_FL is not None:
            self.add_child_bone('Brake_Caliper_FL', root_bone, brake_caliper_FL, armature_data, scene.bone_length)
                
        #Add dashboard instrument bones as children of root bone
        if speedometer_needle is not None:
            self.add_child_bone('Speedometer_Needle', root_bone, speedometer_needle, armature_data, scene.bone_length)
        if tachometer_needle is not None:
            self.add_child_bone('Tachometer_Needle', root_bone, tachometer_needle, armature_data, scene.bone_length)

        #Set object mode
        O.object.mode_set(mode='OBJECT', toggle=True)

        #Select vehicle meshes
        vehicle_base.select_set(state=True)

        if scene.dynamic_wheel_count is True:
            for wheel_item in scene.multiple_wheels:
                wheel_item.wheel_mesh.select_set(state=True)
        else:
            wheel_RL.select_set(state=True)
            wheel_RR.select_set(state=True)
            wheel_FL.select_set(state=True)
            wheel_FR.select_set(state=True)

        #Select additional meshes for parenting
        for mesh in additional_mesh_array:
            mesh.select_set(state=True)

        #Set armature active
        C.view_layer.objects.active = armature_data

        #Parent meshes to armature with empty groups
        O.object.parent_set(type='ARMATURE_NAME')

        #Set mesh vertex groups/weightpaint mesh
        self.set_vertex_group(vehicle_base, 'Root')

        if scene.dynamic_wheel_count is True:
            for wheel_item in scene.multiple_wheels:
                self.set_vertex_group(wheel_item.wheel_mesh, wheel_item.wheel_name)
        else:
            self.set_vertex_group(wheel_RL, 'RL')
            self.set_vertex_group(wheel_RR, 'RR')
            self.set_vertex_group(wheel_FL, 'FL')
            self.set_vertex_group(wheel_FR, 'FR')
            
            #Set vertex groups for brake calipers
            if brake_caliper_FR is not None:
                self.set_vertex_group(brake_caliper_FR, 'Brake_Caliper_FR')
            if brake_caliper_FL is not None:
                self.set_vertex_group(brake_caliper_FL, 'Brake_Caliper_FL')
                
        #Set vertex groups for dashboard instruments
        if speedometer_needle is not None:
            self.set_vertex_group(speedometer_needle, 'Speedometer_Needle')
        if tachometer_needle is not None:
            self.set_vertex_group(tachometer_needle, 'Tachometer_Needle')

        #Deselect all objects
        O.object.select_all(action='DESELECT')
        #Set pose mode
        O.object.mode_set(mode='POSE', toggle=True)

        return {'FINISHED'}


class Scale_Units_OT_Operator(bpy.types.Operator):
    bl_idname = "view3d.set_unit_scale"
    bl_label = "Set Unit Scale"
    bl_description = "Set Scene Unit Scale for UE4"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        unit_length = bpy.context.scene.unit_settings.scale_length
        return not math.isclose(unit_length, 0.01, abs_tol=0.001) or bpy.context.scene.unit_settings.system != 'METRIC'

    def execute(self, context):
        bpy.context.scene.unit_settings.system = 'METRIC'
        bpy.context.scene.unit_settings.scale_length = 0.01
        bpy.context.space_data.clip_end = 100000

        return {'FINISHED'}


class Upscale_Objects_OT_Operator(bpy.types.Operator):
    bl_idname = "view3d.upscale_objects"
    bl_label = "Rig Vehicle"
    bl_description = "Set Scene Unit Scale for UE4"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.object.mode_set(mode='OBJECT', toggle=True)

        bpy.ops.view3d.snap_cursor_to_center()
        bpy.ops.object.select_all(action='SELECT')

        bpy.context.scene.tool_settings.transform_pivot_point = 'CURSOR'

        bpy.ops.transform.resize(value=(100, 100, 100), orient_type='GLOBAL', 
            orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), 
            orient_matrix_type='GLOBAL', mirror=True, use_proportional_edit=False, 
            proportional_edit_falloff='SMOOTH', proportional_size=1, 
            use_proportional_connected=False, use_proportional_projected=False)

        check_and_unlink_objects(bpy.context.selected_objects)

        bpy.ops.object.transform_apply(location = False, rotation = True, scale = True)

        bpy.context.scene.tool_settings.transform_pivot_point = 'MEDIAN_POINT'
        
        return {'FINISHED'}

class Set_Bone_Head_Location_OT_Operator(bpy.types.Operator):
    bl_idname = "view3d.set_bone_head_location"
    bl_label = "Set Head Location"
    bl_description = "Set Bone Head Location"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        scene = context.scene
        #TODO check if selected mesh not armature
        if context.active_object.mode == 'EDIT':
            obj = bpy.context.edit_object
            obj.update_from_editmode()
            me = obj.data

            mat = obj.matrix_world

            verts_sel = [v.co for v in me.vertices if v.select]

            loc = mat @ (sum(verts_sel, Vector()) / len(verts_sel))
            scene.bone_head_location = loc
    
        return {'FINISHED'}


class Set_Bone_Tail_Location_OT_Operator(bpy.types.Operator):
    bl_idname = "view3d.set_bone_tail_location"
    bl_label = "Set Tail Location"
    bl_description = "Set Bone Tail Location"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = context.scene
        #TODO check if selected mesh not armature
        if context.active_object.mode == 'EDIT':
            obj = bpy.context.edit_object
            obj.update_from_editmode()
            me = obj.data

            mat = obj.matrix_world

            verts_sel = [v.co for v in me.vertices if v.select]

            loc = mat @ (sum(verts_sel, Vector()) / len(verts_sel))
            scene.bone_tail_location = loc
    
        return {'FINISHED'}


class Add_Bone_To_Armature_OT_Operator(bpy.types.Operator):
    bl_idname = "view3d.add_bone_to_armature"
    bl_label = "Add Bone To Armature"
    bl_description = "Add Bone To Selected Armature. Only usable in edit mode."
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        parent_name = context.scene.armature_parent_bone_name
        return len(parent_name) > 0 and context.object.mode == "EDIT" and context.object.type == "MESH"

    def execute(self, context):
        C = bpy.context 
        D = bpy.data
        O = bpy.ops
        scene = context.scene

        armature_data = scene.armature_for_new_bone
        parent_name = scene.armature_parent_bone_name
        
        arm_obj = next(filter(lambda o: o.type == 'ARMATURE' and o.data == armature_data, D.objects))

        selected_object = bpy.context.selected_objects[0]

        #Need to have object mode so selected vertices would get updated
        O.object.mode_set(mode='OBJECT', toggle=False)

        selected_vertice_indexes = [v.index for v in selected_object.data.vertices if v.select]

        C.view_layer.objects.active = arm_obj
        arm_obj.select_set(state=True)

        O.object.mode_set(mode='EDIT', toggle=False)

        parent_bone = armature_data.edit_bones[parent_name]

        new_bone_name = scene.new_bone_name

        new_bone = armature_data.edit_bones.new(new_bone_name)
        new_bone.head = scene.bone_head_location
        new_bone.tail = scene.bone_tail_location
        new_bone.parent = parent_bone
        selected_object.vertex_groups.new(name = new_bone.name)
        
        if scene.set_vertext_groups_to_selected:
            arm_obj.select_set(state=False)
            selected_object.select_set(state=True)
            C.view_layer.objects.active  = selected_object
            O.object.mode_set(mode='OBJECT', toggle = True)

            for group in selected_object.vertex_groups:
                selected_object.vertex_groups[group.name].add(selected_vertice_indexes, 1, 'SUBTRACT')

            selected_object.vertex_groups[new_bone.name].add(selected_vertice_indexes, 1, 'REPLACE')
            selected_object.select_set(state=False)

        if not scene.end_in_pose_mode:
            arm_obj.select_set(state=False)
            selected_object.select_set(state=True)
            #Need to go into armature mode so it would get visually updated. Tweek around, maybe can find better solution
            C.view_layer.objects.active = arm_obj
            O.object.mode_set(mode='POSE', toggle = True)

            C.view_layer.objects.active = selected_object
            O.object.mode_set(mode='EDIT', toggle = True)
        else:
            C.view_layer.objects.active = arm_obj
            O.object.mode_set(mode='POSE', toggle = True)

        return {'FINISHED'}


class Add_Another_Wheel_OT_Operator(bpy.types.Operator):
    bl_idname = "view3d.add_another_wheel"
    bl_label = "Add Another Wheel"
    bl_description = "Add Another Wheel Option"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        new = context.scene.multiple_wheels.add()
        new.wheel_name = "Wheel"

        return {'FINISHED'}


class Remove_Chosen_Wheel_OT_Operator(bpy.types.Operator):
    bl_idname = "view3d.remove_chosen_wheel"
    bl_label = "Removes Last Wheel"
    bl_description = "Removes Last Wheel Option"
    bl_options = {'REGISTER', 'UNDO'}

    id: bpy.props.IntProperty()

    def execute(self, context):
        # item = context.scene.multiple_wheels[len(context.scene.multiple_wheels)-1]
        context.scene.multiple_wheels.remove(self.id)

        return {'FINISHED'}
