"""Gera a apresentação completa de validação:
Prismas: área e volume (9º ano do Ensino Fundamental)
4 aulas de 30 minutos, exemplos resolvidos e 5 atividades com soluções nas Anotações.
"""
import sys
from pathlib import Path

# Adiciona o caminho dos scripts da skill uaippt
SKILL_SCRIPTS = Path(__file__).resolve().parent / ".agents" / "skills" / "uaippt" / "scripts"
sys.path.insert(0, str(SKILL_SCRIPTS))

from uaippt_deck import UaipptDeck

ASSETS = Path(__file__).resolve().parent / "assets_prismas"
MOTION_ASSETS = Path(__file__).resolve().parent / ".agents" / "skills" / "uaippt" / "assets" / "motion_renders"
OUT_PPTX = Path(__file__).resolve().parent / "Prismas_Area_e_Volume_9Ano.pptx"

def build_deck():
    deck = UaipptDeck(
        default_professor="Prof. Msc. Ujeverson Tavares",
        default_course="Matemática — 9º Ano"
    )

    # =========================================================================
    # SLIDE 1: CAPA
    # =========================================================================
    deck.cover(
        title="Prismas: Área e Volume",
        subtitle="Geometria Espacial • 4 Aulas de 30 minutos",
        course="Matemática — 9º Ano do Ensino Fundamental",
        professor="Prof. Msc. Ujeverson Tavares",
        notes=(
            "ORIENTAÇÕES GERAIS PARA O PROFESSOR:\n"
            "- Tema: Geometria Espacial (Prismas: área da superfície e volume).\n"
            "- Habilidade BNCC: EF09MA19 (Resolver e elaborar problemas que envolvam medidas de volumes de prismas retos).\n"
            "- Organização temporal: 4 blocos de 30 minutos (120 min no total).\n"
            "- Recursos: Apresentação multimídia, modelos geométricos sólidos (se disponíveis), régua e calculadora.\n"
            "- Estrutura: Cada aula possui exposição conceitual, exemplo resolvido passo a passo e atividade com resolução completa registrada nestas anotações."
        )
    )

    # =========================================================================
    # SLIDE 2: ESTRUTURA DO CURSO
    # =========================================================================
    deck.table(
        title="Cronograma das Quatro Aulas (4 × 30 min)",
        header=["Aula", "Tempo", "Tópico Principal", "Foco Didático"],
        rows=[
            ["Aula 1", "30 min", "O que é um Prisma?", "Conceito, elementos (bases, faces, arestas) e Relação de Euler"],
            ["Aula 2", "30 min", "Áreas da Superfície", "Planificação, Área Lateral (Al) e Área Total (At)"],
            ["Aula 3", "30 min", "Volume e Capacidade", "Fórmula V = Ab · h e relações com litros (m³, dm³, cm³)"],
            ["Aula 4", "30 min", "Aplicações e Síntese", "Problemas integrados (área x volume), desafios e resumo"]
        ],
        col_widths=[1.2, 1.0, 2.5, 3.8],
        notes="Apresentar o panorama geral aos alunos para que compreendam a jornada de aprendizado."
    )

    # =========================================================================
    # AULA 1: CONCEITO, ELEMENTOS E CLASSIFICAÇÃO
    # =========================================================================
    deck.section(
        title="Aula 1: O que é um Prisma?",
        subtitle="Definição geométrica, elementos e classificação (30 min)",
        notes="Iniciar a aula perguntando aos alunos quais objetos da sala de aula ou da casa deles lembram prismas."
    )

    deck.highlight(
        title="Definição Geométrica de Prisma",
        statement="Um prisma é um poliedro com duas bases poligonais paralelas e congruentes, cujas faces laterais são paralelogramos.",
        items=[
            "As bases têm exatamente o mesmo formato e tamanho (triângulos, quadrados, hexágonos...)",
            "A distância perpendicular entre os planos das duas bases é a altura (h)",
            "Prisma Reto: as arestas laterais são perpendiculares às bases (faces laterais são retângulos)",
            "No 9º ano, nosso foco principal são os prismas retos!"
        ],
        notes="Enfatizar a diferença entre prismas e pirâmides (pirâmides possuem apenas uma base e convergem para um vértice; prismas possuem duas bases idênticas e paralelas)."
    )

    deck.image_text(
        title="Elementos Fundamentais do Prisma",
        path=ASSETS / "elementos_prisma.png",
        text_items=[
            "Bases: dois polígonos paralelos e congruentes",
            "Faces Laterais: retângulos ligando as bases",
            "Arestas da Base: lados dos polígonos das bases",
            "Arestas Laterais: segmentos que unem as bases",
            "Vértices: pontos de junção das arestas",
            "Altura (h): distância entre as bases"
        ],
        notes=(
            "Chamar a atenção para o diagrama:\n"
            "- No prisma reto, o comprimento da aresta lateral é exatamente igual à altura h do prisma.\n"
            "- Mostrar que o número de faces laterais é sempre igual ao número de lados da base."
        )
    )

    deck.blender_figure(
        title="Rotação 3D do Prisma Regular (Blender)",
        path=MOTION_ASSETS / "blender_prisma_hex_loop.gif",
        caption="Motion Design 3D com Blender: rotação 360° em estúdio com fundo transparente e materiais oficiais SENAI",
        side_text=[
            "Sólido tridimensional em estúdio virtual",
            "Duas bases regulares idênticas e paralelas",
            "Faces laterais retangulares conectando os vértices",
            "Chanfro (bevel) destacado pela luz de contorno",
            "Giro contínuo facilita a percepção espacial"
        ],
        notes="Apresentar o prisma girando em 3D para que os alunos percebam a congruência entre a base superior e a inferior."
    )

    deck.blender_figure(
        title="Estrutura e Decomposição: Vista Explodida 3D",
        path=MOTION_ASSETS / "blender_vista_explodida.png",
        caption="Modelagem 3D Blender: separação física das duas bases poligonais e das faces laterais",
        side_text=[
            "Bases poligonais (em laranja SENAI): 2 bases idênticas",
            "Faces laterais (em azul SENAI): retângulos de fechamento",
            "Abertura espacial facilita a contagem de elementos",
            "Evidencia o número de faces: F = n (laterais) + 2 (bases)",
            "Visualização ideal para fixar a Relação de Euler"
        ],
        notes="Com a vista explodida, fica evidente para os alunos que as faces laterais 'envolvem' o perímetro das duas bases."
    )

    deck.table(
        title="Classificação dos Prismas e Relação de Euler",
        header=["Base", "Nome do Prisma", "Faces (F)", "Vértices (V)", "Arestas (A)", "V - A + F"],
        rows=[
            ["Triângulo (3 lados)", "Prisma Triangular", "5", "6", "9", "6 - 9 + 5 = 2"],
            ["Quadrilátero (4 lados)", "Prisma Quadrangular", "6", "8", "12", "8 - 12 + 6 = 2"],
            ["Pentágono (5 lados)", "Prisma Pentagonal", "7", "10", "15", "10 - 15 + 7 = 2"],
            ["Hexágono (6 lados)", "Prisma Hexagonal", "8", "12", "18", "12 - 18 + 8 = 2"]
        ],
        col_widths=[2.2, 2.3, 1.0, 1.0, 1.0, 1.8],
        notes=(
            "Destacar a Relação de Euler para poliedros convexos: V - A + F = 2.\n"
            "Fórmula geral para um prisma de base com n lados:\n"
            "- Faces: F = n + 2\n"
            "- Vértices: V = 2n\n"
            "- Arestas: A = 3n"
        )
    )

    deck.two_columns(
        title="Prismas no Cotidiano",
        left=[
            "Onde encontramos prismas?",
            ("Caixas de sapatos, caixas de leite (paralelepípedos)", 1),
            ("Embalagens de chocolate triangular (ex: Toblerone)", 1),
            ("Lápis e giz com seção transversal hexagonal", 1),
            ("Edifícios e galpões industriais modernos", 1)
        ],
        right=[
            "Por que essa forma é tão usada?",
            ("Facilidade de empilhamento vertical e horizontal", 1),
            ("Otimização de espaço no transporte e logística", 1),
            ("Facilidade de corte e montagem a partir de chapas planas", 1),
            ("Estruturas estáveis e resistentes", 1)
        ],
        notes="Comentar com a turma sobre o conceito de logística no SENAI e nas indústrias: caixas prismáticas aproveitam 100% da área dos pallets sem deixar vãos vazios."
    )

    deck.highlight(
        title="Atividade 1 • Identificação e Elementos",
        statement="Uma fábrica de biscoitos quer lançar uma embalagem em formato de prisma octogonal reto (base com 8 lados).",
        items=[
            "a) Quantas faces laterais e quantas bases essa embalagem possui?",
            "b) Qual é o número total de faces (F), vértices (V) e arestas (A)?",
            "c) Comprove que a Relação de Euler (V - A + F = 2) é satisfeita."
        ],
        notes=(
            "SOLUÇÃO COMPLETA DA ATIVIDADE 1:\n"
            "a) O prisma possui 2 bases (octógonos) e 8 faces laterais retangulares.\n"
            "b) Contagem de elementos (base com n = 8 lados):\n"
            "   - Total de Faces: F = 8 faces laterais + 2 bases = 10 faces.\n"
            "   - Total de Vértices: V = 8 vértices na base inferior + 8 vértices na base superior = 16 vértices.\n"
            "   - Total de Arestas: A = 8 arestas na base inferior + 8 arestas na base superior + 8 arestas laterais = 24 arestas.\n"
            "c) Verificação da Relação de Euler:\n"
            "   V - A + F = 16 - 24 + 10 = -8 + 10 = 2. Confirmado!"
        )
    )

    # =========================================================================
    # AULA 2: ÁREAS DA SUPERFÍCIE (LATERAL E TOTAL)
    # =========================================================================
    deck.section(
        title="Aula 2: Áreas da Superfície",
        subtitle="Planificação, Área Lateral e Área Total (30 min)",
        notes="Objetivo desta aula: capacitar os alunos a calcular a quantidade de material necessário para fabricar ou revestir um prisma."
    )

    deck.image_text(
        title="Planificação de um Prisma Reto",
        path=ASSETS / "planificacao_prisma.png",
        text_items=[
            "Planificar é abrir o sólido em uma folha plana",
            "As faces laterais juntas formam um único retângulo",
            "Comprimento desse retângulo = Perímetro da base (2p)",
            "Largura desse retângulo = Altura do prisma (h)",
            "As duas bases completam a superfície total"
        ],
        notes=(
            "Explicar que a planificação é a base do corte industrial de papelão e chapas metálicas.\n"
            "A área lateral é a área do retângulo 'esticado': Al = (perímetro da base) × h."
        )
    )

    deck.manim_figure(
        title="Planificação Geométrica da Superfície (Manim)",
        path=MOTION_ASSETS / "manim_planificacao.png",
        caption="Motion Design vetorial Manim: desdobramento das faces, cotas de altura e perímetro e dedução de At",
        side_text=[
            "Desdobramento contínuo das faces no plano",
            "Três faces laterais abertas em faixa contínua",
            "Cota de altura (h) e perímetro da base (2p = a + b + c)",
            "Duas bases triangulares em abas superior e inferior",
            "Dedução visual da fórmula: At = Al + 2·Ab"
        ],
        notes="A animação vetorial do Manim ilustra o processo mecânico de corte e dobra de embalagens na indústria gráfica."
    )

    deck.bullets(
        title="Fórmulas das Áreas da Superfície",
        items=[
            "Área da Base (Ab):",
            ("Área do polígono da base (quadrado: l², retângulo: b·h, triângulo: b·h/2)", 1),
            "Área Lateral (Al):",
            ("Soma de todas as faces laterais: Al = (Perímetro da Base) × h", 1),
            "Área Total (At):",
            ("Soma da área lateral com as duas bases idênticas:", 1),
            ("At = Al + 2 · Ab", 2)
        ],
        notes="Reforçar o porquê do '2 · Ab': o prisma possui DUAS bases (tampa e fundo). Se o exercício pedir uma caixa aberta ou sem tampa, usa-se apenas 1 · Ab."
    )

    deck.two_columns(
        title="Exemplo Resolvido 1: Paralelepípedo",
        left=[
            "Problema:",
            ("Uma caixa de sapato em forma de paralelepípedo tem dimensões 30 cm de comprimento, 20 cm de largura e 12 cm de altura.", 1),
            ("Calcule a área total de papelão necessária para produzir essa caixa (fechada).", 1)
        ],
        right=[
            "Resolução Passo a Passo:",
            ("1. Área da base: Ab = 30 × 20 = 600 cm²", 1),
            ("2. Perímetro da base: 2p = 2×(30 + 20) = 100 cm", 1),
            ("3. Área lateral: Al = 100 × 12 = 1.200 cm²", 1),
            ("4. Área total: At = Al + 2·Ab", 1),
            ("At = 1.200 + 2 × (600) = 2.400 cm²", 2)
        ],
        notes=(
            "MÉTODO ALTERNATIVO (Soma aos pares):\n"
            "At = 2·(a·b + a·c + b·c)\n"
            "At = 2·(30·20 + 30·12 + 20·12) = 2·(600 + 360 + 240) = 2·(1200) = 2.400 cm².\n"
            "Ambos os métodos são válidos e chegam ao mesmo resultado!"
        )
    )

    deck.comparison(
        title="Exemplo Resolvido 2: O Cubo",
        left_title="Conceito do Cubo",
        left=[
            "O cubo possui 6 faces quadradas idênticas",
            "Todas as arestas têm a mesma medida 'a'",
            "Área de cada face = a²",
            "Área Total: At = 6 · a²"
        ],
        right_title="Aplicação com Números",
        right=[
            "Dado um cubo de aresta a = 5 cm:",
            "Área de 1 face = 5² = 25 cm²",
            "Área lateral (4 faces) = 4 × 25 = 100 cm²",
            "Área total (6 faces) = 6 × 25 = 150 cm²"
        ],
        notes="Destacar que o cubo é o prisma mais simétrico que existe: todas as faces são congruentes entre si."
    )

    deck.highlight(
        title="Atividade 2 • Área de Prisma Quadrangular",
        statement="Uma luminária em formato de prisma reto de base quadrada tem aresta da base medindo 10 cm e altura de 25 cm. Determine a área lateral e a área total dessa luminária.",
        items=[
            "Passo 1: Calcule a área da base quadrada (Ab = L²)",
            "Passo 2: Calcule o perímetro da base (2p = 4 × L)",
            "Passo 3: Calcule a área lateral (Al = 2p × h) e a área total (At = Al + 2·Ab)"
        ],
        notes=(
            "SOLUÇÃO COMPLETA DA ATIVIDADE 2:\n"
            "1. Área da base (quadrado de lado 10 cm):\n"
            "   Ab = 10² = 100 cm²\n"
            "2. Perímetro da base:\n"
            "   2p = 4 × 10 = 40 cm\n"
            "3. Área lateral (4 retângulos de 10 cm × 25 cm):\n"
            "   Al = 2p × h = 40 × 25 = 1.000 cm²\n"
            "4. Área total:\n"
            "   At = Al + 2·Ab = 1.000 + 2·(100) = 1.000 + 200 = 1.200 cm²."
        )
    )

    deck.highlight(
        title="Atividade 3 • Embalagem de Presente",
        statement="Juliana vai encapar uma caixa de presente de dimensões 25 cm × 15 cm × 8 cm com papel decorativo. Sabendo que é preciso 15% a mais de papel para dobras e emendas, qual a área mínima de papel necessária?",
        items=[
            "Calcule a área total da caixa de presente",
            "Calcule 15% sobre o valor da área total para as dobras",
            "Some a área da caixa com o acréscimo de 15%"
        ],
        notes=(
            "SOLUÇÃO COMPLETA DA ATIVIDADE 3:\n"
            "1. Área total da caixa (paralelepípedo a = 25, b = 15, c = 8):\n"
            "   At = 2 · (ab + ac + bc)\n"
            "   ab = 25 × 15 = 375 cm²\n"
            "   ac = 25 × 8 = 200 cm²\n"
            "   bc = 15 × 8 = 120 cm²\n"
            "   At = 2 · (375 + 200 + 120) = 2 · (695) = 1.390 cm².\n"
            "2. Acréscimo de 15% para dobras e acabamento:\n"
            "   Sobras = 1.390 × 0,15 = 208,5 cm².\n"
            "3. Área total de papel necessária:\n"
            "   Total = 1.390 + 208,5 = 1.598,5 cm²."
        )
    )

    # =========================================================================
    # AULA 3: VOLUME E CAPACIDADE
    # =========================================================================
    deck.section(
        title="Aula 3: Volume e Capacidade",
        subtitle="Cálculo de volume e relações com litros (30 min)",
        notes="Foco da aula: entender volume como espaço tridimensional e relacionar unidades de volume cúbico com capacidade em litros."
    )

    deck.image_text(
        title="O Princípio do Cálculo de Volume",
        path=ASSETS / "volume_capacidade.png",
        text_items=[
            "Volume = medida do espaço tridimensional ocupado",
            "Ideia intuitiva: empilhar fatias de área Ab até a altura h",
            "Fórmula Universal para qualquer prisma reto:",
            "V = Área da Base × Altura (V = Ab · h)",
            "1 m³ = 1.000 Litros  |  1 dm³ = 1 Litro  |  1 cm³ = 1 mL"
        ],
        notes=(
            "Explicar o Princípio de Cavalieri: se dois sólidos têm a mesma altura e seções transversais de áreas iguais em qualquer plano paralelo às bases, eles têm o mesmo volume."
        )
    )

    deck.manim_figure(
        title="Princípio do Volume por Extrusão (Manim)",
        path=MOTION_ASSETS / "manim_volume_extrusao.png",
        caption="Motion Design Manim: fatiamento contínuo em camadas empilhadas demonstrando V = Ab · h",
        side_text=[
            "Base poligonal com área superficial Ab",
            "Princípio de Cavalieri: camadas acumuladas",
            "Cada fatia infinitesimal adiciona volume na direção h",
            "Gradiente de cores SENAI marcando a altura acumulada",
            "Fórmula universal: Volume = Ab × h"
        ],
        notes="Mostrar que o mesmo raciocínio de empilhamento de folhas de papel ou lâminas vale para qualquer formato de base regular ou irregular."
    )

    deck.image_text(
        title="Volume de Blocos Retangulares",
        path=ASSETS / "paralelepipedo_cubo.png",
        text_items=[
            "Paralelepípedo Retângulo:",
            "V = comprimento × largura × altura",
            "V = c · l · h",
            "Cubo de aresta 'a':",
            "V = a · a · a = a³",
            "Basta multiplicar as três dimensões!"
        ],
        notes="Lembrar que todas as medidas devem estar na MESMA unidade antes de efetuar a multiplicação (todas em metros, ou todas em centímetros, etc.)."
    )

    deck.table(
        title="Tabela de Conversão: Volume x Capacidade",
        header=["Unidade de Volume", "Equivalência", "Exemplo Real do Dia a Dia"],
        rows=[
            ["1 metro cúbico (1 m³)", "1.000 Litros", "Caixas d'água residenciais, caminhões-pipa"],
            ["1 decímetro cúbico (1 dm³)", "1 Litro", "Caixa de leite longa vida, suco de 1 L"],
            ["1 centímetro cúbico (1 cm³)", "1 mililitro (1 mL)", "Seringas médicas, dosadores de remédios"],
            ["1.000 cm³", "1 Litro (1.000 mL)", "Garrafa de água mineral padrão"]
        ],
        col_widths=[2.5, 2.0, 3.5],
        notes=(
            "ALERTAR OS ALUNOS PARA O ERRO CLÁSSICO:\n"
            "- Muitos alunos pensam que 1 m³ = 100 L porque 1 m = 100 cm. Isso está ERRADO!\n"
            "- 1 m = 10 dm -> 1 m³ = (10 dm)³ = 1.000 dm³ = 1.000 Litros."
        )
    )

    deck.two_columns(
        title="Exemplo Resolvido 3: Caixa d'Água",
        left=[
            "Problema:",
            ("Uma caixa d'água tem a forma de um paralelepípedo com 2,0 m de comprimento, 1,5 m de largura e 1,2 m de altura.", 1),
            ("Quantos litros de água ela comporta quando está completamente cheia?", 1)
        ],
        right=[
            "Resolução:",
            ("1. Cálculo do volume em m³:", 1),
            ("V = comprimento × largura × altura", 2),
            ("V = 2,0 × 1,5 × 1,2 = 3,6 m³", 2),
            ("2. Conversão para litros:", 1),
            ("Como 1 m³ = 1.000 Litros:", 2),
            ("Capacidade = 3,6 × 1.000 = 3.600 Litros", 2)
        ],
        notes=(
            "MÉTODO EM DECÍMETROS:\n"
            "2,0 m = 20 dm; 1,5 m = 15 dm; 1,2 m = 12 dm.\n"
            "V = 20 × 15 × 12 = 3.600 dm³ = 3.600 Litros. Enfatizar a praticidade de converter para decímetros quando se quer a resposta direta em litros!"
        )
    )

    deck.image_text(
        title="Volume do Prisma de Base Triangular",
        path=ASSETS / "prisma_triangular.png",
        text_items=[
            "A base é um triângulo com base b e altura h_tri",
            "Área da base triangular: Ab = (b × h_tri) / 2",
            "Volume do prisma: V = Ab × h_prisma",
            "V = [(b × h_tri) / 2] × h_prisma",
            "Muito comum em telhados, calhas e rampas"
        ],
        notes="Atenção didática: diferenciar a altura da base triangular (h_tri) da altura do prisma (comprimento da peça)."
    )

    deck.highlight(
        title="Atividade 4 • Aquário da Escola",
        statement="Um aquário em formato de paralelepípedo possui 60 cm de comprimento, 40 cm de largura e 50 cm de altura. Se a água atinge 45 cm de altura dentro dele, quantos litros de água há no aquário?",
        items=[
            "Atenção: Use a altura da água (45 cm), não a altura total do aquário!",
            "Passo 1: Calcule o volume de água em cm³ (V = c · l · h_água)",
            "Passo 2: Converta cm³ para litros (lembre-se: 1.000 cm³ = 1 Litro)"
        ],
        notes=(
            "SOLUÇÃO COMPLETA DA ATIVIDADE 4:\n"
            "1. Dimensões ocupadas pela água:\n"
            "   Comprimento = 60 cm\n"
            "   Largura = 40 cm\n"
            "   Altura da água = 45 cm\n"
            "2. Cálculo do volume:\n"
            "   V = 60 × 40 × 45 = 108.000 cm³\n"
            "3. Conversão para Litros:\n"
            "   Como 1 L = 1.000 cm³:\n"
            "   Capacidade = 108.000 / 1.000 = 108 Litros de água."
        )
    )

    deck.blender_figure(
        title="Simulação 3D: Reservatório e Nível da Água (Blender)",
        path=MOTION_ASSETS / "blender_reservatorio_agua.png",
        caption="Modelagem física 3D Blender: reservatório em acrílico com bloco de água preenchendo o volume útil",
        side_text=[
            "Armação estrutural em azul SENAI acetinado",
            "Volume de água com material translúcido e refração física",
            "Apenas a altura da água (45 cm) conta para a capacidade",
            "Espaço livre superior (5 cm) evita transbordamento",
            "Volume calculado: 60 × 40 × 45 cm³ = 108 Litros"
        ],
        notes="A imagem 3D em estúdio reforça o cuidado prático na engenharia: reservatórios nunca devem ser calculados apenas pela borda superior quando há limite de nível."
    )

    # =========================================================================
    # AULA 4: APLICAÇÕES PRÁTICAS E REVISÃO
    # =========================================================================
    deck.section(
        title="Aula 4: Aplicações e Desafios",
        subtitle="Problemas integrados de área e volume, síntese e revisão (30 min)",
        notes="Nesta última aula, os alunos integram os dois conceitos e aprendem a decidir quando o problema exige cálculo de área e quando exige volume."
    )

    deck.comparison(
        title="Área versus Volume: Não Confunda!",
        left_title="Área (Superfície)",
        left=[
            "Mede a casca / superfície externa",
            "Unidade bidimensional: cm², m²",
            "Aplicações típicas:",
            ("Pintura de paredes e caixas", 1),
            ("Quantidade de papelão ou tecido", 1),
            ("Revestimento com azulejos", 1),
            "Fórmula: At = Al + 2·Ab"
        ],
        right_title="Volume (Capacidade)",
        right=[
            "Mede o espaço interno / preenchimento",
            "Unidade tridimensional: cm³, m³, Litros",
            "Aplicações típicas:",
            ("Capacidade de água ou combustível", 1),
            ("Quantidade de concreto em uma viga", 1),
            ("Espaço de ar no interior da sala", 1),
            "Fórmula: V = Ab · h"
        ],
        notes="Quadro de fixação essencial para evitar erros em avaliações e no cotidiano."
    )

    deck.two_columns(
        title="Exemplo Resolvido 4: Embalagem Tetra Pak",
        left=[
            "Dados da Embalagem:",
            ("Uma embalagem de suco tem o formato de prisma reto de base quadrada com 7 cm de aresta e 20 cm de altura.", 1),
            ("a) Qual é o volume em mL?", 1),
            ("b) Quantos cm² de papelão são gastos na embalagem?", 1)
        ],
        right=[
            "Resolução Integrada:",
            ("a) Volume (Capacidade):", 1),
            ("Ab = 7 × 7 = 49 cm²", 2),
            ("V = 49 × 20 = 980 cm³ = 980 mL (~1 Litro)", 2),
            ("b) Área Total (Material):", 1),
            ("Al = (4 × 7) × 20 = 28 × 20 = 560 cm²", 2),
            ("At = 560 + 2 × (49) = 658 cm²", 2)
        ],
        notes="Mostrar aos alunos como a indústria de embalagens precisa otimizar a relação Área/Volume para economizar papelão e transportar o máximo de produto."
    )

    deck.highlight(
        title="Atividade 5 • A Tenda de Camping",
        statement="Uma tenda tem a forma de um prisma triangular reto com 3,0 m de comprimento. A frente da tenda é um triângulo isósceles com base de 2,0 m e altura de 1,5 m. Calcule o volume de ar no interior da tenda.",
        items=[
            "Passo 1: Identifique a base do prisma (triângulo com base b = 2,0 m e altura h_tri = 1,5 m)",
            "Passo 2: Calcule a área da base triangular (Ab = b · h_tri / 2)",
            "Passo 3: Multiplique pela extensão da tenda (altura do prisma h = 3,0 m)"
        ],
        notes=(
            "SOLUÇÃO COMPLETA DA ATIVIDADE 5:\n"
            "1. Área da base triangular (frente da tenda):\n"
            "   Ab = (base × altura do triângulo) / 2\n"
            "   Ab = (2,0 m × 1,5 m) / 2 = 3,0 / 2 = 1,5 m²\n"
            "2. Volume de ar no interior da tenda (h_prisma = 3,0 m):\n"
            "   V = Ab × h_prisma\n"
            "   V = 1,5 m² × 3,0 m = 4,5 m³\n"
            "3. Capacidade equivalente em litros:\n"
            "   4,5 m³ × 1.000 = 4.500 Litros de ar."
        )
    )

    deck.table(
        title="Quadro Resumo de Fórmulas dos Prismas",
        header=["Tipo de Prisma", "Área da Base (Ab)", "Área Lateral (Al)", "Área Total (At)", "Volume (V)"],
        rows=[
            ["Prisma Reto Geral", "Área do polígono", "2p_base × h", "Al + 2·Ab", "Ab × h"],
            ["Paralelepípedo (a,b,c)", "a · b", "2(ac + bc)", "2(ab + ac + bc)", "a · b · c"],
            ["Cubo (aresta a)", "a²", "4a²", "6a²", "a³"],
            ["Prisma Triangular", "(b · h_tri) / 2", "(L1+L2+L3) × h", "Al + 2·Ab", "Ab × h"]
        ],
        col_widths=[2.2, 1.8, 1.8, 2.0, 1.6],
        notes="Tabela de consulta rápida para os alunos levarem para os estudos e avaliações."
    )

    deck.closing(
        title="Parabéns!",
        subtitle="Unidade Curricular: Matemática • Prismas: Área e Volume concluído!",
        notes="Encerrar a 4ª aula parabenizando a turma e indicando a lista complementar de exercícios para fixação."
    )

    out = deck.save(OUT_PPTX)
    print(f"Apresentação gerada com sucesso em: {out}")
    return out

if __name__ == "__main__":
    build_deck()
