"""motion_blender.py — Criação de figuras 3D e animações em Motion Design com Blender (bpy).
Alinhado à identidade visual SENAI: estúdio com iluminação three-point, fundo transparente,
materiais PBR oficiais (Azul SENAI, Laranja acento, Acrílico e Água translúcida).
"""
import math
import os
import shutil
import sys
from pathlib import Path

import bpy
import imageio_ffmpeg

# Paleta SENAI em espaço linear sRGB para o Blender
COLOR_SENAI_BLUE = (0.010, 0.051, 0.301, 1.0)       # #0E4194
COLOR_SENAI_ORANGE = (0.791, 0.065, 0.007, 1.0)     # #E8490F
COLOR_SENAI_PETROL = (0.003, 0.063, 0.216, 1.0)     # #074982
COLOR_SENAI_LIGHT_BLUE = (0.638, 0.760, 0.947, 1.0) # #D0E1F9
COLOR_WATER = (0.050, 0.350, 0.850, 0.6)            # Líquido translúcido


def clear_scene():
    """Limpa completamente a cena do Blender."""
    bpy.ops.wm.read_factory_settings(use_empty=True)
    for block in bpy.data.meshes:
        bpy.data.meshes.remove(block)
    for block in bpy.data.materials:
        bpy.data.materials.remove(block)
    for block in bpy.data.lights:
        bpy.data.lights.remove(block)
    for block in bpy.data.cameras:
        bpy.data.cameras.remove(block)


def setup_studio(camera_dist=13.5, camera_rot=(1.10, 0, 0.785), transparent=True):
    """Monta estúdio 3D com iluminação three-point e fundo transparente."""
    scene = bpy.context.scene
    scene.render.film_transparent = transparent
    scene.render.image_settings.color_mode = 'RGBA' if transparent else 'RGB'

    # Câmera com enquadramento respirado (50mm)
    cam_data = bpy.data.cameras.new("StudioCamera")
    cam_data.lens = 50
    cam_obj = bpy.data.objects.new("StudioCamera", cam_data)
    bpy.context.collection.objects.link(cam_obj)

    cx = camera_dist * math.sin(camera_rot[2]) * math.sin(camera_rot[0])
    cy = -camera_dist * math.cos(camera_rot[2]) * math.sin(camera_rot[0])
    cz = camera_dist * math.cos(camera_rot[0])
    cam_obj.location = (cx, cy, cz)
    cam_obj.rotation_euler = camera_rot
    scene.camera = cam_obj

    # 1. Key Light (Principal - 45° superior direita, suave)
    l1_data = bpy.data.lights.new("KeyLight", type='AREA')
    l1_data.energy = 500.0
    l1_data.size = 3.0
    l1_obj = bpy.data.objects.new("KeyLight", l1_data)
    bpy.context.collection.objects.link(l1_obj)
    l1_obj.location = (4.0, -4.0, 5.0)
    l1_obj.rotation_euler = (0.8, 0.2, 0.6)

    # 2. Fill Light (Preenchimento - oposta, tom frio azulado)
    l2_data = bpy.data.lights.new("FillLight", type='AREA')
    l2_data.energy = 220.0
    l2_data.size = 4.0
    l2_data.color = (0.8, 0.9, 1.0)
    l2_obj = bpy.data.objects.new("FillLight", l2_data)
    bpy.context.collection.objects.link(l2_obj)
    l2_obj.location = (-4.5, -2.5, 3.5)
    l2_obj.rotation_euler = (1.1, -0.3, -0.9)

    # 3. Rim Light (Luz de contorno traseira - Laranja SENAI sutil)
    l3_data = bpy.data.lights.new("RimLight", type='SPOT')
    l3_data.energy = 450.0
    l3_data.spot_size = math.radians(60)
    l3_data.color = (1.0, 0.45, 0.15)
    l3_obj = bpy.data.objects.new("RimLight", l3_data)
    bpy.context.collection.objects.link(l3_obj)
    l3_obj.location = (-2.0, 4.0, 4.0)
    l3_obj.rotation_euler = (-0.9, 0.4, 2.6)

    return cam_obj


def make_material(name, color, roughness=0.25, metallic=0.0, transmission=0.0, alpha=1.0):
    """Cria material PBR com sombreador Principled BSDF."""
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        if "Base Color" in bsdf.inputs:
            bsdf.inputs["Base Color"].default_value = color
        if "Roughness" in bsdf.inputs:
            bsdf.inputs["Roughness"].default_value = roughness
        if "Metallic" in bsdf.inputs:
            bsdf.inputs["Metallic"].default_value = metallic
        if alpha < 1.0 and "Alpha" in bsdf.inputs:
            bsdf.inputs["Alpha"].default_value = alpha
            try:
                mat.blend_method = 'BLEND'
            except Exception:
                pass
    return mat


# ---------------------------------------------------------------- Geradores de Modelos 3D
def build_regular_prism(sides=6, radius=1.6, height=3.0, bevel=0.03):
    """Cria um prisma regular de n lados com chanfro (bevel) suave nas arestas."""
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=sides,
        radius=radius,
        depth=height,
        end_fill_type='NGON',
        location=(0, 0, 0)
    )
    obj = bpy.context.active_object
    obj.name = f"Prisma_{sides}_Lados"

    # Material do corpo (Azul SENAI acetinado)
    mat_corpo = make_material(f"Mat_Corpo_{sides}", COLOR_SENAI_BLUE, roughness=0.28)
    obj.data.materials.append(mat_corpo)

    # Material de destaque para a base superior (Laranja SENAI)
    mat_topo = make_material(f"Mat_Topo_{sides}", COLOR_SENAI_ORANGE, roughness=0.22)
    obj.data.materials.append(mat_topo)

    # Aplica o material de topo na face superior
    mesh = obj.data
    for poly in mesh.polygons:
        if poly.normal.z > 0.8:
            poly.material_index = 1

    # Modificador Bevel para realce de arestas com reflexo de luz de estúdio
    if bevel > 0:
        bev = obj.modifiers.new("Bevel", 'BEVEL')
        bev.width = bevel
        bev.segments = 2

    return obj


def build_exploded_prism(sides=5, radius=1.3, height=2.0, lift=0.9, push=0.45):
    """Cria uma vista explodida de um prisma: bases suspensas e faces laterais separadas."""
    container = []
    mat_base = make_material("MatExpl_Base", COLOR_SENAI_ORANGE, roughness=0.22)
    mat_face = make_material("MatExpl_Face", COLOR_SENAI_BLUE, roughness=0.28)

    angles = [2 * math.pi * i / sides for i in range(sides)]
    
    # Base Superior (elevada por +lift)
    verts_top = [(radius * math.cos(a), radius * math.sin(a), height/2 + lift) for a in angles]
    mesh_top = bpy.data.meshes.new("Exploded_TopBase")
    mesh_top.from_pydata(verts_top, [], [[i for i in range(sides)]])
    obj_top = bpy.data.objects.new("Exploded_TopBase", mesh_top)
    bpy.context.collection.objects.link(obj_top)
    obj_top.data.materials.append(mat_base)
    container.append(obj_top)

    # Base Inferior (rebaixada por -lift)
    verts_bot = [(radius * math.cos(a), radius * math.sin(a), -height/2 - lift) for a in angles]
    mesh_bot = bpy.data.meshes.new("Exploded_BotBase")
    mesh_bot.from_pydata(verts_bot, [], [[i for i in range(sides)][::-1]])
    obj_bot = bpy.data.objects.new("Exploded_BotBase", mesh_bot)
    bpy.context.collection.objects.link(obj_bot)
    obj_bot.data.materials.append(mat_base)
    container.append(obj_bot)

    # Faces Laterais (deslocadas para fora por +push na direção normal)
    for i in range(sides):
        nxt = (i + 1) % sides
        mid_angle = (angles[i] + angles[nxt]) / 2
        px = push * math.cos(mid_angle)
        py = push * math.sin(mid_angle)

        v1 = (radius * math.cos(angles[i]) + px, radius * math.sin(angles[i]) + py, -height/2)
        v2 = (radius * math.cos(angles[nxt]) + px, radius * math.sin(angles[nxt]) + py, -height/2)
        v3 = (radius * math.cos(angles[nxt]) + px, radius * math.sin(angles[nxt]) + py, height/2)
        v4 = (radius * math.cos(angles[i]) + px, radius * math.sin(angles[i]) + py, height/2)

        m = bpy.data.meshes.new(f"Exploded_Face_{i+1}")
        m.from_pydata([v1, v2, v3, v4], [], [[0, 1, 2, 3]])
        o = bpy.data.objects.new(f"Exploded_Face_{i+1}", m)
        bpy.context.collection.objects.link(o)
        o.data.materials.append(mat_face)
        container.append(o)

    return container


def build_aquarium_reservoir(length=3.0, width=1.8, height=2.0, water_fraction=0.70):
    """Cria um reservatório / aquário com água volumétrica translúcida e bordas reforçadas."""
    # Bloco de água interno
    wh = height * water_fraction
    w_z = -height/2 + wh/2
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, w_z))
    water = bpy.context.active_object
    water.name = "Volume_Agua"
    water.scale = (length, width, wh)

    mat_water = make_material("Mat_Agua", (0.05, 0.45, 0.95, 1.0), roughness=0.15, alpha=0.82)
    water.data.materials.append(mat_water)

    # Borda/armação do aquário (wireframe/edges)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0))
    frame = bpy.context.active_object
    frame.name = "Aquario_Armacao"
    frame.scale = (length, width, height)
    
    mat_frame = make_material("Mat_Armacao", COLOR_SENAI_BLUE, roughness=0.3)
    frame.data.materials.append(mat_frame)
    
    # Aplica Wireframe modifier na armação para dar contorno transparente
    wf = frame.modifiers.new("Wireframe", 'WIREFRAME')
    wf.thickness = 0.05

    return [frame, water]


# ---------------------------------------------------------------- Funções de Renderização
def render_blender_to_image(scene_builder_fn, output_path: str | Path, resolution=(1600, 1000), **kwargs) -> Path:
    """Executa a montagem e renderiza a cena em imagem estática de altíssima definição (PNG com transparência)."""
    output_path = Path(output_path).resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    clear_scene()
    setup_studio(transparent=True)
    scene_builder_fn(**kwargs)

    scene = bpy.context.scene
    scene.render.image_settings.file_format = 'PNG'
    scene.render.filepath = str(output_path)
    scene.render.resolution_x = resolution[0]
    scene.render.resolution_y = resolution[1]
    scene.render.resolution_percentage = 100

    bpy.ops.render.render(write_still=True)
    return output_path


def render_blender_turntable(scene_builder_fn, output_path: str | Path, frames=24, fps=12, resolution=(800, 600), **kwargs) -> Path:
    """Renderiza uma rotação 360° em estúdio e compila em GIF animado pronto para slides."""
    output_path = Path(output_path).resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    clear_scene()
    cam = setup_studio(transparent=True)
    scene_builder_fn(**kwargs)

    tmp_dir = output_path.parent / f".tmp_{output_path.stem}"
    tmp_dir.mkdir(parents=True, exist_ok=True)

    scene = bpy.context.scene
    scene.render.image_settings.file_format = 'PNG'
    scene.render.resolution_x = resolution[0]
    scene.render.resolution_y = resolution[1]

    # Rotação em torno do eixo Z da câmera
    dist = 13.5
    elev = 1.10
    frame_files = []

    for f in range(frames):
        theta = 0.785 + 2 * math.pi * f / frames
        cx = dist * math.sin(theta) * math.sin(elev)
        cy = -dist * math.cos(theta) * math.sin(elev)
        cz = dist * math.cos(elev)
        cam.location = (cx, cy, cz)
        cam.rotation_euler = (elev, 0, theta)

        frame_path = tmp_dir / f"frame_{f:03d}.png"
        scene.render.filepath = str(frame_path)
        bpy.ops.render.render(write_still=True)
        frame_files.append(frame_path)

    # Converte os frames para GIF usando ffmpeg com subprocess
    import subprocess
    ffmpeg_exe = shutil.which("ffmpeg") or imageio_ffmpeg.get_ffmpeg_exe()
    pattern = str(tmp_dir / "frame_%03d.png")
    args = [
        str(ffmpeg_exe), "-y", "-r", str(fps), "-i", pattern,
        "-vf", "split[s0][s1];[s0]palettegen=reserve_transparent=on[p];[s1][p]paletteuse=alpha_threshold=128",
        str(output_path)
    ]
    subprocess.run(args, check=True)

    # Limpeza dos frames temporários
    shutil.rmtree(tmp_dir, ignore_errors=True)
    return output_path


if __name__ == "__main__":
    out_dir = Path(__file__).resolve().parent.parent / "assets" / "motion_renders"
    out_dir.mkdir(parents=True, exist_ok=True)

    print("Renderizando Prisma Hexagonal 3D via Blender...")
    p1 = render_blender_to_image(lambda: build_regular_prism(sides=6, radius=1.7, height=3.0), out_dir / "blender_prisma_hex.png")
    print(f"OK: {p1}")

    print("Renderizando Vista Explodida 3D via Blender...")
    p2 = render_blender_to_image(lambda: build_exploded_prism(sides=5, radius=1.6, height=2.5, lift=1.1, push=0.6), out_dir / "blender_vista_explodida.png")
    print(f"OK: {p2}")

    print("Renderizando Reservatório com Água via Blender...")
    p3 = render_blender_to_image(lambda: build_aquarium_reservoir(length=3.2, width=2.0, height=2.2, water_fraction=0.75), out_dir / "blender_reservatorio_agua.png")
    print(f"OK: {p3}")
