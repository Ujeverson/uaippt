"""Gera ilustrações técnicas com alta qualidade e padrão SENAI para a aula de Prismas.
Cores: Azul SENAI (#0E4194), Laranja SENAI (#E8490F), Ciano (#4FB3D9), Cinza (#575656).
Fundo transparente, tipografia legível, margens amplas sem cortes.
"""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, FancyArrowPatch, Rectangle
import matplotlib.patheffects as pe

OUT_DIR = Path(__file__).resolve().parent / "assets_prismas"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Paleta SENAI
AZUL = "#0E4194"
LARANJA = "#E8490F"
CIANO = "#4FB3D9"
CINZA = "#575656"
TEXTO = "#1A1A1A"
AZUL_CLARO = "#D0E1F9"
LARANJA_CLARO = "#FDE8E0"


def make_fig_elementos():
    """Figura 1: Elementos Fundamentais do Prisma (Perspectiva 3D com cotas)."""
    fig, ax = plt.subplots(figsize=(6, 6), dpi=300)
    ax.set_aspect("equal")
    ax.axis("off")

    # Coordenadas 2.5D de um prisma hexagonal reto
    # Base inferior: 6 vértices
    angles = np.linspace(0, 2 * np.pi, 7)[:-1]
    rx, ry = 2.2, 0.9  # elipse da perspectiva
    cx, cy_inf, cy_sup = 3.0, 1.8, 4.3

    pts_inf = [(cx + rx * np.cos(a), cy_inf + ry * np.sin(a)) for a in angles]
    pts_sup = [(cx + rx * np.cos(a), cy_sup + ry * np.sin(a)) for a in angles]

    # Ordenar vértices da base para plotar faces de trás (tracejadas) e da frente (sólidas)
    # y menor fica na frente
    # Faces traseiras (arestas ocultas tracejadas)
    # Arestas da base inferior traseira
    for i in [1, 2]:
        p1, p2 = pts_inf[i], pts_inf[(i + 1) % 6]
        ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color=AZUL, lw=1.5, ls="--", alpha=0.5)
    # Arestas verticais traseiras
    for i in [1, 2]:
        ax.plot([pts_inf[i][0], pts_sup[i][0]], [pts_inf[i][1], pts_sup[i][1]], color=AZUL, lw=1.5, ls="--", alpha=0.5)

    # Base inferior - preenchimento
    poly_inf = Polygon(pts_inf, closed=True, facecolor=AZUL_CLARO, edgecolor="none", alpha=0.4)
    ax.add_patch(poly_inf)

    # Faces laterais visíveis
    for i in [3, 4, 5, 0]:
        ni = (i + 1) % 6
        face_pts = [pts_inf[i], pts_inf[ni], pts_sup[ni], pts_sup[i]]
        poly_face = Polygon(face_pts, closed=True, facecolor=AZUL_CLARO, edgecolor=AZUL, lw=2, alpha=0.35)
        ax.add_patch(poly_face)

    # Arestas da base inferior frontal
    for i in [3, 4, 5, 0]:
        p1, p2 = pts_inf[i], pts_inf[(i + 1) % 6]
        ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color=AZUL, lw=2.2)

    # Arestas verticais frontais
    for i in [3, 4, 5, 0]:
        ax.plot([pts_inf[i][0], pts_sup[i][0]], [pts_inf[i][1], pts_sup[i][1]], color=AZUL, lw=2.2)

    # Base superior - preenchimento e contorno completo
    poly_sup = Polygon(pts_sup, closed=True, facecolor=LARANJA_CLARO, edgecolor=LARANJA, lw=2.4, alpha=0.7)
    ax.add_patch(poly_sup)

    # Cota de Altura (h) à esquerda
    hx = 0.5
    ax.plot([hx, hx], [cy_inf, cy_sup], color=LARANJA, lw=2.2, ls="--")
    ax.plot([hx - 0.15, hx + 0.15], [cy_inf, cy_inf], color=LARANJA, lw=2.0)
    ax.plot([hx - 0.15, hx + 0.15], [cy_sup, cy_sup], color=LARANJA, lw=2.0)
    ax.text(hx - 0.25, (cy_inf + cy_sup) / 2, "Altura (h)", color=LARANJA, fontsize=12,
            fontweight="bold", va="center", ha="right")

    # Textos de elementos com setas apontadoras
    # Base Superior
    ax.annotate("Base Superior", xy=(cx, cy_sup + 0.4), xytext=(cx, 5.7),
                ha="center", fontsize=12, fontweight="bold", color=LARANJA,
                arrowprops=dict(arrowstyle="->", color=LARANJA, lw=1.5))

    # Base Inferior
    ax.annotate("Base Inferior", xy=(cx, cy_inf - 0.6), xytext=(cx, 0.4),
                ha="center", fontsize=12, fontweight="bold", color=AZUL,
                arrowprops=dict(arrowstyle="->", color=AZUL, lw=1.5))

    # Face Lateral
    ax.annotate("Face Lateral\n(Retângulo)", xy=(pts_sup[4][0] + 0.6, (cy_inf + cy_sup) / 2), xytext=(5.3, 3.2),
                ha="left", va="center", fontsize=11, fontweight="bold", color=AZUL,
                arrowprops=dict(arrowstyle="->", color=AZUL, lw=1.5))

    # Aresta da Base
    ax.annotate("Aresta da Base", xy=(pts_sup[5][0], pts_sup[5][1]), xytext=(5.1, 4.8),
                ha="left", va="center", fontsize=10, color=CINZA,
                arrowprops=dict(arrowstyle="->", color=CINZA, lw=1.2))

    # Vértice
    ax.plot(pts_sup[3][0], pts_sup[3][1], marker="o", color=LARANJA, markersize=6)
    ax.annotate("Vértice", xy=(pts_sup[3][0], pts_sup[3][1]), xytext=(pts_sup[3][0] - 0.8, pts_sup[3][1] + 0.5),
                ha="center", fontsize=10, color=CINZA,
                arrowprops=dict(arrowstyle="->", color=CINZA, lw=1.2))

    ax.set_xlim(-0.8, 6.8)
    ax.set_ylim(0.0, 6.2)
    plt.tight_layout()
    out = OUT_DIR / "elementos_prisma.png"
    plt.savefig(out, transparent=True, bbox_inches="tight", dpi=300)
    plt.close()
    print(f"Salvo: {out}")


def make_fig_planificacao():
    """Figura 2: Planificação de um Prisma Triangular Reto."""
    fig, ax = plt.subplots(figsize=(6.5, 5.5), dpi=300)
    ax.set_aspect("equal")
    ax.axis("off")

    # Três retângulos centrais (faces laterais)
    # Larguras das 3 faces: a=1.6, b=1.8, c=1.6. Altura: h=2.5
    w1, w2, w3 = 1.6, 1.8, 1.6
    total_w = w1 + w2 + w3
    h = 2.4
    x0, y0 = 0.8, 1.6

    # Face 1
    f1 = Rectangle((x0, y0), w1, h, facecolor=AZUL_CLARO, edgecolor=AZUL, lw=2, alpha=0.5)
    f2 = Rectangle((x0 + w1, y0), w2, h, facecolor=AZUL_CLARO, edgecolor=AZUL, lw=2, alpha=0.7)
    f3 = Rectangle((x0 + w1 + w2, y0), w3, h, facecolor=AZUL_CLARO, edgecolor=AZUL, lw=2, alpha=0.5)
    for f in [f1, f2, f3]:
        ax.add_patch(f)

    # Rótulos das faces
    ax.text(x0 + w1 / 2, y0 + h / 2, "Face 1\n($a \\times h$)", ha="center", va="center", fontsize=9, color=AZUL)
    ax.text(x0 + w1 + w2 / 2, y0 + h / 2, "Face 2\n($b \\times h$)", ha="center", va="center", fontsize=10, fontweight="bold", color=AZUL)
    ax.text(x0 + w1 + w2 + w3 / 2, y0 + h / 2, "Face 3\n($c \\times h$)", ha="center", va="center", fontsize=9, color=AZUL)

    # Base Superior (triângulo acoplado à Face 2)
    bx0, by0 = x0 + w1, y0 + h
    tri_sup = Polygon([(bx0, by0), (bx0 + w2, by0), (bx0 + w2 / 2, by0 + 1.2)],
                      closed=True, facecolor=LARANJA_CLARO, edgecolor=LARANJA, lw=2.2, alpha=0.8)
    ax.add_patch(tri_sup)
    ax.text(bx0 + w2 / 2, by0 + 0.45, "Base Superior ($A_b$)", ha="center", va="center",
            fontsize=9, fontweight="bold", color=LARANJA)

    # Base Inferior (triângulo acoplado à Face 2)
    by_inf = y0
    tri_inf = Polygon([(bx0, by_inf), (bx0 + w2, by_inf), (bx0 + w2 / 2, by_inf - 1.2)],
                      closed=True, facecolor=LARANJA_CLARO, edgecolor=LARANJA, lw=2.2, alpha=0.8)
    ax.add_patch(tri_inf)
    ax.text(bx0 + w2 / 2, by_inf - 0.45, "Base Inferior ($A_b$)", ha="center", va="center",
            fontsize=9, fontweight="bold", color=LARANJA)

    # Cota de Altura (h) à direita
    cx = x0 + total_w + 0.35
    arrow_h = FancyArrowPatch((cx, y0), (cx, y0 + h), arrowstyle="<->",
                             mutation_scale=15, color=LARANJA, lw=2)
    ax.add_patch(arrow_h)
    ax.text(cx + 0.2, y0 + h / 2, "Altura ($h$)", color=LARANJA, fontsize=11,
            fontweight="bold", va="center", ha="left")

    # Cota do Perímetro da Base (2p) abaixo
    cy = y0 - 1.55
    arrow_p = FancyArrowPatch((x0, cy), (x0 + total_w, cy), arrowstyle="<->",
                             mutation_scale=15, color=AZUL, lw=2)
    ax.add_patch(arrow_p)
    ax.text(x0 + total_w / 2, cy - 0.25, "Perímetro da Base ($2p = a + b + c$)",
            color=AZUL, fontsize=10, fontweight="bold", ha="center", va="top")

    # Fórmulas no topo com caixa de destaque
    ax.text(x0 + total_w / 2, by0 + 1.6, "Área Total: $A_t = A_l + 2 \\cdot A_b$",
            fontsize=12, fontweight="bold", color=AZUL, ha="center")
    ax.text(x0 + total_w / 2, by0 + 1.25, "Área Lateral: $A_l = (a + b + c) \\cdot h = 2p \\cdot h$",
            fontsize=10, color=CINZA, ha="center")

    ax.set_xlim(0.0, 7.2)
    ax.set_ylim(-0.6, 6.2)
    plt.tight_layout()
    out = OUT_DIR / "planificacao_prisma.png"
    plt.savefig(out, transparent=True, bbox_inches="tight", dpi=300)
    plt.close()
    print(f"Salvo: {out}")


def make_fig_paralelepipedo_cubo():
    """Figura 3: Paralelepípedo e Cubo com dimensões e fórmulas."""
    fig, ax = plt.subplots(figsize=(6.5, 4.5), dpi=300)
    ax.set_aspect("equal")
    ax.axis("off")

    def draw_box(x, y, w, h, d, face_col, edge_col, title, formula, dims):
        # Deslocamento isométrico: dx = d * 0.7, dy = d * 0.4
        dx, dy = d * 0.7, d * 0.4
        # Frente
        ax.add_patch(Rectangle((x, y), w, h, facecolor=face_col, edgecolor=edge_col, lw=2, alpha=0.4))
        # Topo
        top_pts = [(x, y + h), (x + w, y + h), (x + w + dx, y + h + dy), (x + dx, y + h + dy)]
        ax.add_patch(Polygon(top_pts, closed=True, facecolor=face_col, edgecolor=edge_col, lw=2, alpha=0.6))
        # Lado direito
        side_pts = [(x + w, y), (x + w + dx, y + dy), (x + w + dx, y + h + dy), (x + w, y + h)]
        ax.add_patch(Polygon(side_pts, closed=True, facecolor=face_col, edgecolor=edge_col, lw=2, alpha=0.5))

        # Título e Fórmula
        ax.text(x + (w + dx) / 2, y + h + dy + 0.65, title, ha="center", fontsize=11, fontweight="bold", color=AZUL)
        ax.text(x + (w + dx) / 2, y + h + dy + 0.3, formula, ha="center", fontsize=10, fontweight="bold", color=LARANJA)

        # Cotas
        # Comprimento
        ax.text(x + w / 2, y - 0.25, dims[0], ha="center", fontsize=10, color=AZUL, fontweight="bold")
        # Largura (profundidade)
        ax.text(x + w + dx / 2 + 0.15, y + dy / 2 - 0.1, dims[1], ha="left", fontsize=10, color=AZUL, fontweight="bold")
        # Altura
        ax.text(x - 0.25, y + h / 2, dims[2], ha="right", va="center", fontsize=10, color=LARANJA, fontweight="bold")

    # Paralelepípedo Reto-Retângulo
    draw_box(0.5, 0.6, 2.2, 1.6, 1.2, AZUL_CLARO, AZUL,
             "Paralelepípedo", "$V = a \\cdot b \\cdot c$", ["$a$ (comp.)", "$b$ (larg.)", "$c$ (alt.)"])

    # Cubo (Hexaedro Regular)
    draw_box(4.0, 0.6, 1.8, 1.8, 1.2, LARANJA_CLARO, LARANJA,
             "Cubo Regular", "$V = a^3$", ["$a$", "$a$", "$a$"])

    ax.set_xlim(0.0, 7.2)
    ax.set_ylim(0.0, 4.4)
    plt.tight_layout()
    out = OUT_DIR / "paralelepipedo_cubo.png"
    plt.savefig(out, transparent=True, bbox_inches="tight", dpi=300)
    plt.close()
    print(f"Salvo: {out}")


def make_fig_volume_capacidade():
    """Figura 4: Princípio do Volume (Fatias empilhadas) e Equivalência de Litros."""
    fig, ax = plt.subplots(figsize=(6.5, 4.8), dpi=300)
    ax.set_aspect("equal")
    ax.axis("off")

    # Lado esquerdo: Pilha de fatias
    x0, y0, w, h_fatia = 0.5, 0.8, 2.5, 0.45
    n_fatias = 5
    for i in range(n_fatias):
        yi = y0 + i * (h_fatia + 0.12)
        # Retângulo com perspectiva sutil
        ax.add_patch(Rectangle((x0, yi), w, h_fatia, facecolor=AZUL_CLARO, edgecolor=AZUL, lw=1.8, alpha=0.7))
        ax.text(x0 + w / 2, yi + h_fatia / 2, f"Camada {i+1} ($A_b$)", ha="center", va="center", fontsize=8, color=AZUL)

    # Cota de altura da pilha
    total_h = n_fatias * (h_fatia + 0.12) - 0.12
    arrow = FancyArrowPatch((x0 + w + 0.3, y0), (x0 + w + 0.3, y0 + total_h),
                            arrowstyle="<->", mutation_scale=14, color=LARANJA, lw=2)
    ax.add_patch(arrow)
    ax.text(x0 + w + 0.45, y0 + total_h / 2, "Altura ($h$)\n$n$ camadas",
            va="center", ha="left", fontsize=9, fontweight="bold", color=LARANJA)

    # Título do princípio
    ax.text(x0 + w / 2, y0 + total_h + 0.55, "Princípio do Volume:\n$V = A_b \\cdot h$",
            ha="center", fontsize=11, fontweight="bold", color=AZUL)

    # Lado direito: Quadro de relações com litros
    qx = 4.2
    ax.text(qx + 1.2, 3.8, "Relações Fundamentais", ha="center", fontsize=11, fontweight="bold", color=AZUL)

    items = [
        ("$1\\text{ m}^3 = 1.000\\text{ Litros}$", "Caixas d'água, piscinas", LARANJA),
        ("$1\\text{ dm}^3 = 1\\text{ Litro}$", "Garrafas, caixas de leite", AZUL),
        ("$1\\text{ cm}^3 = 1\\text{ mL}$", "Seringas, remédios, doses", CINZA),
    ]

    for idx, (formula, desc, col) in enumerate(items):
        py = 3.0 - idx * 0.95
        # Caixa de fundo sutil
        ax.add_patch(Rectangle((qx, py - 0.2), 2.5, 0.75, facecolor="#F4F6F9", edgecolor=col, lw=1.5))
        ax.text(qx + 0.15, py + 0.28, formula, fontsize=10, fontweight="bold", color=col)
        ax.text(qx + 0.15, py - 0.05, desc, fontsize=8, color=TEXTO)

    ax.set_xlim(0.0, 7.0)
    ax.set_ylim(0.2, 4.6)
    plt.tight_layout()
    out = OUT_DIR / "volume_capacidade.png"
    plt.savefig(out, transparent=True, bbox_inches="tight", dpi=300)
    plt.close()
    print(f"Salvo: {out}")


def make_fig_prisma_triangular():
    """Figura 5: Prisma Triangular Reto com base e altura destacadas."""
    fig, ax = plt.subplots(figsize=(6, 5), dpi=300)
    ax.set_aspect("equal")
    ax.axis("off")

    # Vértices 3D em projeção oblíqua
    # Base inferior: 3 vértices
    p1 = (1.2, 1.2)   # frontal esquerdo
    p2 = (3.8, 0.8)   # frontal direito
    p3 = (2.6, 2.2)   # traseiro (tracejado)

    h = 2.6
    p1_s = (p1[0], p1[1] + h)
    p2_s = (p2[0], p2[1] + h)
    p3_s = (p3[0], p3[1] + h)

    # Base inferior - preenchimento
    ax.add_patch(Polygon([p1, p2, p3], closed=True, facecolor=AZUL_CLARO, edgecolor="none", alpha=0.5))

    # Arestas traseiras tracejadas
    ax.plot([p1[0], p3[0]], [p1[1], p3[1]], color=AZUL, lw=1.6, ls="--")
    ax.plot([p2[0], p3[0]], [p2[1], p3[1]], color=AZUL, lw=1.6, ls="--")
    ax.plot([p3[0], p3_s[0]], [p3[1], p3_s[1]], color=AZUL, lw=1.6, ls="--")

    # Faces laterais visíveis
    ax.add_patch(Polygon([p1, p2, p2_s, p1_s], closed=True, facecolor=AZUL_CLARO, edgecolor=AZUL, lw=2.2, alpha=0.35))
    ax.add_patch(Polygon([p2, p3, p3_s, p2_s], closed=True, facecolor=AZUL_CLARO, edgecolor=AZUL, lw=1.8, alpha=0.2))

    # Arestas visíveis
    ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color=AZUL, lw=2.4)
    ax.plot([p1[0], p1_s[0]], [p1[1], p1_s[1]], color=AZUL, lw=2.4)
    ax.plot([p2[0], p2_s[0]], [p2[1], p2_s[1]], color=AZUL, lw=2.4)

    # Base superior
    ax.add_patch(Polygon([p1_s, p2_s, p3_s], closed=True, facecolor=LARANJA_CLARO, edgecolor=LARANJA, lw=2.4, alpha=0.8))

    # Cota de Altura (h)
    cx = p2[0] + 0.4
    arrow_h = FancyArrowPatch((cx, p2[1]), (cx, p2_s[1]), arrowstyle="<->",
                             mutation_scale=15, color=LARANJA, lw=2)
    ax.add_patch(arrow_h)
    ax.text(cx + 0.2, (p2[1] + p2_s[1]) / 2, "Altura ($h$)", color=LARANJA,
            fontsize=11, fontweight="bold", va="center")

    # Rótulo da Base triangular
    ax.annotate("Base Triangular ($A_b$)\n$A_b = \\frac{b \\cdot h_\\Delta}{2}$",
                xy=(2.5, 1.4), xytext=(2.5, 0.0),
                ha="center", fontsize=10, fontweight="bold", color=AZUL,
                arrowprops=dict(arrowstyle="->", color=AZUL, lw=1.5))

    # Fórmula do Volume no topo
    ax.text(2.5, 4.6, "Prisma Triangular Reto", ha="center", fontsize=12, fontweight="bold", color=AZUL)
    ax.text(2.5, 4.2, "$V = A_b \\cdot h = \\left(\\frac{b \\cdot h_\\Delta}{2}\\right) \\cdot h$",
            ha="center", fontsize=11, fontweight="bold", color=LARANJA)

    ax.set_xlim(0.4, 5.2)
    ax.set_ylim(-0.4, 5.0)
    plt.tight_layout()
    out = OUT_DIR / "prisma_triangular.png"
    plt.savefig(out, transparent=True, bbox_inches="tight", dpi=300)
    plt.close()
    print(f"Salvo: {out}")


if __name__ == "__main__":
    make_fig_elementos()
    make_fig_planificacao()
    make_fig_paralelepipedo_cubo()
    make_fig_volume_capacidade()
    make_fig_prisma_triangular()
    print("Todas as figuras foram geradas com sucesso!")
