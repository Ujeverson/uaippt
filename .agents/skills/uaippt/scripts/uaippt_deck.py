"""uaippt_deck — gera apresentações .pptx no padrão visual SENAI / Faculdade SENAI Fatesg.
Suporta Motion Design com Manim e Blender (bpy) e integração com AI Coding Agents.

Uso como biblioteca:
    import sys; sys.path.insert(0, r"<pasta-da-skill>/scripts")
    from uaippt_deck import UaipptDeck

    deck = UaipptDeck()
    deck.cover("Lógica de Programação", "Aula 1 — Algoritmos", course="Análise e Des. de Sistemas", professor="Prof. Msc. Ujeverson Tavares")
    deck.bullets("Objetivos da aula", ["Entender o que é um algoritmo", ("Exemplos do dia a dia", 1)])
    deck.save("aula1.pptx")

Uso via linha de comando (roteiro em JSON):
    python uaippt_deck.py roteiro.json saida.pptx

Dependências: python-pptx (obrigatória), pygments (opcional, colore código).
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Emu, Inches, Pt

SKILL_DIR = Path(__file__).resolve().parent.parent
TEMPLATE = SKILL_DIR / "assets" / "template.pptx"

# ---------------------------------------------------------------- paleta
AZUL = RGBColor(0x0E, 0x41, 0x94)        # azul SENAI
LARANJA = RGBColor(0xE8, 0x49, 0x0F)     # laranja SENAI
PETROLEO = RGBColor(0x07, 0x49, 0x82)    # linhas do banner
CIANO = RGBColor(0x4F, 0xB3, 0xD9)       # setas do banner
CINZA = RGBColor(0x57, 0x56, 0x56)       # cinza da logo
TEXTO = RGBColor(0x26, 0x26, 0x26)       # texto corrido
AZUL_CLARO = RGBColor(0xE8, 0xEE, 0xF7)  # fundo de caixas/linhas alternadas
CODE_BG = RGBColor(0x1E, 0x1E, 0x2E)
CODE_FG = RGBColor(0xE6, 0xE6, 0xE6)

DEFAULT_PROFESSOR = ""
DEFAULT_COURSE = "Faculdade SENAI Fatesg"

# ---------------------------------------------------------------- layouts (índices do template)
L_CAPA, L_CONTEUDO, L_SECAO, L_DUAS, L_COMPARACAO = 0, 1, 2, 3, 4
L_SO_TITULO, L_BRANCO, L_CONTEUDO_LEGENDA, L_IMAGEM_LEGENDA = 5, 6, 7, 8

# Área segura para formas livres (abaixo do título, acima da borda inferior)
AREA = dict(x=0.92, y=2.05, w=11.50, h=4.75)  # polegadas


# ---------------------------------------------------------------- utilidades de texto
def _norm_items(items):
    """Aceita 'texto', ('texto', nivel) ou ['texto', nivel]; devolve [(texto, nivel)]."""
    out = []
    for it in items or []:
        if isinstance(it, (list, tuple)):
            out.append((str(it[0]), int(it[1]) if len(it) > 1 else 0))
        else:
            out.append((str(it), 0))
    return out


def _fit_size(items, width_in, height_in, sizes=(28, 24, 22, 20, 18, 16, 14)):
    """Escolhe o maior tamanho de fonte (pt) cujo texto estimado cabe na caixa.

    Calibrado com renderizações reais do template (Aptos, entrelinha 90%,
    espaço antes do parágrafo 10 pt no nível 0 e 5 pt nos demais).
    """
    for size in sizes:
        total = 0.0
        for text, level in items:
            s = size - 2 * level
            char_w = s * 0.48 / 72          # largura média de caractere (Aptos)
            line_h = s * 1.1 / 72           # entrelinha 90%
            usable = width_in - 0.4 - 0.45 * level
            chars_per_line = max(8, int(usable / char_w))
            lines = max(1, math.ceil(len(text) / chars_per_line))
            total += lines * line_h + ((10 if level == 0 else 5) / 72)
        if total <= height_in - 0.2:
            return size
    return sizes[-1]


def _title_size(text, base=32):
    n = len(text)
    if n <= 40:
        return base
    if n <= 60:
        return base - 4
    return base - 8


def _fill_text(shape, items, size=None, color=TEXTO, bold_level0=False):
    tf = shape.text_frame
    tf.word_wrap = True
    items = _norm_items(items)
    if size is None:
        size = _fit_size(items, Emu(shape.width).inches, Emu(shape.height).inches)
    for i, (text, level) in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = text
        p.level = level
        for r in p.runs:
            r.font.size = Pt(size - 2 * level)
            r.font.color.rgb = color
            if bold_level0 and level == 0:
                r.font.bold = True
    return size


def _set_title(shape, text, base=32):
    shape.text = text
    for p in shape.text_frame.paragraphs:
        for r in p.runs:
            r.font.size = Pt(_title_size(text, base))


def _ph(slide, idx):
    for shape in slide.placeholders:
        if shape.placeholder_format.idx == idx:
            return shape
    raise KeyError(f"placeholder idx={idx} não existe neste layout")


def _remove_empty_placeholders(slide):
    for shape in list(slide.placeholders):
        if shape.has_text_frame and not shape.text_frame.text.strip():
            shape._element.getparent().remove(shape._element)


# ---------------------------------------------------------------- deck
class UaipptDeck:
    def __init__(self, template: str | Path = TEMPLATE, default_professor: str | None = None, default_course: str = DEFAULT_COURSE):
        self.prs = Presentation(str(template))
        self.default_professor = default_professor if default_professor is not None else DEFAULT_PROFESSOR
        self.default_course = default_course
        while len(self.prs.slides) > 0:           # template deve começar vazio
            rId = self.prs.slides._sldIdLst[0].rId
            self.prs.part.drop_rel(rId)
            del self.prs.slides._sldIdLst[0]

    # -------------------------------------------------- base
    def _new(self, layout_idx, notes=None):
        slide = self.prs.slides.add_slide(self.prs.slide_layouts[layout_idx])
        if notes:
            slide.notes_slide.notes_text_frame.text = notes
        return slide

    def _finish(self, slide):
        _remove_empty_placeholders(slide)
        return slide

    # -------------------------------------------------- tipos de slide
    def cover(self, title, subtitle="", course=None, professor=None, notes=None):
        """Capa: banner + título central + subtítulo (curso, professor preenchidos) + rodapé Fatesg."""
        s = self._new(L_CAPA, notes)
        _set_title(_ph(s, 0), title, base=44)

        c = self.default_course if course is None else course
        p_name = self.default_professor if professor is None else professor
        
        # Se o nome do(a) professor(a) não foi informado e estamos no terminal, pergunta interativamente
        if not p_name and sys.stdin and hasattr(sys.stdin, "isatty") and sys.stdin.isatty():
            try:
                p_resp = input("Nome do(a) Professor(a) para a capa (ou Enter para pular): ").strip()
                if p_resp:
                    p_name = p_resp
            except Exception:
                pass

        lines = []
        if subtitle:
            lines.append(subtitle)
        meta = []
        if c:
            meta.append(c)
        if p_name:
            meta.append(p_name)
        if meta:
            lines.append(" | ".join(meta))

        if lines:
            ph = _ph(s, 1)
            tf = ph.text_frame
            tf.word_wrap = True
            for i, line_text in enumerate(lines):
                p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
                p.text = line_text
                p.alignment = PP_ALIGN.CENTER
                for r in p.runs:
                    if len(lines) > 1 and i == 0:
                        r.font.size = Pt(22)
                        r.font.color.rgb = CINZA
                    elif len(lines) > 1 and i == 1:
                        r.font.size = Pt(18)
                        r.font.color.rgb = AZUL
                        r.font.bold = False
                    else:
                        r.font.size = Pt(22)
                        r.font.color.rgb = CINZA

        # filete laranja entre título e subtítulo
        bar = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(5.92), Inches(3.98), Inches(1.5), Inches(0.06))
        bar.fill.solid(); bar.fill.fore_color.rgb = LARANJA; bar.line.fill.background()
        return self._finish(s)

    def section(self, title, subtitle="", notes=None):
        """Divisória de seção/módulo."""
        s = self._new(L_SECAO, notes)
        _set_title(_ph(s, 0), title, base=48)
        if subtitle:
            _fill_text(_ph(s, 1), [subtitle], size=22, color=CINZA)
        bar = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.0), Inches(4.95), Inches(1.5), Inches(0.06))
        bar.fill.solid(); bar.fill.fore_color.rgb = LARANJA; bar.line.fill.background()
        return self._finish(s)

    def bullets(self, title, items, notes=None):
        """Título + lista com níveis. items: ['texto', ('subitem', 1), ...]."""
        s = self._new(L_CONTEUDO, notes)
        _set_title(_ph(s, 0), title)
        _fill_text(_ph(s, 1), items)
        return self._finish(s)

    def two_columns(self, title, left, right, notes=None):
        s = self._new(L_DUAS, notes)
        _set_title(_ph(s, 0), title)
        size = min(_fit_size(_norm_items(left), 5.67, 4.75), _fit_size(_norm_items(right), 5.67, 4.75))
        _fill_text(_ph(s, 1), left, size=size)
        _fill_text(_ph(s, 2), right, size=size)
        return self._finish(s)

    def comparison(self, title, left_title, left, right_title, right, notes=None):
        s = self._new(L_COMPARACAO, notes)
        _set_title(_ph(s, 0), title)
        for idx, head in ((1, left_title), (3, right_title)):
            _fill_text(_ph(s, idx), [head], size=22, color=AZUL, bold_level0=True)
        size = min(_fit_size(_norm_items(left), 5.64, 4.10), _fit_size(_norm_items(right), 5.67, 4.10))
        _fill_text(_ph(s, 2), left, size=size)
        _fill_text(_ph(s, 4), right, size=size)
        return self._finish(s)

    def image(self, title, path, caption=None, notes=None):
        """Título + imagem ajustada (proporção preservada) na área de conteúdo."""
        s = self._new(L_SO_TITULO, notes)
        _set_title(_ph(s, 0), title)
        box_h = AREA["h"] - (0.45 if caption else 0)
        pic = s.shapes.add_picture(str(path), Inches(AREA["x"]), Inches(AREA["y"]))
        scale = min(Inches(AREA["w"]) / pic.width, Inches(box_h) / pic.height)
        pic.width, pic.height = int(pic.width * scale), int(pic.height * scale)
        pic.left = int(Inches(AREA["x"]) + (Inches(AREA["w"]) - pic.width) / 2)
        pic.top = int(Inches(AREA["y"]) + (Inches(box_h) - pic.height) / 2)
        if caption:
            tb = s.shapes.add_textbox(Inches(AREA["x"]), Inches(AREA["y"] + box_h + 0.05), Inches(AREA["w"]), Inches(0.4))
            p = tb.text_frame.paragraphs[0]
            p.text, p.alignment = caption, PP_ALIGN.CENTER
            p.runs[0].font.size, p.runs[0].font.italic, p.runs[0].font.color.rgb = Pt(14), True, CINZA
        return self._finish(s)

    def image_text(self, title, path, text_items, crop=False, notes=None):
        """Layout 'Imagem com Legenda': título e texto à esquerda, imagem grande à direita.

        crop=False (padrão) encaixa a imagem inteira no quadro; crop=True recorta para preencher
        (bom para fotos, ruim para diagramas e logos).
        """
        s = self._new(L_IMAGEM_LEGENDA, notes)
        _set_title(_ph(s, 0), title, base=28)
        frame = _ph(s, 1)
        fx, fy, fw, fh = frame.left, frame.top, frame.width, frame.height
        pic = frame.insert_picture(str(path))
        if not crop:
            pic.crop_left = pic.crop_right = pic.crop_top = pic.crop_bottom = 0
            iw, ih = pic.image.size
            scale = min(fw / iw, fh / ih)
            w, h = int(iw * scale), int(ih * scale)
            pic.left, pic.top, pic.width, pic.height = int(fx + (fw - w) / 2), int(fy + (fh - h) / 2), w, h
        _fill_text(_ph(s, 2), text_items, size=_fit_size(_norm_items(text_items), 4.30, 4.35, (20, 18, 16, 14)))
        return self._finish(s)

    def motion_figure(
        self,
        title: str,
        path: str | Path,
        caption: str | None = None,
        side_text: list | str | None = None,
        media_side: str = "right",
        notes: str | None = None,
    ):
        """Insere figura/animação produzida em Motion Design (Manim / Blender).
        
        Suporta imagens estáticas de alta definição (PNG), GIFs animados em loop e vídeos MP4.
        - Se side_text for None: a mídia é centralizada em destaque na área de conteúdo (layout hero).
        - Se side_text for fornecido: divide o slide em duas colunas (texto explicativo + mídia motion).
        """
        path = Path(path).resolve()
        if not path.exists():
            raise FileNotFoundError(f"Arquivo de motion design não encontrado: {path}")

        s = self._new(L_SO_TITULO, notes)
        _set_title(_ph(s, 0), title)

        ext = path.suffix.lower()
        is_video = ext in (".mp4", ".mov", ".avi", ".wmv")

        if not side_text:
            box_h = AREA["h"] - (0.45 if caption else 0)
            if is_video:
                vw = min(AREA["w"], box_h * 16 / 9)
                vh = vw * 9 / 16
                vx = AREA["x"] + (AREA["w"] - vw) / 2
                vy = AREA["y"] + (box_h - vh) / 2
                s.shapes.add_movie(str(path), Inches(vx), Inches(vy), Inches(vw), Inches(vh))
            else:
                pic = s.shapes.add_picture(str(path), Inches(AREA["x"]), Inches(AREA["y"]))
                scale = min(Inches(AREA["w"]) / pic.width, Inches(box_h) / pic.height)
                pic.width, pic.height = int(pic.width * scale), int(pic.height * scale)
                pic.left = int(Inches(AREA["x"]) + (Inches(AREA["w"]) - pic.width) / 2)
                pic.top = int(Inches(AREA["y"]) + (Inches(box_h) - pic.height) / 2)

            if caption:
                tb = s.shapes.add_textbox(Inches(AREA["x"]), Inches(AREA["y"] + box_h + 0.05), Inches(AREA["w"]), Inches(0.4))
                p = tb.text_frame.paragraphs[0]
                p.text, p.alignment = caption, PP_ALIGN.CENTER
                p.runs[0].font.size, p.runs[0].font.italic, p.runs[0].font.color.rgb = Pt(14), True, CINZA
        else:
            text_w = 4.80
            gap = 0.40
            media_w = AREA["w"] - text_w - gap
            box_h = AREA["h"] - (0.45 if caption else 0)

            if media_side == "left":
                media_x = AREA["x"]
                text_x = AREA["x"] + media_w + gap
            else:
                text_x = AREA["x"]
                media_x = AREA["x"] + text_w + gap

            items = [side_text] if isinstance(side_text, str) else side_text
            tb = s.shapes.add_textbox(Inches(text_x), Inches(AREA["y"]), Inches(text_w), Inches(box_h))
            body = [(f"•  {t}" if lvl == 0 else f"–  {t}", lvl) for t, lvl in _norm_items(items)]
            _fill_text(tb, body, size=_fit_size(body, text_w, box_h, (22, 20, 18, 16, 14)))

            if is_video:
                vw = min(media_w, box_h * 16 / 9)
                vh = vw * 9 / 16
                vx = media_x + (media_w - vw) / 2
                vy = AREA["y"] + (box_h - vh) / 2
                s.shapes.add_movie(str(path), Inches(vx), Inches(vy), Inches(vw), Inches(vh))
            else:
                pic = s.shapes.add_picture(str(path), Inches(media_x), Inches(AREA["y"]))
                scale = min(Inches(media_w) / pic.width, Inches(box_h) / pic.height)
                pic.width, pic.height = int(pic.width * scale), int(pic.height * scale)
                pic.left = int(Inches(media_x) + (Inches(media_w) - pic.width) / 2)
                pic.top = int(Inches(AREA["y"]) + (Inches(box_h) - pic.height) / 2)

            if caption:
                tb_c = s.shapes.add_textbox(Inches(media_x), Inches(AREA["y"] + box_h + 0.05), Inches(media_w), Inches(0.45))
                tf_c = tb_c.text_frame
                tf_c.word_wrap = True
                tf_c.margin_left = tf_c.margin_right = tf_c.margin_top = tf_c.margin_bottom = 0
                p = tf_c.paragraphs[0]
                p.text, p.alignment = caption, PP_ALIGN.CENTER
                p.runs[0].font.size, p.runs[0].font.italic, p.runs[0].font.color.rgb = Pt(11), True, CINZA

        return self._finish(s)

    def manim_figure(self, title: str, path: str | Path, caption: str | None = None, side_text: list | str | None = None, media_side: str = "right", notes: str | None = None):
        """Atalho semântico para figuras/animações geradas via Manim."""
        return self.motion_figure(title, path, caption=caption, side_text=side_text, media_side=media_side, notes=notes)

    def blender_figure(self, title: str, path: str | Path, caption: str | None = None, side_text: list | str | None = None, media_side: str = "right", notes: str | None = None):
        """Atalho semântico para figuras 3D geradas via Blender."""
        return self.motion_figure(title, path, caption=caption, side_text=side_text, media_side=media_side, notes=notes)

    def code(self, title, code, language="python", caption=None, notes=None):
        """Bloco de código com fundo escuro e fonte monoespaçada (cores via pygments, se instalado)."""
        s = self._new(L_SO_TITULO, notes)
        _set_title(_ph(s, 0), title)
        lines = code.expandtabs(4).rstrip("\n").split("\n")
        longest = max(len(l) for l in lines) or 1
        max_h = AREA["h"] - (0.45 if caption else 0)
        size = min(20, (max_h - 0.4) * 72 / (len(lines) * 1.2), (AREA["w"] - 0.6) * 72 / (longest * 0.6))
        size = max(10, int(size))
        box_h = min(max_h, len(lines) * size * 1.2 / 72 + 0.5)   # caixa do tamanho do código
        bg = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(AREA["x"]), Inches(AREA["y"]), Inches(AREA["w"]), Inches(box_h))
        bg.adjustments[0] = 0.03
        bg.fill.solid(); bg.fill.fore_color.rgb = CODE_BG; bg.line.fill.background()
        tf = bg.text_frame
        tf.word_wrap, tf.vertical_anchor = False, MSO_ANCHOR.TOP
        tf.margin_left = tf.margin_right = Inches(0.3)
        tf.margin_top = Inches(0.2)
        for i, line_tokens in enumerate(_highlight(lines, language)):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            p.alignment = PP_ALIGN.LEFT
            p.line_spacing = 1.0
            for text, rgb in line_tokens or [(" ", CODE_FG)]:
                r = p.add_run()
                r.text = text
                r.font.name, r.font.size, r.font.color.rgb = "Consolas", Pt(size), rgb
        # faixa laranja à esquerda (assinatura visual)
        acc = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(AREA["x"]), Inches(AREA["y"] + 0.15), Inches(0.07), Inches(box_h - 0.3))
        acc.fill.solid(); acc.fill.fore_color.rgb = LARANJA; acc.line.fill.background()
        if caption:
            tb = s.shapes.add_textbox(Inches(AREA["x"]), Inches(AREA["y"] + box_h + 0.05), Inches(AREA["w"]), Inches(0.4))
            p = tb.text_frame.paragraphs[0]
            p.text = caption
            p.runs[0].font.size, p.runs[0].font.italic, p.runs[0].font.color.rgb = Pt(14), True, CINZA
        return self._finish(s)

    def table(self, title, header, rows, col_widths=None, notes=None):
        """Tabela com cabeçalho azul SENAI e linhas alternadas."""
        s = self._new(L_SO_TITULO, notes)
        _set_title(_ph(s, 0), title)
        n_rows, n_cols = len(rows) + 1, len(header)
        row_h = min(0.6, AREA["h"] / n_rows)
        size = 18 if row_h >= 0.5 and n_cols <= 4 else 14 if row_h >= 0.35 else 12
        gf = s.shapes.add_table(n_rows, n_cols, Inches(AREA["x"]), Inches(AREA["y"]), Inches(AREA["w"]), Inches(row_h * n_rows))
        tbl = gf.table
        if col_widths:
            total = sum(col_widths)
            for i, w in enumerate(col_widths):
                tbl.columns[i].width = Inches(AREA["w"] * w / total)
        for r in range(n_rows):
            values = header if r == 0 else rows[r - 1]
            for c in range(n_cols):
                cell = tbl.cell(r, c)
                cell.text = str(values[c]) if c < len(values) else ""
                cell.fill.solid()
                cell.fill.fore_color.rgb = AZUL if r == 0 else (AZUL_CLARO if r % 2 == 0 else RGBColor(0xFF, 0xFF, 0xFF))
                cell.vertical_anchor = MSO_ANCHOR.MIDDLE
                for p in cell.text_frame.paragraphs:
                    for run in p.runs:
                        run.font.size = Pt(size)
                        run.font.bold = r == 0
                        run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF) if r == 0 else TEXTO
        return self._finish(s)

    def highlight(self, title, statement, items=None, notes=None):
        """Slide de destaque: uma frase/conceito em caixa + itens opcionais abaixo."""
        s = self._new(L_SO_TITULO, notes)
        _set_title(_ph(s, 0), title)
        box_h = 1.6 if items else AREA["h"] - 0.5
        box = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(AREA["x"]), Inches(AREA["y"]), Inches(AREA["w"]), Inches(box_h))
        box.fill.solid(); box.fill.fore_color.rgb = AZUL_CLARO; box.line.fill.background()
        acc = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(AREA["x"]), Inches(AREA["y"]), Inches(0.12), Inches(box_h))
        acc.fill.solid(); acc.fill.fore_color.rgb = LARANJA; acc.line.fill.background()
        tf = box.text_frame
        tf.word_wrap, tf.vertical_anchor = True, MSO_ANCHOR.MIDDLE
        tf.margin_left = Inches(0.45)
        p = tf.paragraphs[0]
        p.text, p.alignment = statement, PP_ALIGN.LEFT
        size = _fit_size([(statement, 0)], AREA["w"] - 0.6, box_h, (32, 28, 24, 22, 20, 18))
        p.runs[0].font.size, p.runs[0].font.bold, p.runs[0].font.color.rgb = Pt(size), True, AZUL
        if items:
            tb = s.shapes.add_textbox(Inches(AREA["x"]), Inches(AREA["y"] + box_h + 0.2), Inches(AREA["w"]), Inches(AREA["h"] - box_h - 0.2))
            body = [(f"•  {t}" if lvl == 0 else f"–  {t}", lvl) for t, lvl in _norm_items(items)]  # caixa de texto livre não herda marcadores
            _fill_text(tb, body, size=_fit_size(body, AREA["w"], AREA["h"] - box_h - 0.2, (24, 22, 20, 18, 16)))
        return self._finish(s)

    def closing(self, title="Obrigado!", subtitle="", notes=None):
        """Encerramento: mesmo visual da capa (com rodapé Fatesg), mas sem preencher curso/professor."""
        return self.cover(title, subtitle, course="", professor="", notes=notes)

    # -------------------------------------------------- saída
    def save(self, path):
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        self.prs.save(str(path))
        return path


# ---------------------------------------------------------------- realce de sintaxe (opcional)
_PALETTE = {
    "Keyword": RGBColor(0xC6, 0x78, 0xDD), "Name.Builtin": RGBColor(0x61, 0xAF, 0xEF),
    "Name.Function": RGBColor(0x61, 0xAF, 0xEF), "Name.Class": RGBColor(0xE5, 0xC0, 0x7B),
    "Literal.String": RGBColor(0x98, 0xC3, 0x79), "Literal.Number": RGBColor(0xD1, 0x9A, 0x66),
    "Comment": RGBColor(0x7F, 0x84, 0x8E), "Operator": RGBColor(0x56, 0xB6, 0xC2),
}


def _highlight(lines, language):
    try:
        from pygments import lex
        from pygments.lexers import get_lexer_by_name
        lexer = get_lexer_by_name(language)
    except Exception:
        return [[(l, CODE_FG)] if l else [] for l in lines]
    out, current = [], []
    for ttype, value in lex("\n".join(lines), lexer):
        color = CODE_FG
        for key, rgb in _PALETTE.items():
            if str(ttype).replace("Token.", "").startswith(key):
                color = rgb
                break
        parts = value.split("\n")
        for j, part in enumerate(parts):
            if j > 0:
                out.append(current)
                current = []
            if part:
                current.append((part, color))
    out.append(current)
    return out[: len(lines)]


# Alias de retrocompatibilidade
SenaiDeck = UaipptDeck


# ---------------------------------------------------------------- CLI (roteiro JSON)
def build_from_outline(outline: dict, output: str | Path | None = None) -> Path:
    prof = outline.get("professor")
    if not prof and sys.stdin and hasattr(sys.stdin, "isatty") and sys.stdin.isatty():
        try:
            prof = input("Qual é o nome do(a) professor(a) responsável pela apresentação? ").strip()
        except Exception:
            prof = ""

    deck = UaipptDeck(
        template=outline.get("template", TEMPLATE),
        default_professor=prof or DEFAULT_PROFESSOR,
        default_course=outline.get("course", DEFAULT_COURSE)
    )
    for spec in outline["slides"]:
        spec = dict(spec)
        kind = spec.pop("type")
        method = getattr(deck, kind, None)
        if method is None or kind.startswith("_") or kind == "save":
            raise ValueError(f"tipo de slide desconhecido: {kind}")
        method(**spec)
    return deck.save(output or outline.get("output", "apresentacao.pptx"))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    print(build_from_outline(data, sys.argv[2] if len(sys.argv) > 2 else None))
