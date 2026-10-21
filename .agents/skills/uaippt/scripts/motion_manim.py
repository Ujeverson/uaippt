"""motion_manim.py — Criação de figuras e animações matemáticas em Motion Design com Manim.
Alinhado à identidade visual SENAI (paleta oficial, tipografia e enquadramento para slides 16:9).
"""
import os
import sys
from pathlib import Path

# Garante que o ffmpeg instalado em Scripts seja encontrado pelo Manim
import shutil
import imageio_ffmpeg
scripts_dir = os.path.dirname(shutil.which("python") or "")
if scripts_dir and scripts_dir not in os.environ.get("PATH", ""):
    os.environ["PATH"] = scripts_dir + os.pathsep + os.environ.get("PATH", "")

from manim import *

# ---------------------------------------------------------------- Cores SENAI para Manim
SENAI_BLUE = ManimColor("#0E4194")
SENAI_ORANGE = ManimColor("#E8490F")
SENAI_PETROL = ManimColor("#074982")
SENAI_CYAN = ManimColor("#4FB3D9")
SENAI_LIGHT_BLUE = ManimColor("#D0E1F9")
SENAI_DARK_BG = ManimColor("#0E2841")
SENAI_TEXT = ManimColor("#262626")


class SenaiTheme:
    """Configuração de tema e resolução padrão para apresentações 16:9."""
    @staticmethod
    def apply(dark=False, quality="high"):
        config.pixel_width = 1920
        config.pixel_height = 1080
        config.frame_width = 14.22
        config.frame_height = 8.0
        config.background_color = SENAI_DARK_BG if dark else WHITE
        if quality == "low":
            config.pixel_width, config.pixel_height = 854, 480
        elif quality == "medium":
            config.pixel_width, config.pixel_height = 1280, 720


# ---------------------------------------------------------------- Cenas Educacionais Prontas
class PrismaPlanificacaoScene(Scene):
    """Animação de motion design: planificação de um prisma triangular reto.
    Mostra o sólido desdobrando suas 3 faces laterais e as 2 bases com marcadores.
    """
    def construct(self):
        SenaiTheme.apply(dark=False)
        self.camera.background_color = WHITE

        # Título da animação
        titulo = Text("Planificação do Prisma Triangular Reto", font="Segoe UI", weight=BOLD, color=SENAI_BLUE)
        titulo.scale(0.8).to_edge(UP, buff=0.5)
        self.play(Write(titulo), run_time=0.8)

        # Retângulo central da lateral desdobrada
        # 3 faces de largura 2.2 e altura 3.2
        w, h = 2.2, 3.2
        face1 = Rectangle(width=w, height=h, color=SENAI_BLUE, fill_color=SENAI_LIGHT_BLUE, fill_opacity=0.6)
        face2 = Rectangle(width=w, height=h, color=SENAI_BLUE, fill_color=SENAI_LIGHT_BLUE, fill_opacity=0.8)
        face3 = Rectangle(width=w, height=h, color=SENAI_BLUE, fill_color=SENAI_LIGHT_BLUE, fill_opacity=0.6)
        
        face1.move_to(LEFT * w)
        face2.move_to(ORIGIN)
        face3.move_to(RIGHT * w)

        lbl1 = Text("Face 1", font="Segoe UI", color=SENAI_PETROL).scale(0.5).move_to(face1.get_center())
        lbl2 = Text("Face 2", font="Segoe UI", color=SENAI_PETROL).scale(0.5).move_to(face2.get_center())
        lbl3 = Text("Face 3", font="Segoe UI", color=SENAI_PETROL).scale(0.5).move_to(face3.get_center())

        faces = VGroup(face1, face2, face3, lbl1, lbl2, lbl3)

        # Bases triangulares (superior e inferior conectadas à Face 2)
        top_tri = Polygon(
            [-w/2, h/2, 0],
            [w/2, h/2, 0],
            [0, h/2 + 1.6, 0],
            color=SENAI_ORANGE, fill_color=SENAI_ORANGE, fill_opacity=0.35, stroke_width=3
        )
        lbl_top = Text("Base Superior (Ab)", font="Segoe UI", color=SENAI_ORANGE).scale(0.45).move_to([0, h/2 + 0.65, 0])

        bot_tri = Polygon(
            [-w/2, -h/2, 0],
            [w/2, -h/2, 0],
            [0, -h/2 - 1.5, 0],
            color=SENAI_ORANGE, fill_color=SENAI_ORANGE, fill_opacity=0.35, stroke_width=3
        )
        lbl_bot = Text("Base Inferior (Ab)", font="Segoe UI", color=SENAI_ORANGE).scale(0.45).move_to([0, -h/2 - 0.55, 0])

        # Animação de expansão (Motion Design)
        self.play(FadeIn(face2), Write(lbl2), run_time=0.6)
        self.play(
            GrowFromEdge(face1, RIGHT), Write(lbl1),
            GrowFromEdge(face3, LEFT), Write(lbl3),
            run_time=0.8
        )
        self.play(
            GrowFromEdge(top_tri, DOWN), Write(lbl_top),
            GrowFromEdge(bot_tri, UP), Write(lbl_bot),
            run_time=0.8
        )

        # Cotas e fórmulas
        cota_h = DoubleArrow(start=[w*1.5 + 0.3, -h/2, 0], end=[w*1.5 + 0.3, h/2, 0], color=SENAI_ORANGE, buff=0)
        lbl_h = Text("Altura (h)", font="Segoe UI", color=SENAI_ORANGE).scale(0.5).next_to(cota_h, RIGHT)

        cota_2p = DoubleArrow(start=[-w*1.5, -h/2 - 0.85, 0], end=[w*1.5, -h/2 - 0.85, 0], color=SENAI_BLUE, buff=0)
        lbl_2p = Text("Perímetro da Base (2p = a + b + c)", font="Segoe UI", color=SENAI_BLUE).scale(0.42).next_to(cota_2p, DOWN, buff=0.1)

        eq_total = Text("Área Total: At = Al + 2·Ab", font="Segoe UI", weight=BOLD, color=SENAI_BLUE).scale(0.65)
        eq_total.to_edge(DOWN, buff=0.2)

        self.play(Create(cota_h), Write(lbl_h), Create(cota_2p), Write(lbl_2p), run_time=0.8)
        self.play(Write(eq_total), run_time=0.6)
        self.wait(1.5)


class VolumeExtrusaoScene(Scene):
    """Animação conceitual: A base Ab desliza pela altura h gerando o Volume V = Ab · h."""
    def construct(self):
        SenaiTheme.apply(dark=False)
        self.camera.background_color = WHITE

        titulo = Text("Princípio do Volume: V = Ab · h", font="Segoe UI", weight=BOLD, color=SENAI_BLUE).scale(0.8).to_edge(UP, buff=0.5)
        self.add(titulo)

        # Polígono da base (hexágono ou retângulo)
        base = RegularPolygon(n=6, radius=1.5, color=SENAI_BLUE, fill_color=SENAI_LIGHT_BLUE, fill_opacity=0.7)
        base.move_to(DOWN * 1.6 + LEFT * 2)

        lbl_ab = Text("Área da Base (Ab)", font="Segoe UI", weight=BOLD, color=SENAI_BLUE).scale(0.5).next_to(base, DOWN, buff=0.2)

        self.play(FadeIn(base), Write(lbl_ab), run_time=0.6)

        # Fatias empilhadas
        camadas = VGroup()
        for i in range(1, 8):
            copia = base.copy().shift(UP * (i * 0.45))
            copia.set_fill(color=interpolate_color(SENAI_LIGHT_BLUE, SENAI_BLUE, i / 8), opacity=0.75)
            camadas.add(copia)

        self.play(
            LaggedStart(*[FadeIn(c, shift=UP*0.2) for c in camadas], lag_ratio=0.12),
            run_time=2.0
        )

        # Seta de altura
        cota_h = DoubleArrow(start=base.get_right() + RIGHT*0.4, end=camadas[-1].get_right() + RIGHT*0.4, color=SENAI_ORANGE)
        lbl_h = Text("Altura (h)", font="Segoe UI", weight=BOLD, color=SENAI_ORANGE).scale(0.55).next_to(cota_h, RIGHT)

        resumo = VGroup(
            Text("Cada camada adiciona", font="Segoe UI", color=SENAI_TEXT).scale(0.5),
            Text("uma fatia de volume Ab.", font="Segoe UI", color=SENAI_TEXT).scale(0.5),
            Text("Total = Ab × h", font="Segoe UI", weight=BOLD, color=SENAI_ORANGE).scale(0.7)
        ).arrange(DOWN, aligned_edge=LEFT).next_to(lbl_h, RIGHT, buff=0.8)

        self.play(Create(cota_h), Write(lbl_h), Write(resumo), run_time=1.0)
        self.wait(1.5)


# ---------------------------------------------------------------- Funções Utilitárias de Render
def render_manim_to_image(scene_class, output_path: str | Path, quality="high", dark=False) -> Path:
    """Renderiza o último frame (keyframe hero) da cena Manim diretamente em PNG de alta resolução."""
    output_path = Path(output_path).resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    config.media_dir = str(output_path.parent / ".manim_cache")
    config.format = "png"
    config.quality = "high_quality" if quality == "high" else "low_quality"
    config.frame_rate = 30
    SenaiTheme.apply(dark=dark, quality=quality)

    scene = scene_class()
    scene.render()

    # O manim gera a imagem em config.media_dir / images / ...
    img_dir = Path(config.media_dir) / "images"
    candidates = list(img_dir.rglob("*.png"))
    if candidates:
        latest = max(candidates, key=os.path.getmtime)
        shutil.copyfile(latest, output_path)
    else:
        raise FileNotFoundError("Não foi possível localizar o frame gerado pelo Manim.")

    return output_path


def render_manim_to_gif(scene_class, output_path: str | Path, quality="medium") -> Path:
    """Renderiza a cena completa em GIF animado (looping) pronto para slides do PowerPoint."""
    output_path = Path(output_path).resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    config.media_dir = str(output_path.parent / ".manim_cache")
    config.format = "gif"
    config.quality = "medium_quality" if quality == "medium" else "low_quality"
    SenaiTheme.apply(dark=False, quality=quality)

    scene = scene_class()
    scene.render()

    gif_dir = Path(config.media_dir)
    candidates = list(gif_dir.rglob("*.gif"))
    if candidates:
        latest = max(candidates, key=os.path.getmtime)
        shutil.copyfile(latest, output_path)
    else:
        # Se gerou MP4, converte para GIF com ffmpeg
        mp4_candidates = list(gif_dir.rglob("*.mp4"))
        if mp4_candidates:
            import subprocess
            latest_mp4 = max(mp4_candidates, key=os.path.getmtime)
            ffmpeg_exe = shutil.which("ffmpeg") or imageio_ffmpeg.get_ffmpeg_exe()
            args = [
                str(ffmpeg_exe), "-y", "-i", str(latest_mp4),
                "-vf", "fps=15,scale=800:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse",
                str(output_path)
            ]
            subprocess.run(args, check=True)
        else:
            raise FileNotFoundError("Não foi possível gerar o GIF pelo Manim.")

    return output_path


if __name__ == "__main__":
    out_dir = Path(__file__).resolve().parent.parent / "assets" / "motion_renders"
    out_dir.mkdir(parents=True, exist_ok=True)
    
    print("Renderizando Planificação via Manim...")
    p1 = render_manim_to_image(PrismaPlanificacaoScene, out_dir / "manim_planificacao.png")
    print(f"OK: {p1}")

    print("Renderizando Volume Extrusão via Manim...")
    p2 = render_manim_to_image(VolumeExtrusaoScene, out_dir / "manim_volume_extrusao.png")
    print(f"OK: {p2}")
