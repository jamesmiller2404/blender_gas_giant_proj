

bl_info = {
    "name": "Gas Giant Shader Controls v10",
    "author": "ChatGPT for James Miller",
    "version": (10, 1, 0),
    "blender": (4, 0, 0),
    "location": "View3D > Sidebar > Gas Giant",
    "description": "Safer 6-layer gas giant shader controller with presets, atmosphere, and per-layer swirl-warp controls.",
    "category": "Material",
}

import bpy

CONTROLLER_NAME = "Gas Giant Shader Controls"
FRAME_NAME = "GG 6-Layer Cloud Rig"
ATM_FRAME_NAME = "GG Atmospheric Edge Rig"
SWIRL_FRAME_NAME = "GG Cloud Swirl Warp Rig"
PREVIEW_SPHERE_NAME = "Gas Giant Preview Sphere"
PREVIEW_MATERIAL_NAME = "Gas Giant Preview Material"

DEFAULT_PALETTE = [
    (1.00, 0.95, 0.70, 1.0),
    (1.00, 0.82, 0.38, 1.0),
    (0.72, 0.42, 0.20, 1.0),
    (0.95, 0.72, 0.48, 1.0),
    (0.50, 0.30, 0.17, 1.0),
    (0.92, 0.86, 0.68, 1.0),
]

PRESET_DATA = [
    ("saturn_gold_bands", "Saturn Gold Bands", [(0.97,0.94,0.78,1),(0.93,0.84,0.58,1),(0.84,0.69,0.42,1),(0.95,0.89,0.70,1),(0.71,0.57,0.34,1),(0.99,0.97,0.88,1)], 16, 7.5, .42, .42, [.18,.25,.38,.45,.52,.62], .50, .92, 1.02),
    ("jupiter_classic", "Jupiter Classic", [(0.94,0.90,0.76,1),(0.87,0.69,0.47,1),(0.76,0.45,0.27,1),(0.95,0.80,0.63,1),(0.58,0.31,0.18,1),(0.83,0.74,0.60,1)], 21, 9.5, .58, .62, [.25,.36,.44,.58,.66,.78], .50, 1.00, 1.00),
    ("jupiter_stormy_rust", "Jupiter Stormy Rust", [(0.96,0.89,0.77,1),(0.88,0.68,0.48,1),(0.72,0.38,0.19,1),(0.97,0.78,0.57,1),(0.47,0.20,0.10,1),(0.77,0.61,0.47,1)], 24, 10.5, .63, .68, [.24,.38,.50,.63,.74,.86], .50, 1.08, .98),
    ("jupiter_pale_belts", "Jupiter Pale Belts", [(0.99,0.96,0.90,1),(0.92,0.84,0.69,1),(0.78,0.62,0.45,1),(0.98,0.91,0.77,1),(0.60,0.43,0.29,1),(0.88,0.80,0.68,1)], 18.5, 8.3, .50, .48, [.18,.28,.36,.44,.52,.64], .50, .90, 1.04),
    ("neptune_deep_blue", "Neptune Deep Blue", [(0.80,0.93,1.00,1),(0.44,0.72,0.97,1),(0.18,0.41,0.80,1),(0.58,0.85,1.00,1),(0.07,0.19,0.52,1),(0.30,0.55,0.88,1)], 11, 6.4, .36, .26, [.10,.18,.22,.28,.36,.44], .50, 1.08, 1.00),
    ("uranus_cyan_haze", "Uranus Cyan Haze", [(0.88,1.00,0.98,1),(0.67,0.92,0.92,1),(0.42,0.76,0.83,1),(0.78,0.98,0.97,1),(0.28,0.59,0.68,1),(0.55,0.84,0.87,1)], 9, 5.8, .28, .18, [.08,.12,.16,.18,.22,.26], .50, .82, 1.05),
    ("cold_methane_bands", "Cold Methane Bands", [(0.83,0.97,1.00,1),(0.48,0.82,0.97,1),(0.19,0.52,0.84,1),(0.64,0.91,1.00,1),(0.09,0.27,0.56,1),(0.28,0.63,0.91,1)], 14, 7.1, .38, .35, [.12,.18,.24,.32,.40,.48], .50, 1.04, 1.00),
    ("ice_giant_teal", "Ice Giant Teal", [(0.87,0.99,0.98,1),(0.57,0.89,0.89,1),(0.22,0.63,0.67,1),(0.72,0.96,0.94,1),(0.10,0.38,0.44,1),(0.42,0.77,0.78,1)], 10.5, 6.1, .32, .24, [.10,.16,.20,.24,.30,.38], .50, .95, 1.03),
    ("hot_jupiter_charcoal", "Hot Jupiter Charcoal", [(0.80,0.74,0.67,1),(0.55,0.42,0.36,1),(0.25,0.19,0.18,1),(0.74,0.57,0.47,1),(0.10,0.08,0.08,1),(0.44,0.30,0.27,1)], 17.5, 10, .68, .72, [.20,.32,.48,.60,.72,.84], .50, .78, .86),
    ("hot_jupiter_copper", "Hot Jupiter Copper", [(0.98,0.82,0.58,1),(0.86,0.49,0.22,1),(0.56,0.23,0.08,1),(0.97,0.66,0.34,1),(0.32,0.12,0.04,1),(0.73,0.36,0.15,1)], 20, 10.8, .66, .74, [.22,.34,.50,.64,.78,.90], .50, 1.18, .95),
    ("ultra_hot_ember", "Ultra-Hot Ember", [(1.00,0.86,0.56,1),(1.00,0.47,0.13,1),(0.78,0.18,0.05,1),(1.00,0.66,0.25,1),(0.40,0.05,0.02,1),(0.93,0.30,0.07,1)], 23, 11.4, .72, .80, [.26,.40,.56,.70,.84,.96], .50, 1.25, 1.02),
    ("silicate_cloud_blue", "Silicate Cloud Blue", [(0.88,0.96,1.00,1),(0.46,0.70,0.96,1),(0.16,0.33,0.72,1),(0.70,0.86,1.00,1),(0.05,0.14,0.42,1),(0.30,0.50,0.86,1)], 15.5, 8.8, .52, .60, [.16,.26,.38,.52,.66,.80], .50, 1.10, .98),
    ("lava_twilight_giant", "Lava Twilight Giant", [(0.95,0.76,0.62,1),(0.73,0.38,0.30,1),(0.33,0.16,0.20,1),(0.56,0.29,0.53,1),(0.12,0.06,0.11,1),(0.81,0.50,0.72,1)], 18, 9.8, .64, .70, [.18,.30,.44,.58,.72,.86], .50, 1.06, .90),
    ("young_self_luminous", "Young Self-Luminous Giant", [(1.00,0.82,0.54,1),(0.95,0.55,0.25,1),(0.63,0.23,0.10,1),(0.99,0.70,0.40,1),(0.34,0.12,0.04,1),(0.79,0.36,0.14,1)], 19, 10.2, .61, .67, [.20,.32,.48,.62,.74,.88], .50, 1.15, 1.08),
    ("brown_dwarf_bands", "Brown Dwarf Bands", [(0.85,0.70,0.50,1),(0.63,0.40,0.24,1),(0.31,0.18,0.10,1),(0.78,0.55,0.34,1),(0.14,0.08,0.05,1),(0.49,0.29,0.16,1)], 17, 11, .75, .82, [.22,.36,.52,.68,.82,.94], .50, .95, .84),
    ("ammonia_storm_giant", "Ammonia Storm Giant", [(0.97,0.97,0.94,1),(0.89,0.84,0.70,1),(0.69,0.58,0.42,1),(0.96,0.91,0.82,1),(0.47,0.36,0.24,1),(0.83,0.78,0.66,1)], 20, 10.4, .60, .66, [.16,.24,.36,.50,.70,.92], .50, .88, 1.02),
    ("creamsicle_giant", "Creamsicle Gas Giant", [(1.00,0.97,0.90,1),(1.00,0.78,0.48,1),(0.93,0.48,0.22,1),(1.00,0.89,0.67,1),(0.67,0.30,0.10,1),(0.98,0.65,0.32,1)], 18.5, 9.2, .54, .58, [.18,.28,.42,.54,.66,.78], .50, 1.10, 1.02),
    ("violet_haze_giant", "Violet Haze Giant", [(0.96,0.91,1.00,1),(0.72,0.56,0.92,1),(0.41,0.26,0.68,1),(0.88,0.78,0.98,1),(0.22,0.12,0.40,1),(0.58,0.43,0.82,1)], 15, 8.7, .46, .54, [.14,.22,.34,.46,.58,.72], .50, 1.06, .96),
    ("desert_sand_giant", "Desert Sand Giant", [(0.98,0.93,0.76,1),(0.87,0.73,0.46,1),(0.66,0.47,0.24,1),(0.93,0.84,0.62,1),(0.42,0.28,0.12,1),(0.77,0.61,0.34,1)], 16.8, 8.6, .50, .52, [.16,.26,.38,.48,.60,.74], .50, .96, 1.00),
    ("pearl_cloud_giant", "Pearl Cloud Giant", [(1.00,0.99,0.98,1),(0.94,0.95,0.97,1),(0.77,0.81,0.88,1),(0.98,0.96,0.95,1),(0.58,0.63,0.72,1),(0.87,0.89,0.93,1)], 12, 7.2, .38, .30, [.12,.18,.24,.30,.36,.44], .50, .78, 1.06),
    ("hycean_tropical_teal", "Hycean Tropical Teal", [(0.86,1.00,0.97,1),(0.46,0.93,0.88,1),(0.11,0.63,0.63,1),(0.73,0.99,0.95,1),(0.04,0.32,0.39,1),(0.28,0.78,0.74,1)], 13.5, 7.8, .47, .48, [.14,.24,.34,.44,.56,.70], .50, 1.08, 1.04),
    ("hycean_deep_ocean", "Hycean Deep Ocean", [(0.80,0.95,1.00,1),(0.32,0.68,0.92,1),(0.05,0.29,0.66,1),(0.58,0.86,1.00,1),(0.01,0.10,0.34,1),(0.17,0.48,0.83,1)], 12, 8, .50, .56, [.16,.26,.38,.50,.64,.80], .50, 1.12, .98),
    ("hycean_whitecap", "Hycean Steamy Whitecap", [(1.00,1.00,1.00,1),(0.77,0.96,0.99,1),(0.34,0.78,0.90,1),(0.92,1.00,1.00,1),(0.10,0.46,0.67,1),(0.59,0.90,0.97,1)], 14.5, 8.4, .53, .60, [.18,.28,.40,.56,.72,.90], .50, .95, 1.10),
    ("hycean_storm_world", "Hycean Storm World", [(0.92,1.00,1.00,1),(0.48,0.85,0.94,1),(0.14,0.52,0.68,1),(0.76,0.98,0.98,1),(0.05,0.23,0.36,1),(0.29,0.67,0.80,1)], 17, 10.2, .67, .72, [.20,.32,.48,.62,.80,.96], .50, 1.02, .98),
    ("dark_hycean_twilight", "Dark Hycean Twilight", [(0.77,0.94,1.00,1),(0.25,0.60,0.84,1),(0.04,0.18,0.47,1),(0.57,0.80,0.96,1),(0.01,0.07,0.23,1),(0.12,0.39,0.68,1)], 15, 9.4, .61, .68, [.18,.30,.44,.58,.74,.90], .50, 1.06, .82),
]

PRESETS = {p[0]: p for p in PRESET_DATA}
PRESET_ENUM_ITEMS = [(p[0], p[1], p[1]) for p in PRESET_DATA]


def find_controller():
    obj = bpy.data.objects.get(CONTROLLER_NAME)
    if obj:
        return obj
    obj = bpy.data.objects.new(CONTROLLER_NAME, None)
    bpy.context.collection.objects.link(obj)
    obj.empty_display_type = 'SPHERE'
    obj.empty_display_size = 0.75
    return obj


def set_prop(obj, name, value, desc='', min_value=None, max_value=None, subtype=None):
    obj[name] = value
    try:
        ui = obj.id_properties_ui(name)
        kwargs = {'description': desc}
        if min_value is not None:
            kwargs['min'] = min_value; kwargs['soft_min'] = min_value
        if max_value is not None:
            kwargs['max'] = max_value; kwargs['soft_max'] = max_value
        if subtype:
            kwargs['subtype'] = subtype
        ui.update(**kwargs)
    except Exception:
        pass


def setup_controller(ctrl):
    for i, color in enumerate(DEFAULT_PALETTE, 1):
        if f'band_color_{i}' not in ctrl:
            set_prop(ctrl, f'band_color_{i}', list(color), f'Band/cloud color {i}', 0, 1, 'COLOR')
    defaults = {
        'cloud_scale': 18.0, 'cloud_complexity': 9.0, 'cloud_roughness': .56, 'cloud_contrast': .55,
        'cloud_opacity': 0.55,
        'hue_shift': .50, 'saturation': 1.0, 'brightness': 1.0,
        'atmosphere_strength': 0.45,
        'atmosphere_thickness': 0.38,
        'atmosphere_falloff': 0.70,
        'atmosphere_alpha': 0.85,
        'swirl_tightness': 0.18,
        'swirl_curvature': 0.25,
        'swirl_scale': 6.0,
        'swirl_offset': 0.0,
        'swirl_layer_variation': 0.35,
    }
    for i, value in enumerate([.22,.34,.48,.58,.68,.78], 1):
        defaults[f'layer_{i}_strength'] = value
    for k, v in defaults.items():
        if k not in ctrl:
            set_prop(ctrl, k, v, k.replace('_',' ').title(), 0.0, 2.0 if k in {'saturation','brightness'} else 1.0)
    # Per-layer swirl controls. These are initialized from the legacy global controls
    # so older scenes keep a familiar starting look, but each cloud layer can diverge.
    base_tightness = float(ctrl.get('swirl_tightness', defaults['swirl_tightness']))
    base_curvature = float(ctrl.get('swirl_curvature', defaults['swirl_curvature']))
    base_scale = float(ctrl.get('swirl_scale', defaults['swirl_scale']))
    base_offset = float(ctrl.get('swirl_offset', defaults['swirl_offset']))
    for i in range(1, 7):
        layer_defaults = {
            f'layer_{i}_swirl_tightness': max(0.0, base_tightness * (0.70 + i * 0.12)),
            f'layer_{i}_swirl_curvature': max(-1.0, min(1.0, base_curvature + (i - 3.5) * 0.07)),
            f'layer_{i}_swirl_scale': max(0.1, base_scale * (0.80 + i * 0.08)),
            f'layer_{i}_swirl_offset': base_offset + i * 0.11,
        }
        for k, v in layer_defaults.items():
            if k not in ctrl:
                set_prop(ctrl, k, v, k.replace('_',' ').title(), 0.0, 1.0)
    if 'atmosphere_color' not in ctrl:
        set_prop(ctrl, 'atmosphere_color', [0.45, 0.82, 1.0, 1.0], 'Atmospheric rim / limb glow color', 0, 1, 'COLOR')
    # Re-apply UI metadata for colors even if they already exist.
    for i in range(1, 7):
        try:
            ctrl.id_properties_ui(f'band_color_{i}').update(subtype='COLOR', min=0, max=1, soft_min=0, soft_max=1)
        except Exception:
            pass
    try:
        ctrl.id_properties_ui('atmosphere_color').update(subtype='COLOR', min=0, max=1, soft_min=0, soft_max=1)
    except Exception:
        pass
    # Cloud controls need ranges that match Blender shader node inputs and preset values.
    for prop_name, min_value, max_value, soft_max in [
        ('cloud_scale', 0.1, 250.0, 80.0),
        ('cloud_complexity', 0.0, 15.0, 15.0),
        ('cloud_roughness', 0.0, 1.0, 1.0),
        ('cloud_contrast', 0.0, 1.0, 1.0),
        ('cloud_opacity', 0.0, 1.0, 1.0),
    ]:
        try:
            ctrl.id_properties_ui(prop_name).update(min=min_value, max=max_value, soft_min=min_value, soft_max=soft_max)
        except Exception:
            pass
    for i in range(1, 7):
        try:
            ctrl.id_properties_ui(f'layer_{i}_strength').update(min=0.0, max=1.0, soft_min=0.0, soft_max=1.0)
        except Exception:
            pass
    # Atmosphere control ranges.
    for prop_name, max_value in [
        ('atmosphere_strength', 5.0),
        ('atmosphere_thickness', 1.0),
        ('atmosphere_falloff', 1.0),
        ('atmosphere_alpha', 1.0),
    ]:
        try:
            ctrl.id_properties_ui(prop_name).update(min=0.0, max=max_value, soft_min=0.0, soft_max=max_value)
        except Exception:
            pass

    # Swirl / coordinate warp ranges.
    for prop_name, min_value, max_value in [
        ('swirl_tightness', 0.0, 2.0),
        ('swirl_curvature', -1.0, 1.0),
        ('swirl_scale', 0.1, 50.0),
        ('swirl_offset', -10.0, 10.0),
        ('swirl_layer_variation', 0.0, 2.0),
    ]:
        try:
            ctrl.id_properties_ui(prop_name).update(min=min_value, max=max_value, soft_min=min_value, soft_max=max_value)
        except Exception:
            pass
    for i in range(1, 7):
        for prop_name, min_value, max_value in [
            (f'layer_{i}_swirl_tightness', 0.0, 2.0),
            (f'layer_{i}_swirl_curvature', -1.0, 1.0),
            (f'layer_{i}_swirl_scale', 0.1, 50.0),
            (f'layer_{i}_swirl_offset', -10.0, 10.0),
        ]:
            try:
                ctrl.id_properties_ui(prop_name).update(min=min_value, max=max_value, soft_min=min_value, soft_max=max_value)
            except Exception:
                pass


def material_score(mat):
    if not mat or not mat.use_nodes or not mat.node_tree:
        return -1
    score = 0
    for n in mat.node_tree.nodes:
        if n.type in {'TEX_NOISE','VALTORGB','MIX','MIX_RGB','BSDF_PRINCIPLED','HUE_SAT'}:
            score += 2
        if any(word in n.name.lower() for word in ['gas','giant','planet','noise','musgrave','ramp','hue','principled']):
            score += 1
    return score


def find_material(context):
    obj = context.object
    if obj and obj.active_material and material_score(obj.active_material) > 0:
        return obj.active_material
    if obj:
        mats = [s.material for s in obj.material_slots if s.material]
        mats.sort(key=material_score, reverse=True)
        if mats and material_score(mats[0]) > 0:
            return mats[0]
    mats = list(bpy.data.materials)
    mats.sort(key=material_score, reverse=True)
    return mats[0] if mats and material_score(mats[0]) > 0 else None


def create_preview_sphere(context):
    obj = bpy.data.objects.get(PREVIEW_SPHERE_NAME)
    if not obj:
        bpy.ops.mesh.primitive_uv_sphere_add(segments=128, ring_count=64, radius=2.0, location=(0, 0, 0))
        obj = context.object
        obj.name = PREVIEW_SPHERE_NAME
        try:
            bpy.ops.object.shade_smooth()
        except Exception:
            pass
    mat = bpy.data.materials.get(PREVIEW_MATERIAL_NAME)
    if not mat:
        mat = bpy.data.materials.new(PREVIEW_MATERIAL_NAME)
        mat.use_nodes = True
    if not obj.data.materials:
        obj.data.materials.append(mat)
    else:
        obj.data.materials[0] = mat
    obj.active_material = mat
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    context.view_layer.objects.active = obj
    return obj, mat


def socket_by_names(sockets, names, fallback_index=None):
    for name in names:
        if name in sockets:
            return sockets[name]
    if fallback_index is not None and len(sockets) > fallback_index:
        return sockets[fallback_index]
    return None


def remove_driver(idblock, data_path, index=-1):
    if not idblock.animation_data:
        return
    for fc in list(idblock.animation_data.drivers):
        if fc.data_path == data_path and (index == -1 or fc.array_index == index):
            try:
                idblock.driver_remove(data_path, fc.array_index)
            except Exception:
                pass


def drive_prop(idblock, data_path, ctrl, prop, expr='var'):
    remove_driver(idblock, data_path, -1)
    fc = idblock.driver_add(data_path)
    fc.driver.type = 'SCRIPTED'
    fc.driver.expression = expr
    var = fc.driver.variables.new()
    var.name = 'var'
    var.targets[0].id_type = 'OBJECT'
    var.targets[0].id = ctrl
    var.targets[0].data_path = f'["{prop}"]'



def drive_prop_index(idblock, data_path, index, ctrl, prop, expr='var'):
    remove_driver(idblock, data_path, index)
    fc = idblock.driver_add(data_path, index)
    fc.driver.type = 'SCRIPTED'
    fc.driver.expression = expr
    var = fc.driver.variables.new()
    var.name = 'var'
    var.targets[0].id_type = 'OBJECT'
    var.targets[0].id = ctrl
    var.targets[0].data_path = f'["{prop}"]'


def drive_color_component(idblock, data_path, index, ctrl, prop, component):
    remove_driver(idblock, data_path, index)
    fc = idblock.driver_add(data_path, index)
    fc.driver.type = 'SCRIPTED'
    fc.driver.expression = 'c'
    var = fc.driver.variables.new()
    var.name = 'c'
    var.targets[0].id_type = 'OBJECT'
    var.targets[0].id = ctrl
    var.targets[0].data_path = f'["{prop}"][{component}]'


def clear_input(nt, input_socket):
    for link in list(nt.links):
        if link.to_socket == input_socket:
            nt.links.remove(link)


def link(nt, a, b):
    if a is None or b is None:
        return
    try:
        nt.links.new(a, b)
    except Exception:
        pass


def get_or_new(nt, node_type, name, loc):
    old = nt.nodes.get(name)
    if old and old.bl_idname == node_type:
        old.location = loc
        return old
    if old:
        nt.nodes.remove(old)
    node = nt.nodes.new(node_type)
    node.name = name
    node.label = name
    node.location = loc
    return node


def new_mix_node(nt, name, loc):
    old = nt.nodes.get(name)
    if old:
        nt.nodes.remove(old)
    try:
        node = nt.nodes.new('ShaderNodeMixRGB')
        node.blend_type = 'MIX'
        node.use_clamp = True
    except Exception:
        node = nt.nodes.new('ShaderNodeMix')
        try:
            node.data_type = 'RGBA'
            node.factor_mode = 'UNIFORM'
        except Exception:
            pass
    node.name = name
    node.label = name
    node.location = loc
    return node


def mix_sockets(node):
    fac = socket_by_names(node.inputs, ['Fac','Factor'], 0)
    a = socket_by_names(node.inputs, ['Color1','A'], 1)
    b = socket_by_names(node.inputs, ['Color2','B'], 2)
    out = socket_by_names(node.outputs, ['Color','Result'], 0)
    return fac, a, b, out


def make_rgb_node(nt, name, loc, ctrl, color_prop):
    node = get_or_new(nt, 'ShaderNodeRGB', name, loc)
    path = f'nodes["{node.name}"].outputs[0].default_value'
    for c in range(4):
        drive_color_component(nt, path, c, ctrl, color_prop, c)
    return node


def build_rig(context):
    ctrl = find_controller()
    setup_controller(ctrl)
    mat = find_material(context)
    if not mat:
        raise RuntimeError('No likely node material found. Select the planet object first.')
    nt = mat.node_tree
    nodes = nt.nodes

    principled = None
    for n in nodes:
        if n.type == 'BSDF_PRINCIPLED':
            principled = n
            break
    if not principled:
        raise RuntimeError('No Principled BSDF node found in the material.')

    base_input = socket_by_names(principled.inputs, ['Base Color'], None)
    if not base_input:
        raise RuntimeError('Could not find Principled BSDF Base Color input.')

    original_from = None
    if base_input.is_linked:
        old_link = base_input.links[0]
        if not old_link.from_node.name.startswith('GG '):
            original_from = old_link.from_socket

    frame = nodes.get(FRAME_NAME)
    if not frame:
        frame = nodes.new('NodeFrame')
        frame.name = FRAME_NAME
        frame.label = FRAME_NAME
    frame.location = (-1500, 400)

    base_rgb = make_rgb_node(nt, 'GG Fallback Base Color', (-1500, 100), ctrl, 'band_color_6')
    previous = original_from if original_from else base_rgb.outputs[0]

    scale_mults = [.35,.60,.95,1.40,2.10,3.10]
    for i in range(1, 7):
        y = 600 - i * 220
        noise = get_or_new(nt, 'ShaderNodeTexNoise', f'GG Noise {i}', (-1400, y))
        bands = get_or_new(nt, 'ShaderNodeTexWave', f'GG Latitude Bands {i}', (-1400, y - 115))
        band_mix = get_or_new(nt, 'ShaderNodeMath', f'GG Band Noise Mask {i}', (-1160, y))
        ramp = get_or_new(nt, 'ShaderNodeValToRGB', f'GG Mask Ramp {i}', (-960, y))
        math = get_or_new(nt, 'ShaderNodeMath', f'GG Strength {i}', (-900, y))
        opacity_math = get_or_new(nt, 'ShaderNodeMath', f'GG Cloud Opacity {i}', (-760, y))
        color = make_rgb_node(nt, f'GG Layer Color {i}', (-900, y-120), ctrl, f'band_color_{i}')
        mix = new_mix_node(nt, f'GG Layer Mix {i}', (-620 + (i-1)*190, 100))
        for node in [noise, bands, band_mix, ramp, math, opacity_math, color, mix]:
            node.parent = frame

        math.operation = 'MULTIPLY'
        band_mix.operation = 'MULTIPLY'
        opacity_math.operation = 'MULTIPLY'
        try:
            bands.bands_direction = 'Z'
        except Exception:
            pass
        if 'Scale' in noise.inputs:
            drive_prop(nt, f'nodes["{noise.name}"].inputs["Scale"].default_value', ctrl, 'cloud_scale', f'var*{scale_mults[i-1]}')
        if 'Detail' in noise.inputs:
            drive_prop(nt, f'nodes["{noise.name}"].inputs["Detail"].default_value', ctrl, 'cloud_complexity', 'var')
        if 'Roughness' in noise.inputs:
            drive_prop(nt, f'nodes["{noise.name}"].inputs["Roughness"].default_value', ctrl, 'cloud_roughness', 'var')
        if 'Scale' in bands.inputs:
            drive_prop(nt, f'nodes["{bands.name}"].inputs["Scale"].default_value', ctrl, 'cloud_scale', f'var*{0.55 + i * 0.11}')
        if 'Distortion' in bands.inputs:
            drive_prop(nt, f'nodes["{bands.name}"].inputs["Distortion"].default_value', ctrl, f'layer_{i}_swirl_tightness', 'var*8.0')

        while len(ramp.color_ramp.elements) < 2:
            ramp.color_ramp.elements.new(1.0)
        while len(ramp.color_ramp.elements) > 2:
            ramp.color_ramp.elements.remove(ramp.color_ramp.elements[-1])
        ramp.color_ramp.elements[0].color = (0,0,0,1)
        ramp.color_ramp.elements[1].color = (1,1,1,1)
        # Simple expressions supported by Blender drivers.
        drive_prop(nt, f'nodes["{ramp.name}"].color_ramp.elements[0].position', ctrl, 'cloud_contrast', '0.10+var*0.35')
        drive_prop(nt, f'nodes["{ramp.name}"].color_ramp.elements[1].position', ctrl, 'cloud_contrast', '0.90-var*0.35')
        drive_prop(nt, f'nodes["{math.name}"].inputs[1].default_value', ctrl, f'layer_{i}_strength', 'var')
        drive_prop(nt, f'nodes["{opacity_math.name}"].inputs[1].default_value', ctrl, 'cloud_opacity', 'var')

        clear_input(nt, band_mix.inputs[0])
        link(nt, socket_by_names(bands.outputs, ['Fac','Color'], 0), band_mix.inputs[0])
        clear_input(nt, band_mix.inputs[1])
        link(nt, noise.outputs[0], band_mix.inputs[1])
        clear_input(nt, ramp.inputs[0])
        link(nt, band_mix.outputs[0], ramp.inputs[0])
        clear_input(nt, math.inputs[0])
        link(nt, ramp.outputs[0], math.inputs[0])
        clear_input(nt, opacity_math.inputs[0])
        link(nt, math.outputs[0], opacity_math.inputs[0])

        fac, a, b, out = mix_sockets(mix)
        clear_input(nt, fac); clear_input(nt, a); clear_input(nt, b)
        link(nt, opacity_math.outputs[0], fac)
        link(nt, previous, a)
        link(nt, color.outputs[0], b)
        previous = out

    hue = get_or_new(nt, 'ShaderNodeHueSaturation', 'GG Hue Saturation Value', (650, 100))
    hue.parent = frame
    hue_socket = socket_by_names(hue.inputs, ['Hue'], None)
    sat_socket = socket_by_names(hue.inputs, ['Saturation'], None)
    val_socket = socket_by_names(hue.inputs, ['Value'], None)
    color_socket = socket_by_names(hue.inputs, ['Color'], len(hue.inputs)-1)
    color_output = socket_by_names(hue.outputs, ['Color'], 0)
    if hue_socket: drive_prop(nt, f'nodes["{hue.name}"].inputs["{hue_socket.name}"].default_value', ctrl, 'hue_shift', 'var')
    if sat_socket: drive_prop(nt, f'nodes["{hue.name}"].inputs["{sat_socket.name}"].default_value', ctrl, 'saturation', 'var')
    if val_socket: drive_prop(nt, f'nodes["{hue.name}"].inputs["{val_socket.name}"].default_value', ctrl, 'brightness', 'var')
    clear_input(nt, color_socket)
    link(nt, previous, color_socket)

    clear_input(nt, base_input)
    link(nt, color_output, base_input)

    mat['gas_giant_controller'] = ctrl.name
    mat['gas_giant_v3_note'] = 'Built by Gas Giant Shader Controls v3. Six added cloud layers are driven by controller properties.'
    return mat.name


def apply_preset(ctrl, key):
    setup_controller(ctrl)
    p = PRESETS[key]
    _, _, colors, scale, detail, rough, contrast, layers, hue, sat, bright = p
    for i, c in enumerate(colors, 1):
        ctrl[f'band_color_{i}'] = list(c)
    ctrl['cloud_scale'] = scale
    ctrl['cloud_complexity'] = detail
    ctrl['cloud_roughness'] = rough
    ctrl['cloud_contrast'] = contrast
    for i, val in enumerate(layers, 1):
        ctrl[f'layer_{i}_strength'] = val
    ctrl['hue_shift'] = hue
    ctrl['saturation'] = sat
    ctrl['brightness'] = bright




def find_material_output(nt):
    for n in nt.nodes:
        if n.type == 'OUTPUT_MATERIAL':
            return n
    node = nt.nodes.new('ShaderNodeOutputMaterial')
    node.name = 'Material Output'
    node.location = (900, 0)
    return node


def shader_output_socket(node):
    if not node:
        return None
    return socket_by_names(node.outputs, ['BSDF', 'Shader'], 0)


def build_atmosphere(context):
    """Add/repair a clearly visible camera-facing atmospheric edge/rim glow.

    v5 uses Layer Weight / Facing because Facing is predictable:
    - Facing = 1.0 at the center of the visible disk
    - Facing = 0.0 near the limb/edge

    The rim mask is therefore WHITE near low Facing values and BLACK toward the center.
    This mask drives an Emission shader that is added to the existing material surface.
    """
    ctrl = find_controller()
    setup_controller(ctrl)
    mat = find_material(context)
    if not mat:
        raise RuntimeError('No likely node material found. Select the planet object first.')
    nt = mat.node_tree
    nodes = nt.nodes

    output = find_material_output(nt)
    surface_input = socket_by_names(output.inputs, ['Surface'], 0)
    if not surface_input:
        raise RuntimeError('Could not find Material Output Surface input.')

    # Preserve the original shader. If v4/v5 atmosphere already exists, unwrap it and reuse
    # the original shader plugged into the first Add Shader input. This prevents nested add nodes.
    original_shader = None
    if surface_input.is_linked:
        current_from = surface_input.links[0].from_socket
        current_node = surface_input.links[0].from_node
        if current_node.name in {'GG Atmosphere Add Shader', 'GG Visible Atmosphere Add'}:
            first_shader_input = socket_by_names(current_node.inputs, ['Shader'], 0)
            if first_shader_input and first_shader_input.is_linked:
                original_shader = first_shader_input.links[0].from_socket
        else:
            original_shader = current_from

    if original_shader is None:
        for n in nodes:
            if n.type == 'BSDF_PRINCIPLED':
                original_shader = shader_output_socket(n)
                break
    if original_shader is None:
        raise RuntimeError('Could not find an existing shader output to combine with the atmosphere.')

    frame = nodes.get(ATM_FRAME_NAME)
    if not frame:
        frame = nodes.new('NodeFrame')
        frame.name = ATM_FRAME_NAME
        frame.label = ATM_FRAME_NAME
    frame.location = (250, -700)

    layer = get_or_new(nt, 'ShaderNodeLayerWeight', 'GG Atmosphere Layer Weight', (250, -520))
    ramp = get_or_new(nt, 'ShaderNodeValToRGB', 'GG Visible Atmosphere Rim Ramp', (500, -520))
    strength_math = get_or_new(nt, 'ShaderNodeMath', 'GG Atmosphere Strength Multiply', (760, -520))
    alpha_math = get_or_new(nt, 'ShaderNodeMath', 'GG Atmosphere Alpha Multiply', (980, -520))
    color = make_rgb_node(nt, 'GG Atmosphere Color', (760, -700), ctrl, 'atmosphere_color')
    emission = get_or_new(nt, 'ShaderNodeEmission', 'GG Visible Atmosphere Emission', (1200, -570))
    add = get_or_new(nt, 'ShaderNodeAddShader', 'GG Visible Atmosphere Add', (1450, -300))

    for node in [layer, ramp, strength_math, alpha_math, color, emission, add]:
        node.parent = frame

    strength_math.operation = 'MULTIPLY'
    alpha_math.operation = 'MULTIPLY'

    # Layer Weight Blend adjusts how quickly the facing value falls toward the edge.
    blend_socket = socket_by_names(layer.inputs, ['Blend'], 0)
    if blend_socket:
        drive_prop(nt, f'nodes["{layer.name}"].inputs["{blend_socket.name}"].default_value', ctrl, 'atmosphere_falloff', 'var')

    # Use Facing, not Fresnel. Facing is easier to understand and makes the control work visibly.
    facing_out = socket_by_names(layer.outputs, ['Facing'], 0)
    if not facing_out:
        facing_out = socket_by_names(layer.outputs, ['Fresnel'], 1)
    if not facing_out:
        raise RuntimeError('Layer Weight node has no Facing/Fresnel output.')

    # Rim mask: white at low Facing values / edge, black toward the center.
    while len(ramp.color_ramp.elements) < 2:
        ramp.color_ramp.elements.new(1.0)
    while len(ramp.color_ramp.elements) > 2:
        ramp.color_ramp.elements.remove(ramp.color_ramp.elements[-1])
    ramp.color_ramp.interpolation = 'EASE'
    ramp.color_ramp.elements[0].position = 0.0
    ramp.color_ramp.elements[0].color = (1, 1, 1, 1)
    ramp.color_ramp.elements[1].position = 0.45
    ramp.color_ramp.elements[1].color = (0, 0, 0, 1)

    # Thickness moves the fade-to-black point. Higher thickness = glow reaches farther inward.
    # Keep it away from 0 and 1 so the ramp never collapses.
    drive_prop(nt, f'nodes["{ramp.name}"].color_ramp.elements[1].position', ctrl, 'atmosphere_thickness', '0.04+var*0.86')

    # User strength and alpha multiply together, then feed emission strength.
    drive_prop(nt, f'nodes["{strength_math.name}"].inputs[1].default_value', ctrl, 'atmosphere_strength', 'var')
    drive_prop(nt, f'nodes["{alpha_math.name}"].inputs[1].default_value', ctrl, 'atmosphere_alpha', 'var')

    clear_input(nt, ramp.inputs[0]); link(nt, facing_out, ramp.inputs[0])
    clear_input(nt, strength_math.inputs[0]); link(nt, ramp.outputs[0], strength_math.inputs[0])
    clear_input(nt, alpha_math.inputs[0]); link(nt, strength_math.outputs[0], alpha_math.inputs[0])

    color_in = socket_by_names(emission.inputs, ['Color'], 0)
    strength_in = socket_by_names(emission.inputs, ['Strength'], 1)
    clear_input(nt, color_in); link(nt, color.outputs[0], color_in)
    clear_input(nt, strength_in); link(nt, alpha_math.outputs[0], strength_in)

    add_a = socket_by_names(add.inputs, ['Shader'], 0)
    add_b = add.inputs[1] if len(add.inputs) > 1 else None
    clear_input(nt, add_a); clear_input(nt, add_b)
    link(nt, original_shader, add_a)
    link(nt, shader_output_socket(emission), add_b)
    clear_input(nt, surface_input)
    link(nt, shader_output_socket(add), surface_input)

    mat['gas_giant_atmosphere_note'] = 'Visible atmospheric edge/rim glow added by Gas Giant Shader Controls v6.'
    return mat.name


def apply_test_atmosphere(ctrl):
    """Set exaggerated atmosphere values so the user can confirm the rig is connected."""
    setup_controller(ctrl)
    ctrl['atmosphere_color'] = [0.25, 0.75, 1.0, 1.0]
    ctrl['atmosphere_strength'] = 3.0
    ctrl['atmosphere_thickness'] = 0.75
    ctrl['atmosphere_falloff'] = 0.25
    ctrl['atmosphere_alpha'] = 1.0




def set_vector_default(socket, values):
    if not socket:
        return
    try:
        for i, value in enumerate(values):
            socket.default_value[i] = value
    except Exception:
        pass


def build_swirl_warp(context):
    """Add/repair coordinate-warp node rigs that feed the six GG Noise nodes.

    This does not create true fluid simulation vortices. It creates procedural coordinate
    distortion before the cloud noise layers, which is the shader-node equivalent of
    tightening/curving cloud swirls.

    Controls:
    - layer_N_swirl_tightness: how strongly turbulence bends that layer
    - layer_N_swirl_curvature: rotates that layer's coordinate field around Z
    - layer_N_swirl_scale: size/frequency of that layer's turbulence field
    - layer_N_swirl_offset: slides that layer's warp field; can be keyframed
    """
    ctrl = find_controller()
    setup_controller(ctrl)
    mat = find_material(context)
    if not mat:
        raise RuntimeError('No likely node material found. Select the planet object first.')
    nt = mat.node_tree
    nodes = nt.nodes

    # If the six-layer cloud rig does not exist yet, build it first so there are targets.
    if not nodes.get('GG Noise 1'):
        build_rig(context)
        nt = mat.node_tree
        nodes = nt.nodes

    frame = nodes.get(SWIRL_FRAME_NAME)
    if not frame:
        frame = nodes.new('NodeFrame')
        frame.name = SWIRL_FRAME_NAME
        frame.label = SWIRL_FRAME_NAME
    frame.location = (-1900, 980)

    texcoord = get_or_new(nt, 'ShaderNodeTexCoord', 'GG Swirl Texture Coordinates', (-1900, 920))
    texcoord.parent = frame
    base_vector = socket_by_names(texcoord.outputs, ['Generated','Object'], 0)

    # Feed each cloud layer from its own mapping/noise/tightness chain. The old shared
    # nodes may remain in older files, but this builder rewires the cloud noise inputs
    # to the independent layer outputs below.
    wired = 0
    for i in range(1, 7):
        noise = nodes.get(f'GG Noise {i}')
        bands = nodes.get(f'GG Latitude Bands {i}')
        if not noise or 'Vector' not in noise.inputs:
            continue

        y = 980 - i * 150
        mapping = get_or_new(nt, 'ShaderNodeMapping', f'GG Swirl Layer Mapping {i}', (-1660, y))
        warp_noise = get_or_new(nt, 'ShaderNodeTexNoise', f'GG Swirl Layer Warp Noise {i}', (-1420, y))
        center = get_or_new(nt, 'ShaderNodeVectorMath', f'GG Swirl Layer Center Noise {i}', (-1180, y))
        tight_scale = get_or_new(nt, 'ShaderNodeVectorMath', f'GG Swirl Layer Tightness Scale {i}', (-940, y))
        add = get_or_new(nt, 'ShaderNodeVectorMath', f'GG Swirl Layer Add Warp {i}', (-700, y))

        for node in [mapping, warp_noise, center, tight_scale, add]:
            node.parent = frame
        try:
            center.operation = 'SUBTRACT'
        except Exception:
            pass
        try:
            tight_scale.operation = 'SCALE'
        except Exception:
            pass
        try:
            add.operation = 'ADD'
        except Exception:
            pass

        loc_socket = socket_by_names(mapping.inputs, ['Location'], 1)
        rot_socket = socket_by_names(mapping.inputs, ['Rotation'], 2)
        scale_socket = socket_by_names(mapping.inputs, ['Scale'], 3)
        if loc_socket:
            drive_prop_index(nt, f'nodes["{mapping.name}"].inputs["{loc_socket.name}"].default_value', 0, ctrl, f'layer_{i}_swirl_offset', 'var')
            drive_prop_index(nt, f'nodes["{mapping.name}"].inputs["{loc_socket.name}"].default_value', 1, ctrl, f'layer_{i}_swirl_offset', 'var*0.37')
        if rot_socket:
            drive_prop_index(nt, f'nodes["{mapping.name}"].inputs["{rot_socket.name}"].default_value', 2, ctrl, f'layer_{i}_swirl_curvature', 'var*6.283185')
        if scale_socket:
            for axis in range(3):
                drive_prop_index(nt, f'nodes["{mapping.name}"].inputs["{scale_socket.name}"].default_value', axis, ctrl, f'layer_{i}_swirl_scale', 'var')

        if 'Scale' in warp_noise.inputs:
            drive_prop(nt, f'nodes["{warp_noise.name}"].inputs["Scale"].default_value', ctrl, f'layer_{i}_swirl_scale', 'var')
        if 'Detail' in warp_noise.inputs:
            drive_prop(nt, f'nodes["{warp_noise.name}"].inputs["Detail"].default_value', ctrl, 'cloud_complexity', 'var')
        if 'Roughness' in warp_noise.inputs:
            drive_prop(nt, f'nodes["{warp_noise.name}"].inputs["Roughness"].default_value', ctrl, 'cloud_roughness', 'var')

        if len(center.inputs) > 1:
            set_vector_default(center.inputs[1], (0.5, 0.5, 0.5))
        tight_socket = socket_by_names(tight_scale.inputs, ['Scale'], 3 if len(tight_scale.inputs) > 3 else None)
        if tight_socket:
            drive_prop(nt, f'nodes["{tight_scale.name}"].inputs["{tight_socket.name}"].default_value', ctrl, f'layer_{i}_swirl_tightness', 'var')

        clear_input(nt, mapping.inputs[0]); link(nt, base_vector, mapping.inputs[0])
        if 'Vector' in warp_noise.inputs:
            clear_input(nt, warp_noise.inputs['Vector']); link(nt, mapping.outputs[0], warp_noise.inputs['Vector'])
        clear_input(nt, center.inputs[0]); link(nt, socket_by_names(warp_noise.outputs, ['Color','Fac'], 1), center.inputs[0])
        clear_input(nt, tight_scale.inputs[0]); link(nt, center.outputs[0], tight_scale.inputs[0])
        clear_input(nt, add.inputs[0]); link(nt, mapping.outputs[0], add.inputs[0])
        clear_input(nt, add.inputs[1]); link(nt, tight_scale.outputs[0], add.inputs[1])
        clear_input(nt, noise.inputs['Vector']); link(nt, add.outputs[0], noise.inputs['Vector'])
        if bands and 'Vector' in bands.inputs:
            clear_input(nt, bands.inputs['Vector']); link(nt, add.outputs[0], bands.inputs['Vector'])
        wired += 1

    mat['gas_giant_swirl_note'] = f'Independent per-layer swirl warp node rig added by Gas Giant Shader Controls v10; wired {wired} cloud noise nodes.'
    return mat.name, wired


def apply_test_swirl(ctrl):
    setup_controller(ctrl)
    ctrl['swirl_tightness'] = 0.85
    ctrl['swirl_curvature'] = 0.65
    ctrl['swirl_scale'] = 8.0
    ctrl['swirl_offset'] = 0.0
    ctrl['swirl_layer_variation'] = 0.85
    layer_values = [
        (0.45, -0.35, 5.5, 0.00),
        (0.70, 0.55, 7.0, 0.35),
        (1.05, -0.80, 9.0, 0.70),
        (0.85, 0.90, 11.0, 1.05),
        (1.30, -0.55, 13.5, 1.40),
        (0.60, 0.35, 16.0, 1.75),
    ]
    for i, (tightness, curvature, scale, offset) in enumerate(layer_values, 1):
        ctrl[f'layer_{i}_swirl_tightness'] = tightness
        ctrl[f'layer_{i}_swirl_curvature'] = curvature
        ctrl[f'layer_{i}_swirl_scale'] = scale
        ctrl[f'layer_{i}_swirl_offset'] = offset


class GASGIANT_OT_diagnostics(bpy.types.Operator):
    bl_idname = 'gasgiant.diagnostics_v3'
    bl_label = 'Diagnostics'
    bl_options = {'REGISTER'}
    def execute(self, context):
        mat = find_material(context)
        obj = context.object
        msg = f'Object: {obj.name if obj else "None"}; Material: {mat.name if mat else "None"}'
        self.report({'INFO'}, msg)
        print('Gas Giant v3 diagnostics:', msg)
        return {'FINISHED'}


class GASGIANT_OT_build(bpy.types.Operator):
    bl_idname = 'gasgiant.build_v3'
    bl_label = 'Build / Repair 6-Layer Rig'
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        try:
            mat_name = build_rig(context)
        except Exception as e:
            self.report({'ERROR'}, str(e))
            print('Gas Giant v3 error:', repr(e))
            return {'CANCELLED'}
        self.report({'INFO'}, f'Built 6-layer rig on material: {mat_name}')
        return {'FINISHED'}


class GASGIANT_OT_create_preview_sphere(bpy.types.Operator):
    bl_idname = 'gasgiant.create_preview_sphere_v10'
    bl_label = 'Create Visible Preview Sphere'
    bl_description = 'Create/select a mesh sphere with a proper material and build the gas giant shader on it'
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        try:
            obj, mat = create_preview_sphere(context)
            build_rig(context)
            build_atmosphere(context)
            build_swirl_warp(context)
        except Exception as e:
            self.report({'ERROR'}, str(e))
            print('Gas Giant v10 preview sphere error:', repr(e))
            return {'CANCELLED'}
        self.report({'INFO'}, f'Created visible preview sphere: {obj.name}; material: {mat.name}')
        return {'FINISHED'}




class GASGIANT_OT_build_atmosphere(bpy.types.Operator):
    bl_idname = 'gasgiant.build_atmosphere_v5'
    bl_label = 'Build / Repair Atmosphere Edge'
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        try:
            mat_name = build_atmosphere(context)
        except Exception as e:
            self.report({'ERROR'}, str(e))
            print('Gas Giant v5 atmosphere error:', repr(e))
            return {'CANCELLED'}
        self.report({'INFO'}, f'Built atmosphere edge rig on material: {mat_name}')
        return {'FINISHED'}


class GASGIANT_OT_test_atmosphere(bpy.types.Operator):
    bl_idname = 'gasgiant.test_atmosphere_v5'
    bl_label = 'Make Atmosphere Obvious'
    bl_description = 'Set exaggerated atmosphere values so you can confirm the rim rig is working'
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        ctrl = find_controller()
        apply_test_atmosphere(ctrl)
        self.report({'INFO'}, 'Atmosphere test values applied: bright cyan, strong, thick rim.')
        return {'FINISHED'}


class GASGIANT_OT_build_swirl(bpy.types.Operator):
    bl_idname = 'gasgiant.build_swirl_v6'
    bl_label = 'Build / Repair Swirl Warp'
    bl_description = 'Wire independent coordinate-warp nodes into each cloud noise layer'
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        try:
            mat_name, wired = build_swirl_warp(context)
        except Exception as e:
            self.report({'ERROR'}, str(e))
            print('Gas Giant v6 swirl error:', repr(e))
            return {'CANCELLED'}
        self.report({'INFO'}, f'Built swirl warp on {mat_name}; wired {wired} cloud noise nodes.')
        return {'FINISHED'}


class GASGIANT_OT_test_swirl(bpy.types.Operator):
    bl_idname = 'gasgiant.test_swirl_v6'
    bl_label = 'Make Swirl Obvious'
    bl_description = 'Set exaggerated swirl values so the warp effect is easy to confirm'
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        ctrl = find_controller()
        apply_test_swirl(ctrl)
        try:
            build_swirl_warp(context)
        except Exception as e:
            self.report({'ERROR'}, str(e))
            print('Gas Giant v10 test swirl rebuild error:', repr(e))
            return {'CANCELLED'}
        self.report({'INFO'}, 'Swirl test values applied and rig rebuilt.')
        return {'FINISHED'}


class GASGIANT_OT_apply_preset(bpy.types.Operator):
    bl_idname = 'gasgiant.apply_preset_v3'
    bl_label = 'Apply Preset'
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        ctrl = find_controller()
        key = context.scene.gas_giant_preset_v3
        apply_preset(ctrl, key)
        self.report({'INFO'}, f'Applied {PRESETS[key][1]}')
        return {'FINISHED'}


class GASGIANT_OT_select_ctrl(bpy.types.Operator):
    bl_idname = 'gasgiant.select_ctrl_v3'
    bl_label = 'Select Controller'
    bl_options = {'REGISTER'}
    def execute(self, context):
        ctrl = find_controller()
        bpy.ops.object.select_all(action='DESELECT')
        ctrl.select_set(True)
        context.view_layer.objects.active = ctrl
        return {'FINISHED'}


class GASGIANT_PT_panel(bpy.types.Panel):
    bl_label = 'Shader Controls v6'
    bl_idname = 'GASGIANT_PT_shader_controls_v6'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Gas Giant'
    def draw(self, context):
        layout = self.layout
        ctrl = bpy.data.objects.get(CONTROLLER_NAME)
        row = layout.row(align=True)
        row.operator('gasgiant.diagnostics_v3', icon='INFO')
        row.operator('gasgiant.select_ctrl_v3', icon='EMPTY_AXIS')
        layout.operator('gasgiant.create_preview_sphere_v10', icon='MESH_UVSPHERE')
        layout.operator('gasgiant.build_v3', icon='NODETREE')
        layout.operator('gasgiant.build_atmosphere_v5', icon='WORLD')
        layout.operator('gasgiant.test_atmosphere_v5', icon='LIGHT_HEMI')
        layout.operator('gasgiant.build_swirl_v6', icon='MOD_WARP')
        layout.operator('gasgiant.test_swirl_v6', icon='FORCE_VORTEX')
        box = layout.box()
        box.label(text='Presets')
        box.prop(context.scene, 'gas_giant_preset_v3', text='')
        box.operator('gasgiant.apply_preset_v3', icon='PRESET')
        if not ctrl:
            layout.label(text='Controller appears after build or preset.', icon='INFO')
            return
        setup_controller(ctrl)
        box = layout.box(); box.label(text='Palette')
        for i in range(1,7):
            box.prop(ctrl, f'["band_color_{i}"]', text=f'Color {i}')
        box = layout.box(); box.label(text='Cloud Structure')
        for name in ['cloud_scale','cloud_complexity','cloud_roughness','cloud_contrast','cloud_opacity']:
            box.prop(ctrl, f'["{name}"]', text=name.replace('_',' ').title())
        box = layout.box(); box.label(text='Legacy Swirl Defaults')
        for name in ['swirl_tightness','swirl_curvature','swirl_scale','swirl_offset','swirl_layer_variation']:
            box.prop(ctrl, f'["{name}"]', text=name.replace('_',' ').title())
        box = layout.box(); box.label(text='Per-Layer Swirl')
        for i in range(1,7):
            col = box.column(align=True)
            col.label(text=f'Layer {i}')
            col.prop(ctrl, f'["layer_{i}_swirl_tightness"]', text='Tightness')
            col.prop(ctrl, f'["layer_{i}_swirl_curvature"]', text='Curvature')
            col.prop(ctrl, f'["layer_{i}_swirl_scale"]', text='Scale')
            col.prop(ctrl, f'["layer_{i}_swirl_offset"]', text='Offset')
        box = layout.box(); box.label(text='Cloud Layers')
        for i in range(1,7):
            box.prop(ctrl, f'["layer_{i}_strength"]', text=f'Layer {i}')
        box = layout.box(); box.label(text='Global Color')
        for name in ['hue_shift','saturation','brightness']:
            box.prop(ctrl, f'["{name}"]', text=name.replace('_',' ').title())
        box = layout.box(); box.label(text='Planet Edge Atmosphere')
        box.prop(ctrl, '["atmosphere_color"]', text='Atmosphere Color')
        for name in ['atmosphere_strength','atmosphere_thickness','atmosphere_falloff','atmosphere_alpha']:
            box.prop(ctrl, f'["{name}"]', text=name.replace('_',' ').title())


CLASSES = [
    GASGIANT_OT_diagnostics,
    GASGIANT_OT_build,
    GASGIANT_OT_create_preview_sphere,
    GASGIANT_OT_build_atmosphere,
    GASGIANT_OT_test_atmosphere,
    GASGIANT_OT_build_swirl,
    GASGIANT_OT_test_swirl,
    GASGIANT_OT_apply_preset,
    GASGIANT_OT_select_ctrl,
    GASGIANT_PT_panel,
]


def setup_controller_deferred():
    ctrl = find_controller()
    setup_controller(ctrl)
    return None


def register():
    for c in CLASSES:
        try:
            bpy.utils.register_class(c)
        except ValueError:
            pass
    if not hasattr(bpy.types.Scene, 'gas_giant_preset_v3'):
        bpy.types.Scene.gas_giant_preset_v3 = bpy.props.EnumProperty(
            name='Gas Giant Preset',
            items=PRESET_ENUM_ITEMS,
            default=PRESET_ENUM_ITEMS[0][0],
        )
    if not bpy.app.timers.is_registered(setup_controller_deferred):
        bpy.app.timers.register(setup_controller_deferred, first_interval=0.1)


def unregister():
    if bpy.app.timers.is_registered(setup_controller_deferred):
        bpy.app.timers.unregister(setup_controller_deferred)
    if hasattr(bpy.types.Scene, 'gas_giant_preset_v3'):
        del bpy.types.Scene.gas_giant_preset_v3
    for c in reversed(CLASSES):
        try:
            bpy.utils.unregister_class(c)
        except Exception:
            pass


if __name__ == '__main__':
    register()
    print('Gas Giant Shader Controls v6 registered. Press N > Gas Giant > Diagnostics, then Build / Repair 6-Layer Rig, Build / Repair Atmosphere Edge, or Build / Repair Swirl Warp.')
