"""
Rocky/Ocean Planet Shader Controls v1

Usage:
1. Open Blender.
2. Go to Scripting, open this file, and Run Script.
3. Select a UV sphere or planet mesh.
4. Press N in the 3D Viewport.
5. Open the Rocky Planet tab.
6. Choose a preset or tune the controls.
7. Click Build / Rebuild Planet Shader.

The shader is fully procedural and is intended for orbit-view rocky/ocean
planets. It builds large landmasses, noisy coastlines, island fields, shallow
shelves, interior biome color, mountain relief, polar ice, and ocean surface
variation.
"""

bl_info = {
    "name": "Rocky/Ocean Planet Shader Controls",
    "author": "ChatGPT for James Miller",
    "version": (1, 0, 0),
    "blender": (4, 0, 0),
    "location": "View3D > Sidebar > Rocky Planet",
    "description": "Procedural rocky/ocean planet shader with continents, islands, shorelines, biomes, and terrain relief.",
    "category": "Material",
}

import bpy


MATERIAL_NAME = "Procedural Rocky Ocean Planet"
FRAME_PREFIX = "ROP"


PRESETS = {
    "earthlike": {
        "label": "Earthlike",
        "land_coverage": 0.46,
        "continent_scale": 1.55,
        "continent_detail": 9.0,
        "continent_roughness": 0.58,
        "continent_contrast": 0.19,
        "shoreline_complexity": 0.62,
        "shoreline_noise_scale": 18.0,
        "shoreline_detail": 12.0,
        "shoreline_erosion": 0.18,
        "beach_width": 0.045,
        "shelf_width": 0.14,
        "island_density": 0.38,
        "island_scale": 34.0,
        "island_threshold": 0.73,
        "island_chain_strength": 0.35,
        "biome_scale": 8.0,
        "biome_complexity": 10.0,
        "desert_coverage": 0.27,
        "forest_coverage": 0.56,
        "mountain_density": 0.42,
        "mountain_scale": 16.0,
        "mountain_sharpness": 0.68,
        "mountain_bump": 0.11,
        "polar_ice_size": 0.16,
        "snow_threshold": 0.74,
        "ocean_bump": 0.025,
    },
    "archipelago": {
        "label": "Archipelago World",
        "land_coverage": 0.32,
        "continent_scale": 2.75,
        "continent_detail": 12.0,
        "continent_roughness": 0.66,
        "continent_contrast": 0.15,
        "shoreline_complexity": 0.86,
        "shoreline_noise_scale": 28.0,
        "shoreline_detail": 14.0,
        "shoreline_erosion": 0.34,
        "beach_width": 0.06,
        "shelf_width": 0.18,
        "island_density": 0.82,
        "island_scale": 48.0,
        "island_threshold": 0.64,
        "island_chain_strength": 0.74,
        "biome_scale": 12.0,
        "biome_complexity": 12.0,
        "desert_coverage": 0.18,
        "forest_coverage": 0.66,
        "mountain_density": 0.34,
        "mountain_scale": 20.0,
        "mountain_sharpness": 0.55,
        "mountain_bump": 0.08,
        "polar_ice_size": 0.08,
        "snow_threshold": 0.82,
        "ocean_bump": 0.03,
    },
    "supercontinent": {
        "label": "Supercontinent",
        "land_coverage": 0.58,
        "continent_scale": 0.95,
        "continent_detail": 8.0,
        "continent_roughness": 0.52,
        "continent_contrast": 0.23,
        "shoreline_complexity": 0.48,
        "shoreline_noise_scale": 13.0,
        "shoreline_detail": 10.0,
        "shoreline_erosion": 0.12,
        "beach_width": 0.035,
        "shelf_width": 0.11,
        "island_density": 0.16,
        "island_scale": 26.0,
        "island_threshold": 0.80,
        "island_chain_strength": 0.22,
        "biome_scale": 6.5,
        "biome_complexity": 9.0,
        "desert_coverage": 0.46,
        "forest_coverage": 0.36,
        "mountain_density": 0.55,
        "mountain_scale": 11.0,
        "mountain_sharpness": 0.78,
        "mountain_bump": 0.14,
        "polar_ice_size": 0.20,
        "snow_threshold": 0.70,
        "ocean_bump": 0.018,
    },
    "dry_rocky": {
        "label": "Dry Rocky World",
        "land_coverage": 0.68,
        "continent_scale": 1.35,
        "continent_detail": 11.0,
        "continent_roughness": 0.64,
        "continent_contrast": 0.20,
        "shoreline_complexity": 0.55,
        "shoreline_noise_scale": 21.0,
        "shoreline_detail": 12.0,
        "shoreline_erosion": 0.22,
        "beach_width": 0.025,
        "shelf_width": 0.08,
        "island_density": 0.12,
        "island_scale": 30.0,
        "island_threshold": 0.82,
        "island_chain_strength": 0.28,
        "biome_scale": 10.0,
        "biome_complexity": 13.0,
        "desert_coverage": 0.72,
        "forest_coverage": 0.12,
        "mountain_density": 0.62,
        "mountain_scale": 18.0,
        "mountain_sharpness": 0.86,
        "mountain_bump": 0.16,
        "polar_ice_size": 0.04,
        "snow_threshold": 0.88,
        "ocean_bump": 0.014,
    },
    "frozen_ocean": {
        "label": "Frozen Ocean World",
        "land_coverage": 0.28,
        "continent_scale": 1.85,
        "continent_detail": 8.0,
        "continent_roughness": 0.50,
        "continent_contrast": 0.18,
        "shoreline_complexity": 0.40,
        "shoreline_noise_scale": 12.0,
        "shoreline_detail": 8.0,
        "shoreline_erosion": 0.10,
        "beach_width": 0.02,
        "shelf_width": 0.10,
        "island_density": 0.18,
        "island_scale": 22.0,
        "island_threshold": 0.78,
        "island_chain_strength": 0.24,
        "biome_scale": 7.0,
        "biome_complexity": 8.0,
        "desert_coverage": 0.10,
        "forest_coverage": 0.18,
        "mountain_density": 0.38,
        "mountain_scale": 13.0,
        "mountain_sharpness": 0.60,
        "mountain_bump": 0.07,
        "polar_ice_size": 0.48,
        "snow_threshold": 0.48,
        "ocean_bump": 0.012,
    },
}

PRESET_ITEMS = [(key, value["label"], value["label"]) for key, value in PRESETS.items()]


def clamp(value, low, high):
    return max(low, min(high, value))


def active_planet_object():
    obj = bpy.context.object
    if obj and obj.type == "MESH":
        return obj
    return None


def new_node(nodes, node_type, label, loc, parent=None):
    node = nodes.new(node_type)
    node.label = label
    node.name = label
    node.location = loc
    if parent:
        node.parent = parent
    return node


def new_frame(nodes, label, loc):
    frame = nodes.new("NodeFrame")
    frame.label = label
    frame.name = label
    frame.location = loc
    return frame


def socket(node, name, fallback_index=None):
    if name in node.inputs:
        return node.inputs[name]
    if fallback_index is not None:
        return node.inputs[fallback_index]
    raise KeyError(f"{node.name} has no input named {name}")


def out_socket(node, name, fallback_index=None):
    if name in node.outputs:
        return node.outputs[name]
    if fallback_index is not None:
        return node.outputs[fallback_index]
    raise KeyError(f"{node.name} has no output named {name}")


def set_color_ramp(ramp_node, stops):
    ramp = ramp_node.color_ramp
    while len(ramp.elements) < len(stops):
        ramp.elements.new(0.5)
    while len(ramp.elements) > len(stops):
        ramp.elements.remove(ramp.elements[-1])
    for element, (pos, color) in zip(ramp.elements, stops):
        element.position = clamp(pos, 0.0, 1.0)
        element.color = color


def set_principled_input(node, names, value):
    for name in names:
        if name in node.inputs:
            node.inputs[name].default_value = value
            return


def material_for_object(obj):
    mat = bpy.data.materials.get(MATERIAL_NAME)
    if mat is None:
        mat = bpy.data.materials.new(MATERIAL_NAME)
    mat.use_nodes = True
    if obj.data.materials:
        obj.data.materials[0] = mat
    else:
        obj.data.materials.append(mat)
    return mat


def clear_material_nodes(mat):
    nodes = mat.node_tree.nodes
    nodes.clear()


def create_mix_rgb(nodes, label, loc, blend_type="MIX", factor=0.5, parent=None):
    node = new_node(nodes, "ShaderNodeMixRGB", label, loc, parent)
    node.blend_type = blend_type
    node.inputs["Fac"].default_value = factor
    return node


def create_noise(nodes, label, loc, scale, detail, roughness, parent=None):
    node = new_node(nodes, "ShaderNodeTexNoise", label, loc, parent)
    node.inputs["Scale"].default_value = scale
    node.inputs["Detail"].default_value = detail
    node.inputs["Roughness"].default_value = roughness
    return node


def create_math(nodes, label, loc, operation, value1=None, value2=None, parent=None):
    node = new_node(nodes, "ShaderNodeMath", label, loc, parent)
    node.operation = operation
    if value1 is not None:
        node.inputs[0].default_value = value1
    if value2 is not None:
        node.inputs[1].default_value = value2
    return node


def add_latitude_nodes(nodes, links, texcoord, loc, props, parent):
    separate = new_node(nodes, "ShaderNodeSeparateXYZ", "Latitude From Generated Z", loc, parent)
    abs_z = create_math(nodes, "Absolute Latitude", (loc[0] + 220, loc[1]), "ABSOLUTE", parent=parent)
    ice_ramp = new_node(nodes, "ShaderNodeValToRGB", "Polar Ice Mask", (loc[0] + 440, loc[1]), parent)
    ice_edge = clamp(1.0 - props.polar_ice_size, 0.05, 0.98)
    set_color_ramp(
        ice_ramp,
        [
            (max(0.0, ice_edge - 0.06), (0.0, 0.0, 0.0, 1.0)),
            (ice_edge, (0.22, 0.22, 0.22, 1.0)),
            (min(1.0, ice_edge + 0.08), (1.0, 1.0, 1.0, 1.0)),
        ],
    )
    links.new(out_socket(texcoord, "Generated"), separate.inputs["Vector"])
    links.new(separate.outputs["Z"], abs_z.inputs[0])
    links.new(abs_z.outputs["Value"], ice_ramp.inputs["Fac"])
    return ice_ramp


def build_rocky_ocean_shader(obj, props):
    mat = material_for_object(obj)
    clear_material_nodes(mat)
    mat.diffuse_color = (0.08, 0.18, 0.22, 1.0)

    nodes = mat.node_tree.nodes
    links = mat.node_tree.links

    coord_frame = new_frame(nodes, f"{FRAME_PREFIX} Coordinates", (-900, 300))
    land_frame = new_frame(nodes, f"{FRAME_PREFIX} Land / Ocean Mask", (-590, 290))
    coast_frame = new_frame(nodes, f"{FRAME_PREFIX} Shorelines and Islands", (-590, -110))
    biome_frame = new_frame(nodes, f"{FRAME_PREFIX} Interior Biomes", (-170, 260))
    relief_frame = new_frame(nodes, f"{FRAME_PREFIX} Relief", (-170, -310))
    surface_frame = new_frame(nodes, f"{FRAME_PREFIX} Surface Assembly", (330, 80))

    texcoord = new_node(nodes, "ShaderNodeTexCoord", "Planet Coordinates", (-900, 420), coord_frame)
    mapping = new_node(nodes, "ShaderNodeMapping", "Seed / Orientation Mapping", (-700, 420), coord_frame)
    mapping.inputs["Location"].default_value = (
        props.seed_offset_x,
        props.seed_offset_y,
        props.seed_offset_z,
    )
    mapping.inputs["Rotation"].default_value = (
        props.rotation_x,
        props.rotation_y,
        props.rotation_z,
    )
    mapping.inputs["Scale"].default_value = (
        props.stretch_x,
        props.stretch_y,
        props.stretch_z,
    )
    links.new(out_socket(texcoord, "Generated"), mapping.inputs["Vector"])

    continent_noise = create_noise(
        nodes,
        "Major Continent Noise",
        (-580, 470),
        props.continent_scale,
        props.continent_detail,
        props.continent_roughness,
        land_frame,
    )
    coastline_noise = create_noise(
        nodes,
        "Coastline Fractal Detail",
        (-580, 210),
        props.shoreline_noise_scale,
        props.shoreline_detail,
        0.62,
        land_frame,
    )
    coast_center = create_math(nodes, "Center Coast Noise", (-360, 210), "SUBTRACT", value2=0.5, parent=land_frame)
    coast_amp = create_math(
        nodes,
        "Coastline Distortion Amount",
        (-150, 210),
        "MULTIPLY",
        value2=props.shoreline_complexity * 0.28,
        parent=land_frame,
    )
    erode = create_math(
        nodes,
        "Shoreline Erosion Bias",
        (-150, 80),
        "SUBTRACT",
        value2=props.shoreline_erosion * 0.16,
        parent=land_frame,
    )
    combine_land = create_math(nodes, "Distorted Continent Field", (70, 380), "ADD", parent=land_frame)
    land_ramp = new_node(nodes, "ShaderNodeValToRGB", "Land Mask Threshold", (290, 380), land_frame)
    threshold = clamp(1.0 - props.land_coverage, 0.05, 0.95)
    contrast = clamp(props.continent_contrast, 0.01, 0.45)
    set_color_ramp(
        land_ramp,
        [
            (threshold - contrast, (0.0, 0.0, 0.0, 1.0)),
            (threshold + contrast, (1.0, 1.0, 1.0, 1.0)),
        ],
    )
    links.new(mapping.outputs["Vector"], continent_noise.inputs["Vector"])
    links.new(mapping.outputs["Vector"], coastline_noise.inputs["Vector"])
    links.new(continent_noise.outputs["Fac"], combine_land.inputs[0])
    links.new(coastline_noise.outputs["Fac"], coast_center.inputs[0])
    links.new(coast_center.outputs["Value"], coast_amp.inputs[0])
    links.new(coast_amp.outputs["Value"], erode.inputs[0])
    links.new(erode.outputs["Value"], combine_land.inputs[1])
    links.new(combine_land.outputs["Value"], land_ramp.inputs["Fac"])

    island_noise = create_noise(
        nodes,
        "Island Field Noise",
        (-580, -40),
        props.island_scale,
        14.0,
        0.68,
        coast_frame,
    )
    chain_wave = new_node(nodes, "ShaderNodeTexWave", "Island Chain Grain", (-580, -230), coast_frame)
    chain_wave.bands_direction = "DIAGONAL"
    chain_wave.inputs["Scale"].default_value = props.island_scale * 0.18
    chain_wave.inputs["Distortion"].default_value = props.island_chain_strength * 18.0
    island_chain_mix = create_mix_rgb(
        nodes,
        "Island Chain Influence",
        (-340, -80),
        factor=props.island_chain_strength,
        parent=coast_frame,
    )
    island_ramp = new_node(nodes, "ShaderNodeValToRGB", "Island Threshold", (-120, -80), coast_frame)
    island_threshold = clamp(props.island_threshold - props.island_density * 0.18, 0.25, 0.95)
    set_color_ramp(
        island_ramp,
        [
            (island_threshold, (0.0, 0.0, 0.0, 1.0)),
            (min(1.0, island_threshold + 0.07), (1.0, 1.0, 1.0, 1.0)),
        ],
    )
    land_or_island = create_math(nodes, "Land Plus Islands", (110, 80), "MAXIMUM", parent=coast_frame)
    shelf_ramp = new_node(nodes, "ShaderNodeValToRGB", "Coastal Shelf / Shallow Water", (110, -210), coast_frame)
    shelf_outer = clamp(threshold - props.shelf_width, 0.0, 1.0)
    shelf_inner = clamp(threshold + props.beach_width, 0.0, 1.0)
    set_color_ramp(
        shelf_ramp,
        [
            (shelf_outer, (0.0, 0.0, 0.0, 1.0)),
            (threshold, (0.8, 0.8, 0.8, 1.0)),
            (shelf_inner, (1.0, 1.0, 1.0, 1.0)),
        ],
    )
    beach_ramp = new_node(nodes, "ShaderNodeValToRGB", "Beach / Shore Band", (340, -210), coast_frame)
    set_color_ramp(
        beach_ramp,
        [
            (clamp(threshold - props.beach_width, 0.0, 1.0), (0.0, 0.0, 0.0, 1.0)),
            (threshold, (1.0, 1.0, 1.0, 1.0)),
            (clamp(threshold + props.beach_width, 0.0, 1.0), (0.0, 0.0, 0.0, 1.0)),
        ],
    )
    links.new(mapping.outputs["Vector"], island_noise.inputs["Vector"])
    links.new(mapping.outputs["Vector"], chain_wave.inputs["Vector"])
    links.new(island_noise.outputs["Fac"], island_chain_mix.inputs["Color1"])
    links.new(chain_wave.outputs["Color"], island_chain_mix.inputs["Color2"])
    links.new(island_chain_mix.outputs["Color"], island_ramp.inputs["Fac"])
    links.new(land_ramp.outputs["Color"], land_or_island.inputs[0])
    links.new(island_ramp.outputs["Color"], land_or_island.inputs[1])
    links.new(combine_land.outputs["Value"], shelf_ramp.inputs["Fac"])
    links.new(combine_land.outputs["Value"], beach_ramp.inputs["Fac"])

    biome_noise = create_noise(
        nodes,
        "Interior Biome Noise",
        (-160, 590),
        props.biome_scale,
        props.biome_complexity,
        0.57,
        biome_frame,
    )
    biome_ramp = new_node(nodes, "ShaderNodeValToRGB", "Biome Color Ramp", (70, 590), biome_frame)
    forest_stop = clamp(0.22 + (1.0 - props.forest_coverage) * 0.22, 0.12, 0.60)
    desert_stop = clamp(0.58 - props.desert_coverage * 0.22, 0.30, 0.74)
    set_color_ramp(
        biome_ramp,
        [
            (0.00, props.forest_dark_color),
            (forest_stop, props.forest_color),
            (0.48, props.grassland_color),
            (desert_stop, props.dry_plain_color),
            (0.82, props.desert_color),
            (1.00, props.rock_color),
        ],
    )
    mountain_noise = create_noise(
        nodes,
        "Mountain Ridge Noise",
        (-160, 350),
        props.mountain_scale,
        15.0,
        0.72,
        biome_frame,
    )
    mountain_ramp = new_node(nodes, "ShaderNodeValToRGB", "Mountain Mask", (70, 350), biome_frame)
    mountain_start = clamp(1.0 - props.mountain_density, 0.12, 0.92)
    set_color_ramp(
        mountain_ramp,
        [
            (mountain_start, (0.0, 0.0, 0.0, 1.0)),
            (clamp(mountain_start + 0.20 - props.mountain_sharpness * 0.16, 0.0, 1.0), (1.0, 1.0, 1.0, 1.0)),
        ],
    )
    mountain_color_mix = create_mix_rgb(nodes, "Add Rocky Highlands", (300, 510), factor=0.58, parent=biome_frame)
    snow_ramp = new_node(nodes, "ShaderNodeValToRGB", "High Mountain Snow", (300, 300), biome_frame)
    set_color_ramp(
        snow_ramp,
        [
            (props.snow_threshold, (0.0, 0.0, 0.0, 1.0)),
            (min(1.0, props.snow_threshold + 0.10), (1.0, 1.0, 1.0, 1.0)),
        ],
    )
    snow_mix = create_mix_rgb(nodes, "Blend Snowcaps", (530, 510), factor=0.55, parent=biome_frame)
    polar_ice = add_latitude_nodes(nodes, links, texcoord, (-160, 90), props, biome_frame)
    polar_mix = create_mix_rgb(nodes, "Blend Polar Ice", (760, 510), factor=0.7, parent=biome_frame)
    links.new(mapping.outputs["Vector"], biome_noise.inputs["Vector"])
    links.new(mapping.outputs["Vector"], mountain_noise.inputs["Vector"])
    links.new(biome_noise.outputs["Fac"], biome_ramp.inputs["Fac"])
    links.new(mountain_noise.outputs["Fac"], mountain_ramp.inputs["Fac"])
    links.new(mountain_noise.outputs["Fac"], snow_ramp.inputs["Fac"])
    links.new(mountain_ramp.outputs["Color"], mountain_color_mix.inputs["Fac"])
    links.new(biome_ramp.outputs["Color"], mountain_color_mix.inputs["Color1"])
    mountain_color_mix.inputs["Color2"].default_value = props.rock_color
    links.new(snow_ramp.outputs["Color"], snow_mix.inputs["Fac"])
    links.new(mountain_color_mix.outputs["Color"], snow_mix.inputs["Color1"])
    snow_mix.inputs["Color2"].default_value = props.snow_color
    links.new(polar_ice.outputs["Color"], polar_mix.inputs["Fac"])
    links.new(snow_mix.outputs["Color"], polar_mix.inputs["Color1"])
    polar_mix.inputs["Color2"].default_value = props.ice_color

    ocean_noise = create_noise(nodes, "Ocean Current Color Noise", (330, 40), 22.0, 8.0, 0.52, surface_frame)
    ocean_color_mix = create_mix_rgb(nodes, "Deep Ocean Variation", (550, 40), factor=0.20, parent=surface_frame)
    shallow_mix = create_mix_rgb(nodes, "Shallow Shelf Water", (770, 40), factor=0.5, parent=surface_frame)
    shore_mix = create_mix_rgb(nodes, "Beach Color Band", (1000, 140), factor=0.5, parent=surface_frame)
    final_land_ocean = create_mix_rgb(nodes, "Final Land / Ocean Mix", (1230, 250), factor=0.5, parent=surface_frame)
    ocean_color_mix.inputs["Color1"].default_value = props.deep_ocean_color
    ocean_color_mix.inputs["Color2"].default_value = props.ocean_variation_color
    shallow_mix.inputs["Color2"].default_value = props.shallow_ocean_color
    shore_mix.inputs["Color2"].default_value = props.beach_color
    links.new(mapping.outputs["Vector"], ocean_noise.inputs["Vector"])
    links.new(ocean_noise.outputs["Fac"], ocean_color_mix.inputs["Fac"])
    links.new(ocean_color_mix.outputs["Color"], shallow_mix.inputs["Color1"])
    links.new(shelf_ramp.outputs["Color"], shallow_mix.inputs["Fac"])
    links.new(shallow_mix.outputs["Color"], shore_mix.inputs["Color1"])
    links.new(beach_ramp.outputs["Color"], shore_mix.inputs["Fac"])
    links.new(shore_mix.outputs["Color"], final_land_ocean.inputs["Color1"])
    links.new(polar_mix.outputs["Color"], final_land_ocean.inputs["Color2"])
    links.new(land_or_island.outputs["Value"], final_land_ocean.inputs["Fac"])

    relief_land = create_math(nodes, "Land Relief Mask", (-160, -190), "MULTIPLY", parent=relief_frame)
    relief_strength = create_math(nodes, "Land Relief Strength", (70, -190), "MULTIPLY", value2=props.mountain_bump, parent=relief_frame)
    ocean_bump_noise = create_noise(nodes, "Ocean Micro Wave Noise", (-160, -430), 95.0, 7.0, 0.58, relief_frame)
    ocean_mask_inv = create_math(nodes, "Ocean Mask", (70, -430), "SUBTRACT", value1=1.0, parent=relief_frame)
    ocean_relief = create_math(nodes, "Ocean Wave Strength", (300, -430), "MULTIPLY", value2=props.ocean_bump, parent=relief_frame)
    relief_add = create_math(nodes, "Combined Surface Height", (530, -280), "ADD", parent=relief_frame)
    bump = new_node(nodes, "ShaderNodeBump", "Planet Bump", (760, -280), relief_frame)
    bump.inputs["Strength"].default_value = 1.0
    bump.inputs["Distance"].default_value = 0.09
    links.new(mountain_ramp.outputs["Color"], relief_land.inputs[0])
    links.new(land_or_island.outputs["Value"], relief_land.inputs[1])
    links.new(relief_land.outputs["Value"], relief_strength.inputs[0])
    links.new(mapping.outputs["Vector"], ocean_bump_noise.inputs["Vector"])
    links.new(land_or_island.outputs["Value"], ocean_mask_inv.inputs[1])
    links.new(ocean_bump_noise.outputs["Fac"], ocean_relief.inputs[0])
    links.new(ocean_mask_inv.outputs["Value"], ocean_relief.inputs[1])
    links.new(relief_strength.outputs["Value"], relief_add.inputs[0])
    links.new(ocean_relief.outputs["Value"], relief_add.inputs[1])
    links.new(relief_add.outputs["Value"], bump.inputs["Height"])

    principled = new_node(nodes, "ShaderNodeBsdfPrincipled", "Rocky Ocean Planet BSDF", (1530, 250), surface_frame)
    output = new_node(nodes, "ShaderNodeOutputMaterial", "Material Output", (1810, 250), surface_frame)
    set_principled_input(principled, ["Base Color"], (0.08, 0.18, 0.22, 1.0))
    set_principled_input(principled, ["Roughness"], props.surface_roughness)
    set_principled_input(principled, ["Metallic"], 0.0)
    set_principled_input(principled, ["Alpha"], 1.0)
    if "Specular IOR Level" in principled.inputs:
        principled.inputs["Specular IOR Level"].default_value = props.ocean_specular
    elif "Specular" in principled.inputs:
        principled.inputs["Specular"].default_value = props.ocean_specular
    links.new(final_land_ocean.outputs["Color"], principled.inputs["Base Color"])
    links.new(bump.outputs["Normal"], principled.inputs["Normal"])
    links.new(principled.outputs["BSDF"], output.inputs["Surface"])

    mat["rocky_ocean_shader_version"] = "v1"
    return mat


class RockyOceanPlanetProperties(bpy.types.PropertyGroup):
    preset: bpy.props.EnumProperty(name="Preset", items=PRESET_ITEMS, default="earthlike")

    seed_offset_x: bpy.props.FloatProperty(name="Seed X", default=8.3, min=-1000.0, max=1000.0)
    seed_offset_y: bpy.props.FloatProperty(name="Seed Y", default=21.7, min=-1000.0, max=1000.0)
    seed_offset_z: bpy.props.FloatProperty(name="Seed Z", default=-4.6, min=-1000.0, max=1000.0)
    rotation_x: bpy.props.FloatProperty(name="Rotation X", default=0.0, min=-6.283, max=6.283)
    rotation_y: bpy.props.FloatProperty(name="Rotation Y", default=0.0, min=-6.283, max=6.283)
    rotation_z: bpy.props.FloatProperty(name="Rotation Z", default=0.0, min=-6.283, max=6.283)
    stretch_x: bpy.props.FloatProperty(name="Stretch X", default=1.0, min=0.1, max=6.0)
    stretch_y: bpy.props.FloatProperty(name="Stretch Y", default=1.0, min=0.1, max=6.0)
    stretch_z: bpy.props.FloatProperty(name="Stretch Z", default=1.0, min=0.1, max=6.0)

    land_coverage: bpy.props.FloatProperty(name="Global Land Coverage", default=0.46, min=0.02, max=0.95)
    continent_scale: bpy.props.FloatProperty(name="Continent Scale", default=1.55, min=0.25, max=8.0)
    continent_detail: bpy.props.FloatProperty(name="Continent Detail Layers", default=9.0, min=0.0, max=15.0)
    continent_roughness: bpy.props.FloatProperty(name="Continent Roughness", default=0.58, min=0.0, max=1.0)
    continent_contrast: bpy.props.FloatProperty(name="Continent Edge Contrast", default=0.19, min=0.01, max=0.45)

    shoreline_complexity: bpy.props.FloatProperty(name="Shoreline Complexity", default=0.62, min=0.0, max=1.0)
    shoreline_noise_scale: bpy.props.FloatProperty(name="Shoreline Noise Scale", default=18.0, min=1.0, max=90.0)
    shoreline_detail: bpy.props.FloatProperty(name="Shoreline Detail Layers", default=12.0, min=0.0, max=15.0)
    shoreline_erosion: bpy.props.FloatProperty(name="Shoreline Erosion", default=0.18, min=0.0, max=1.0)
    beach_width: bpy.props.FloatProperty(name="Beach Width", default=0.045, min=0.0, max=0.18)
    shelf_width: bpy.props.FloatProperty(name="Coastal Shelf Width", default=0.14, min=0.0, max=0.35)

    island_density: bpy.props.FloatProperty(name="Island Density", default=0.38, min=0.0, max=1.0)
    island_scale: bpy.props.FloatProperty(name="Island Scale", default=34.0, min=4.0, max=120.0)
    island_threshold: bpy.props.FloatProperty(name="Island Threshold", default=0.73, min=0.2, max=0.98)
    island_chain_strength: bpy.props.FloatProperty(name="Island Chain Strength", default=0.35, min=0.0, max=1.0)

    biome_scale: bpy.props.FloatProperty(name="Interior Biome Scale", default=8.0, min=0.5, max=40.0)
    biome_complexity: bpy.props.FloatProperty(name="Interior Biome Complexity", default=10.0, min=0.0, max=15.0)
    desert_coverage: bpy.props.FloatProperty(name="Desert Coverage", default=0.27, min=0.0, max=1.0)
    forest_coverage: bpy.props.FloatProperty(name="Forest Coverage", default=0.56, min=0.0, max=1.0)
    mountain_density: bpy.props.FloatProperty(name="Mountain Density", default=0.42, min=0.0, max=1.0)
    mountain_scale: bpy.props.FloatProperty(name="Mountain Scale", default=16.0, min=1.0, max=80.0)
    mountain_sharpness: bpy.props.FloatProperty(name="Mountain Ridge Sharpness", default=0.68, min=0.0, max=1.0)
    mountain_bump: bpy.props.FloatProperty(name="Mountain Bump Strength", default=0.11, min=0.0, max=0.5)
    polar_ice_size: bpy.props.FloatProperty(name="Polar Ice Cap Size", default=0.16, min=0.0, max=0.75)
    snow_threshold: bpy.props.FloatProperty(name="Snow Elevation Threshold", default=0.74, min=0.2, max=1.0)

    ocean_bump: bpy.props.FloatProperty(name="Ocean Micro Wave Bump", default=0.025, min=0.0, max=0.12)
    ocean_specular: bpy.props.FloatProperty(name="Ocean Specular", default=0.65, min=0.0, max=1.0)
    surface_roughness: bpy.props.FloatProperty(name="Surface Roughness", default=0.44, min=0.0, max=1.0)

    deep_ocean_color: bpy.props.FloatVectorProperty(name="Deep Ocean", subtype="COLOR", size=4, default=(0.015, 0.055, 0.18, 1.0), min=0.0, max=1.0)
    ocean_variation_color: bpy.props.FloatVectorProperty(name="Ocean Variation", subtype="COLOR", size=4, default=(0.02, 0.16, 0.30, 1.0), min=0.0, max=1.0)
    shallow_ocean_color: bpy.props.FloatVectorProperty(name="Shallow Ocean", subtype="COLOR", size=4, default=(0.10, 0.52, 0.58, 1.0), min=0.0, max=1.0)
    beach_color: bpy.props.FloatVectorProperty(name="Beach", subtype="COLOR", size=4, default=(0.78, 0.69, 0.46, 1.0), min=0.0, max=1.0)
    forest_dark_color: bpy.props.FloatVectorProperty(name="Dark Forest", subtype="COLOR", size=4, default=(0.035, 0.16, 0.075, 1.0), min=0.0, max=1.0)
    forest_color: bpy.props.FloatVectorProperty(name="Forest", subtype="COLOR", size=4, default=(0.07, 0.31, 0.11, 1.0), min=0.0, max=1.0)
    grassland_color: bpy.props.FloatVectorProperty(name="Grassland", subtype="COLOR", size=4, default=(0.30, 0.44, 0.18, 1.0), min=0.0, max=1.0)
    dry_plain_color: bpy.props.FloatVectorProperty(name="Dry Plain", subtype="COLOR", size=4, default=(0.52, 0.45, 0.25, 1.0), min=0.0, max=1.0)
    desert_color: bpy.props.FloatVectorProperty(name="Desert", subtype="COLOR", size=4, default=(0.70, 0.52, 0.28, 1.0), min=0.0, max=1.0)
    rock_color: bpy.props.FloatVectorProperty(name="Rock / Mountain", subtype="COLOR", size=4, default=(0.42, 0.40, 0.36, 1.0), min=0.0, max=1.0)
    snow_color: bpy.props.FloatVectorProperty(name="Snow", subtype="COLOR", size=4, default=(0.92, 0.95, 0.93, 1.0), min=0.0, max=1.0)
    ice_color: bpy.props.FloatVectorProperty(name="Polar Ice", subtype="COLOR", size=4, default=(0.78, 0.91, 0.96, 1.0), min=0.0, max=1.0)


class ROP_OT_apply_preset(bpy.types.Operator):
    bl_idname = "rop.apply_preset"
    bl_label = "Apply Preset"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        props = context.scene.rocky_ocean_planet
        data = PRESETS.get(props.preset)
        if not data:
            self.report({"ERROR"}, "Unknown preset")
            return {"CANCELLED"}
        for key, value in data.items():
            if key == "label":
                continue
            if hasattr(props, key):
                setattr(props, key, value)
        self.report({"INFO"}, f"Applied {data['label']}")
        return {"FINISHED"}


class ROP_OT_randomize_seed(bpy.types.Operator):
    bl_idname = "rop.randomize_seed"
    bl_label = "Randomize Seed"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        props = context.scene.rocky_ocean_planet
        import random

        props.seed_offset_x = random.uniform(-300.0, 300.0)
        props.seed_offset_y = random.uniform(-300.0, 300.0)
        props.seed_offset_z = random.uniform(-300.0, 300.0)
        props.rotation_x = random.uniform(-3.14159, 3.14159)
        props.rotation_y = random.uniform(-3.14159, 3.14159)
        props.rotation_z = random.uniform(-3.14159, 3.14159)
        self.report({"INFO"}, "Randomized planet seed")
        return {"FINISHED"}


class ROP_OT_build_shader(bpy.types.Operator):
    bl_idname = "rop.build_shader"
    bl_label = "Build / Rebuild Planet Shader"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        obj = active_planet_object()
        if obj is None:
            self.report({"ERROR"}, "Select a mesh planet object first")
            return {"CANCELLED"}
        mat = build_rocky_ocean_shader(obj, context.scene.rocky_ocean_planet)
        self.report({"INFO"}, f"Built {mat.name} on {obj.name}")
        return {"FINISHED"}


class ROP_OT_create_preview_planet(bpy.types.Operator):
    bl_idname = "rop.create_preview_planet"
    bl_label = "Create Preview Planet"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        bpy.ops.mesh.primitive_uv_sphere_add(segments=128, ring_count=64, radius=2.0, location=(0, 0, 0))
        obj = context.object
        obj.name = "Rocky Ocean Planet Preview"
        build_rocky_ocean_shader(obj, context.scene.rocky_ocean_planet)
        try:
            bpy.ops.object.shade_smooth()
        except Exception:
            pass
        self.report({"INFO"}, "Created preview planet")
        return {"FINISHED"}


class ROP_PT_panel(bpy.types.Panel):
    bl_label = "Rocky/Ocean Planet"
    bl_idname = "ROP_PT_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Rocky Planet"

    def draw(self, context):
        layout = self.layout
        props = context.scene.rocky_ocean_planet
        obj = active_planet_object()

        if obj:
            layout.label(text=f"Target: {obj.name}", icon="MESH_UVSPHERE")
        else:
            layout.label(text="Select a mesh planet object", icon="ERROR")

        row = layout.row(align=True)
        row.operator("rop.create_preview_planet", icon="SPHERE")
        row.operator("rop.build_shader", icon="NODE_MATERIAL")

        box = layout.box()
        box.prop(props, "preset")
        row = box.row(align=True)
        row.operator("rop.apply_preset", icon="CHECKMARK")
        row.operator("rop.randomize_seed", icon="FILE_REFRESH")

        box = layout.box()
        box.label(text="Planet Layout")
        box.prop(props, "land_coverage")
        box.prop(props, "continent_scale")
        box.prop(props, "continent_detail")
        box.prop(props, "continent_roughness")
        box.prop(props, "continent_contrast")

        box = layout.box()
        box.label(text="Shorelines")
        box.prop(props, "shoreline_complexity")
        box.prop(props, "shoreline_noise_scale")
        box.prop(props, "shoreline_detail")
        box.prop(props, "shoreline_erosion")
        box.prop(props, "beach_width")
        box.prop(props, "shelf_width")

        box = layout.box()
        box.label(text="Islands")
        box.prop(props, "island_density")
        box.prop(props, "island_scale")
        box.prop(props, "island_threshold")
        box.prop(props, "island_chain_strength")

        box = layout.box()
        box.label(text="Interiors")
        box.prop(props, "biome_scale")
        box.prop(props, "biome_complexity")
        box.prop(props, "forest_coverage")
        box.prop(props, "desert_coverage")
        box.prop(props, "mountain_density")
        box.prop(props, "mountain_scale")
        box.prop(props, "mountain_sharpness")
        box.prop(props, "mountain_bump")
        box.prop(props, "polar_ice_size")
        box.prop(props, "snow_threshold")

        box = layout.box()
        box.label(text="Ocean / Surface")
        box.prop(props, "ocean_bump")
        box.prop(props, "ocean_specular")
        box.prop(props, "surface_roughness")

        box = layout.box()
        box.label(text="Seed / Orientation")
        row = box.row(align=True)
        row.prop(props, "seed_offset_x")
        row.prop(props, "seed_offset_y")
        row.prop(props, "seed_offset_z")
        row = box.row(align=True)
        row.prop(props, "rotation_x")
        row.prop(props, "rotation_y")
        row.prop(props, "rotation_z")
        row = box.row(align=True)
        row.prop(props, "stretch_x")
        row.prop(props, "stretch_y")
        row.prop(props, "stretch_z")

        box = layout.box()
        box.label(text="Colors")
        box.prop(props, "deep_ocean_color")
        box.prop(props, "shallow_ocean_color")
        box.prop(props, "beach_color")
        box.prop(props, "forest_color")
        box.prop(props, "grassland_color")
        box.prop(props, "desert_color")
        box.prop(props, "rock_color")
        box.prop(props, "snow_color")
        box.prop(props, "ice_color")


CLASSES = (
    RockyOceanPlanetProperties,
    ROP_OT_apply_preset,
    ROP_OT_randomize_seed,
    ROP_OT_build_shader,
    ROP_OT_create_preview_planet,
    ROP_PT_panel,
)


def register():
    for cls in CLASSES:
        bpy.utils.register_class(cls)
    bpy.types.Scene.rocky_ocean_planet = bpy.props.PointerProperty(type=RockyOceanPlanetProperties)


def unregister():
    if hasattr(bpy.types.Scene, "rocky_ocean_planet"):
        del bpy.types.Scene.rocky_ocean_planet
    for cls in reversed(CLASSES):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
