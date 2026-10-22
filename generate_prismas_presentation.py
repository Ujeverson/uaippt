"""Gera a apresentação de validação:
Prismas: área e volume (9º ano do Ensino Fundamental) — 4 aulas de 30 minutos,
exemplos resolvidos e 5 atividades com soluções nas Anotações.

Padrão (slideExemploComConteudo.pdf):
  capa: título Poppins 36 + nome do professor Poppins 40
  slides 2+: título Montserrat 36 + conteúdo Calibri 24 (texto à esquerda, imagem à direita)
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / ".agents" / "skills" / "uaippt" / "scripts"))
from uaippt_deck import UaipptDeck  # noqa: E402

FIG = ROOT / "assets_prismas"
MOTION = ROOT / ".agents" / "skills" / "uaippt" / "assets" / "motion_renders"
OUT_PPTX = ROOT / "Prismas_Area_e_Volume_9Ano.pptx"
CRED = "Figura: autoria própria"


def build_deck():
    deck = UaipptDeck(default_professor="Prof. Msc. Ujeverson Tavares",
                      default_course="Matemática — 9º Ano", social_handle="@prof.ujeverson")

    # ------------------------------------------------------------------ CAPA
    deck.cover(
        "Prismas: Área e Volume", "Geometria Espacial • 4 aulas de 30 minutos",
        course="Matemática — 9º Ano do Ensino Fundamental", professor="Prof. Msc. Ujeverson Tavares",
        notes=("ORIENTAÇÕES GERAIS:\n- Habilidade BNCC EF09MA19: resolver e elaborar problemas que envolvam "
               "medidas de volumes de prismas retos.\n- 4 blocos de 30 minutos (120 min).\n"
               "- Recursos: projetor, régua, calculadora e, se houver, modelos de sólidos.\n"
               "- Cada aula tem exposição, exemplo resolvido e atividade; as soluções das cinco atividades "
               "estão nas anotações dos respectivos slides."))

    deck.table(
        "Cronograma das Quatro Aulas",
        ["Aula", "Tópico", "Foco"],
        [["1 • 30 min", "O que é um prisma?", "Elementos e relação de Euler"],
         ["2 • 30 min", "Áreas da superfície", "Planificação, Al e At"],
         ["3 • 30 min", "Volume e capacidade", "V = Ab · h e litros"],
         ["4 • 30 min", "Aplicações e síntese", "Problemas integrados"]],
        col_widths=[1.4, 2.6, 3.0],
        notes="Apresente a jornada de 4 aulas. Cada aula termina com uma atividade; as soluções ficam nas anotações.")

    # ------------------------------------------------------------------ AULA 1
    deck.section("Aula 1: O que é um Prisma?", "Definição, elementos e classificação (30 min)",
                 notes="Pergunte: que objetos da sala ou de casa lembram prismas? (caixas, lápis sextavados, telhados).")

    deck.highlight(
        "Definição Geométrica de Prisma",
        "Prisma é um poliedro com duas bases poligonais paralelas e congruentes; suas faces laterais são paralelogramos.",
        ["Altura (h): distância perpendicular entre as bases",
         "Prisma reto: faces laterais retangulares",
         "No 9º ano, o foco são os prismas retos"],
        notes=("Diferencie prisma de pirâmide: a pirâmide tem uma só base e um vértice; o prisma tem duas bases "
               "idênticas e paralelas."))

    deck.image_text(
        "Elementos Fundamentais do Prisma", FIG / "elementos_prisma.png",
        ["**Bases:** dois polígonos congruentes", "**Faces laterais:** retângulos",
         "**Arestas:** da base e laterais", "**Vértices:** pontos de encontro", "**Altura (h):** entre as bases"],
        caption=CRED, bulleted=True,
        notes=("No prisma reto, a aresta lateral mede o mesmo que a altura h. O número de faces laterais é sempre "
               "igual ao número de lados da base."))

    deck.blender_figure(
        "Rotação 3D do Prisma Regular", MOTION / "blender_prisma_hex_loop.gif",
        caption="Blender • uaippt",
        side_text=["Duas bases idênticas e paralelas", "Faces laterais retangulares",
                   "O giro ajuda a ver a forma em 3D"],
        notes="Deixe o GIF girar e peça que os alunos apontem as bases e as faces laterais.")

    deck.blender_figure(
        "Vista Explodida do Prisma", MOTION / "blender_vista_explodida.png",
        caption="Blender • uaippt",
        side_text=["Bases em laranja: 2", "Faces laterais em azul: n", "Total de faces: F = n + 2"],
        notes="Com as peças separadas, os alunos contam faces, e a relação de Euler fica mais natural.")

    deck.table(
        "Classificação e Relação de Euler",
        ["Base", "Prisma", "F", "V", "A", "V − A + F"],
        [["Triângulo", "Triangular", "5", "6", "9", "2"],
         ["Quadrilátero", "Quadrangular", "6", "8", "12", "2"],
         ["Pentágono", "Pentagonal", "7", "10", "15", "2"],
         ["Hexágono", "Hexagonal", "8", "12", "18", "2"]],
        col_widths=[2.0, 2.4, 0.8, 0.8, 0.8, 1.6],
        notes="Para base de n lados: F = n + 2, V = 2n e A = 3n. Então V − A + F = 2n − 3n + n + 2 = 2.")

    deck.two_columns(
        "Prismas no Cotidiano",
        ["**Onde estão?**", "Caixas de sapato e de leite", "Chocolate triangular", "Lápis sextavado", "Galpões industriais"],
        ["**Por que são usados?**", "Empilham sem deixar vãos", "Economizam espaço no transporte", "São fáceis de montar", "Estruturas estáveis"],
        notes="Relacione com logística industrial: caixas prismáticas aproveitam toda a área do pallet.")

    deck.highlight(
        "Atividade 1 • Elementos do Prisma",
        "Uma fábrica de biscoitos criou uma embalagem em forma de prisma octogonal reto (base com 8 lados).",
        ["a) Quantas bases e quantas faces laterais?",
         "b) Quantos faces, vértices e arestas no total?",
         "c) Verifique a relação de Euler (V − A + F = 2)."],
        notes=("SOLUÇÃO — ATIVIDADE 1:\na) 2 bases (octógonos) e 8 faces laterais retangulares.\n"
               "b) F = 8 + 2 = 10; V = 8 + 8 = 16; A = 8 + 8 + 8 = 24.\n"
               "c) V − A + F = 16 − 24 + 10 = 2. Confirmado."))

    # ------------------------------------------------------------------ AULA 2
    deck.section("Aula 2: Áreas da Superfície", "Planificação, área lateral e área total (30 min)",
                 notes="Objetivo: calcular o material necessário para fabricar ou revestir um prisma.")

    deck.image_text(
        "Planificação de um Prisma Reto", FIG / "planificacao_prisma.png",
        ["Planificar é abrir o sólido no plano", "As faces laterais formam um retângulo",
         "Base do retângulo = perímetro (2p)", "Altura do retângulo = h", "As duas bases completam a superfície"],
        caption=CRED, bulleted=True,
        notes="A planificação é a base do corte industrial de papelão e chapas. Al = (perímetro da base) × h.")

    deck.manim_figure(
        "Planificação Geométrica (Manim)", MOTION / "manim_planificacao.png",
        caption="Manim • uaippt",
        side_text=["Três faces laterais em faixa", "Cotas: altura h e perímetro 2p",
                   "Duas bases nas abas", "At = Al + 2·Ab"],
        notes="Mostre como a lateral vira um retângulo e onde entram as duas bases.")

    deck.bullets(
        "Fórmulas das Áreas da Superfície",
        ["**Área da base (Ab):** área do polígono da base",
         ("Quadrado: l² • retângulo: b·h • triângulo: b·h/2", 1),
         "**Área lateral (Al):** Al = (perímetro da base) × h",
         "**Área total (At):** At = Al + 2 · Ab"],
        notes="Por que 2·Ab? O prisma tem duas bases (tampa e fundo). Caixa aberta: usa-se apenas 1·Ab.")

    deck.two_columns(
        "Exemplo Resolvido 1: Caixa",
        ["**Problema:**", "Caixa de sapato de 30 cm × 20 cm × 12 cm.", "Calcule a área total de papelão."],
        ["**Resolução:**", "Ab = 30 × 20 = 600 cm²", "2p = 2·(30 + 20) = 100 cm",
         "Al = 100 × 12 = 1.200 cm²", "At = 1.200 + 2·600 = **2.400 cm²**"],
        notes=("Método alternativo: At = 2(ab + ac + bc) = 2(600 + 360 + 240) = 2.400 cm². Ambos chegam ao mesmo resultado."))

    deck.comparison(
        "Exemplo Resolvido 2: O Cubo",
        "Conceito", ["6 faces quadradas iguais", "Área de uma face = a²", "At = 6a²"],
        "Aplicação (a = 5 cm)", ["1 face: 5² = 25 cm²", "Lateral (4 faces): 100 cm²", "Total (6 faces): **150 cm²**"],
        notes="O cubo é o prisma mais simétrico: todas as faces são congruentes.")

    deck.highlight(
        "Atividade 2 • Luminária Prismática",
        "Uma luminária em forma de prisma reto de base quadrada tem aresta da base de 10 cm e altura de 25 cm.",
        ["Calcule a área lateral.", "Calcule a área total."],
        notes=("SOLUÇÃO — ATIVIDADE 2:\nAb = 10² = 100 cm²; 2p = 4 × 10 = 40 cm.\n"
               "Al = 40 × 25 = 1.000 cm².\nAt = 1.000 + 2·100 = 1.200 cm²."))

    deck.highlight(
        "Atividade 3 • Embalagem de Presente",
        "Juliana vai encapar uma caixa de 25 cm × 15 cm × 8 cm. O papel deve ter 15% a mais para dobras e emendas.",
        ["Qual é a área mínima de papel necessária?"],
        notes=("SOLUÇÃO — ATIVIDADE 3:\nAt = 2(25·15 + 25·8 + 15·8) = 2(375 + 200 + 120) = 1.390 cm².\n"
               "Acréscimo: 1.390 × 0,15 = 208,5 cm².\nTotal: 1.390 + 208,5 = 1.598,5 cm²."))

    # ------------------------------------------------------------------ AULA 3
    deck.section("Aula 3: Volume e Capacidade", "Cálculo de volume e relação com litros (30 min)",
                 notes="Foco: volume como espaço ocupado e a ligação entre unidades cúbicas e litros.")

    deck.image_text(
        "O Princípio do Cálculo de Volume", FIG / "volume_capacidade.png",
        ["Volume é o espaço ocupado", "Empilhe fatias de área Ab até a altura h", "**V = Ab · h**",
         "1 m³ = 1.000 L • 1 dm³ = 1 L"],
        caption=CRED, bulleted=True,
        notes="Princípio de Cavalieri: mesma altura e seções de áreas iguais levam ao mesmo volume.")

    deck.manim_figure(
        "Volume por Extrusão (Manim)", MOTION / "manim_volume_extrusao.png",
        caption="Manim • uaippt",
        side_text=["Base com área Ab", "Camadas empilhadas até h", "Volume = Ab × h"],
        notes="Compare com empilhar folhas de papel: cada folha acrescenta uma camada de área Ab.")

    deck.image_text(
        "Volume de Blocos Retangulares", FIG / "paralelepipedo_cubo.png",
        ["**Paralelepípedo:** V = c · l · h", "**Cubo de aresta a:** V = a³",
         "Use a mesma unidade nas três medidas"],
        caption=CRED, bulleted=True,
        notes="Todas as medidas devem estar na MESMA unidade antes de multiplicar.")

    deck.table(
        "Volume x Capacidade",
        ["Volume", "Capacidade", "Exemplo"],
        [["1 m³", "1.000 L", "Caixa d'água"], ["1 dm³", "1 L", "Caixa de leite"],
         ["1 cm³", "1 mL", "Seringa"], ["1.000 cm³", "1 L", "Garrafa de água"]],
        col_widths=[1.6, 1.6, 2.6],
        notes="Erro clássico: 1 m³ NÃO é 100 L. 1 m = 10 dm → 1 m³ = (10 dm)³ = 1.000 dm³ = 1.000 L.")

    deck.two_columns(
        "Exemplo Resolvido 3: Caixa d'Água",
        ["**Problema:**", "Caixa de 2,0 m × 1,5 m × 1,2 m.", "Quantos litros ela comporta?"],
        ["**Resolução:**", "V = 2,0 × 1,5 × 1,2 = 3,6 m³", "1 m³ = 1.000 L", "Capacidade = **3.600 L**"],
        notes="Em decímetros: 20 × 15 × 12 = 3.600 dm³ = 3.600 L — resposta direta em litros.")

    deck.image_text(
        "Volume do Prisma Triangular", FIG / "prisma_triangular.png",
        ["Base: triângulo (b e h_tri)", "Ab = b · h_tri / 2", "V = Ab · h_prisma",
         "Comum em telhados e rampas"],
        caption=CRED, bulleted=True,
        notes="Diferencie a altura do triângulo (h_tri) da altura do prisma (comprimento da peça).")

    deck.highlight(
        "Atividade 4 • Aquário da Escola",
        "Um aquário de 60 cm × 40 cm × 50 cm está com água até 45 cm de altura.",
        ["Quantos litros de água há no aquário?", "Dica: use a altura da água, não a do aquário."],
        notes=("SOLUÇÃO — ATIVIDADE 4:\nV = 60 × 40 × 45 = 108.000 cm³.\n108.000 ÷ 1.000 = 108 litros."))

    deck.blender_figure(
        "Reservatório 3D e Nível da Água", MOTION / "blender_reservatorio_agua.png",
        caption="Blender • uaippt",
        side_text=["Só a altura da água conta", "Altura da água: 45 cm", "60 × 40 × 45 cm³ = 108 L"],
        notes="Use a imagem para discutir por que o nível da água, e não a borda, define o volume.")

    # ------------------------------------------------------------------ AULA 4
    deck.section("Aula 4: Aplicações e Desafios", "Problemas integrados e síntese (30 min)",
                 notes="Os alunos integram área e volume e decidem qual cálculo cada problema exige.")

    deck.comparison(
        "Área versus Volume",
        "Área (superfície)", ["Mede a casca externa", "Unidades: cm², m²", "Pintura, papelão, azulejo", "At = Al + 2·Ab"],
        "Volume (capacidade)", ["Mede o espaço interno", "Unidades: cm³, m³, L", "Água, concreto, ar", "V = Ab · h"],
        notes="Quadro de fixação para evitar confusão em avaliações.")

    deck.two_columns(
        "Exemplo Resolvido 4: Embalagem",
        ["**Dados:**", "Prisma de base quadrada, aresta 7 cm e altura 20 cm.", "a) Volume em mL", "b) Papelão gasto"],
        ["**Resolução:**", "Ab = 7 × 7 = 49 cm²", "a) V = 49 × 20 = 980 cm³ = **980 mL**",
         "b) Al = 28 × 20 = 560 cm²", "At = 560 + 98 = **658 cm²**"],
        notes="A indústria otimiza a relação área/volume para economizar material e transportar mais produto.")

    deck.highlight(
        "Atividade 5 • A Tenda de Camping",
        "Uma tenda é um prisma triangular reto de 3,0 m de comprimento; a frente é um triângulo isósceles de base 2,0 m e altura 1,5 m.",
        ["Calcule o volume de ar no interior da tenda."],
        notes=("SOLUÇÃO — ATIVIDADE 5:\nAb = (2,0 × 1,5) / 2 = 1,5 m².\nV = 1,5 × 3,0 = 4,5 m³.\n"
               "Em litros: 4,5 × 1.000 = 4.500 L de ar."))

    deck.table(
        "Quadro Resumo de Fórmulas",
        ["Prisma", "Ab", "Al", "At", "V"],
        [["Reto geral", "área da base", "2p · h", "Al + 2Ab", "Ab · h"],
         ["Paralelepípedo", "a · b", "2(ac + bc)", "2(ab+ac+bc)", "a · b · c"],
         ["Cubo", "a²", "4a²", "6a²", "a³"],
         ["Triangular", "b·h_tri/2", "2p · h", "Al + 2Ab", "Ab · h"]],
        col_widths=[2.0, 1.8, 1.8, 2.0, 1.6],
        notes="Tabela de consulta rápida para estudo e avaliações.")

    deck.closing("Parabéns!", "Prismas: área e volume concluído",
                 notes="Encerre parabenizando a turma e indique a lista complementar de exercícios.")

    out = deck.save(OUT_PPTX)
    print(f"Apresentação gerada: {out}")
    return out


if __name__ == "__main__":
    build_deck()
