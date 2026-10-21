---
name: uaippt
description: Template PowerPoint oficial SENAI / Faculdade SENAI Fatesg para gerar apresentações .pptx com banner de circuitos, logo SENAI, rodapé institucional Fatesg, paleta da marca e Motion Design (Manim e Blender). SEMPRE pergunte ao usuário o nome do(a) professor(a) responsável para ser inserido na capa caso não tenha sido informado. Use SEMPRE que o usuário pedir slides, apresentação, PowerPoint, PPT ou pptx para aula, disciplina, unidade curricular, curso, palestra, banca, projeto integrador ou qualquer material do SENAI, FIEG ou Fatesg — mesmo que não mencione "template".
---

# uaippt — Gerador de Apresentações SENAI / Fatesg & Motion Design

Template oficial: `assets/template.pptx` — Formato 16:9 (13,33" × 7,50"), 1 mestre, 11 layouts, 0 slides.
Biblioteca nativa: `scripts/uaippt_deck.py` (classe `UaipptDeck`, com alias de compatibilidade `SenaiDeck`).
**Prefira sempre a biblioteca** em vez de montar `python-pptx` do zero: ela respeita rigorosamente as áreas de segurança, a paleta de cores institucional, a tipografia corporativa e calcula automaticamente o ajuste de tamanho de fonte (*autofit* calibrado).

Dependências Python: `pip install python-pptx` (opcionais: `pygments` para colorir código, `manim` e `bpy` para Motion Design).

---

## Regra Mandatória: Identificação do Docente na Capa

> [!IMPORTANT]
> **Coleta do Nome do(a) Professor(a):**
> Sempre que o usuário solicitar a criação de slides, aula ou apresentação:
> 1. Verifique se o nome do(a) professor(a) foi expressamente fornecido no prompt.
> 2. Se o nome **NÃO** tiver sido informado, **a skill DEVE PERGUNTAR ao usuário antes de gerar**:
>    *"Qual é o nome do(a) professor(a) responsável pela apresentação para constar na capa?"*
> 3. O nome coletado será inserido **exclusivamente na capa** (`deck.cover(..., professor="Nome Informado")`).
> 4. **NUNCA** repita o nome do(a) professor(a) nos slides de conteúdo ou no slide de encerramento (`deck.closing()`).

---

## Identidade Visual Oficial (SENAI / Fatesg)

| Elemento | Onde | Observação |
|---|---|---|
| Banner de circuitos + logo SENAI | Fundo do mestre, y = 0,00"–1,00" | Presente em todos os slides. **Nenhum elemento pode ser colocado acima de y = 1,00".** |
| Rodapé Faculdade SENAI Fatesg | Layout de capa, y = 6,82"–7,50" | Inserido automaticamente em `cover()` e `closing()`. |
| Títulos | Azul SENAI `#0E4194` | Fonte do tema: Aptos Display / Aptos. |

### Paleta de Cores (constantes em `uaippt_deck.py`)
- **Azul SENAI:** `#0E4194` (cor primária da marca e títulos)
- **Laranja SENAI:** `#E8490F` (acentos, filetes e destaques — use com moderação)
- **Petróleo:** `#074982` (linhas estruturais do banner de circuitos)
- **Ciano:** `#4FB3D9` (setas e direcionadores do banner)
- **Cinza Corporativo:** `#575656` (subtítulos e legendas)
- **Texto Corrido:** `#262626` (alta legibilidade em leitura contínua)
- **Azul Claro Suave:** `#E8EEF7` (fundo de cartões de destaque e linhas alternadas de tabelas)

---

## Fluxo de Trabalho Recomendado

1. **Identificação e Planejamento:**
   - Pergunte o nome do(a) professor(a) caso não tenha sido informado.
   - Planeje o roteiro: Capa → Cronograma/Objetivos → Divisórias de Seção → Conteúdo Expositivo → Exemplos Resolvidos Passo a Passo → Atividades Didáticas (com resoluções completas nas Anotações) → Síntese/Tabela → Encerramento.
2. **Geração:** Crie o deck via script Python (`UaipptDeck`) ou roteiro JSON CLI.
3. **Motion Design (Opcional & Recomendado para Exatas e Técnicas):**
   - Use **Manim** (`motion_manim.py`) para deduções vetoriais, planificações geométricas e animações matemáticas.
   - Use **Blender** (`motion_blender.py`) para sólidos 3D, vistas explodidas, modelos físicos em estúdio e loops 360°.
4. **Renderização e Validação Visual (Passo Obrigatório):**
   ```powershell
   powershell -ExecutionPolicy Bypass -File scripts/render_preview.ps1 -Pptx saida.pptx
   ```
   Gera imagens em `preview_<nome>/slideNN.png` para checagem de alinhamento, legibilidade e ausência de sobreposição com o banner.

---

## Uso em Python

```python
import sys
from pathlib import Path
sys.path.insert(0, r"<caminho-da-skill>/scripts")
from uaippt_deck import UaipptDeck

deck = UaipptDeck()

# Capa: curso e professor preenchidos na capa exclusivamente
deck.cover(
    title="Introdução à Programação em Python",
    subtitle="Aula 1 — Variáveis e Tipos de Dados",
    course="Análise e Desenvolvimento de Sistemas",
    professor="Prof. Msc. Ujeverson Tavares",
    notes="Anotações do professor: introduzir os conceitos com exemplos do dia a dia."
)

deck.bullets("Objetivos da Aula", [
    "Compreender o conceito de variável e espaço de memória",
    ("Nome, valor e tipos primitivos (int, float, str, bool)", 1),
    "Aprender a receber entradas do usuário e exibir saídas",
])

deck.section("Variáveis na Memória", "Como o computador armazena dados")

deck.highlight(
    title="Conceito-Chave",
    statement="Variável é um espaço nomeado na memória que armazena temporariamente um valor durante a execução.",
    items=["O tipo de dado é inferido dinamicamente pelo Python", "Adote nomes autoexplicativos seguindo o padrão snake_case"]
)

deck.code(
    title="Exemplo em Código",
    code='nome = "Aluno SENAI"\nidade = 20\nprint(f"Olá {nome}, você tem {idade} anos.")',
    language="python",
    caption="Execute no terminal interativo ou no Google Colab"
)

deck.table(
    title="Tipos Primitivos em Python",
    header=["Tipo", "Descrição", "Exemplo"],
    rows=[
        ["int", "Números inteiros positivos ou negativos", "42, -5"],
        ["float", "Números com casas decimais (ponto flutuante)", "3.1415, 99.90"],
        ["str", "Texto delimitado por aspas simples ou duplas", '"SENAI Fatesg"'],
        ["bool", "Valores lógicos de verdadeiro ou falso", "True, False"]
    ],
    col_widths=[1.5, 4.0, 2.5]
)

deck.closing(
    title="Obrigado!",
    subtitle="Faculdade SENAI Fatesg • Dúvidas? Fale com o professor"
)

deck.save("aula1_python.pptx")
```

---

## Métodos Disponíveis na Classe `UaipptDeck`

| Método | Layout | Quando usar |
|---|---|---|
| `cover(title, subtitle, course, professor)` | [0] Título | Capa institucional com rodapé Fatesg, filete laranja, professor e curso. |
| `section(title, subtitle)` | [2] Seção | Divisória entre módulos ou tópicos da aula. |
| `bullets(title, items)` | [1] Conteúdo | Lista hierárquica (nível 0 e nível 1 com subitens). |
| `two_columns(title, left, right)` | [3] Duas Colunas | Comparação ou blocos conceituais paralelos. |
| `comparison(title, lt, left, rt, right)` | [4] Comparação | Prós × Contras, Antes × Depois, Certo × Errado. |
| `highlight(title, statement, items)` | [5] Caixa Destaque | Leis, princípios, definições essenciais ou desafios. |
| `code(title, code, language, caption)` | [5] Código Escuro | Trechos de código com realce sintático pygments. |
| `table(title, header, rows, col_widths)` | [5] Tabela | Tabelas com cabeçalho azul SENAI e zebrado suave. |
| `image(title, path, caption)` | [5] Imagem Central | Diagramas e capturas com proporção preservada. |
| `image_text(title, path, text_items)` | [8] Imagem Legenda | Foto grande à direita e itens descritivos à esquerda. |
| `motion_figure(title, path, caption, side_text, media_side)` | [5] Motion Hero/Duplo | Mídias dinâmicas (PNG alta definição, GIF animado em loop ou vídeo MP4). Se `side_text` for fornecido, monta layout em 2 colunas. |
| `manim_figure(title, path, ...)` | [5] Manim | Atalho semântico para deduções e animações matemáticas Manim. |
| `blender_figure(title, path, ...)` | [5] Blender | Atalho semântico para renderizações 3D procedurais em Blender (`bpy`). |
| `closing(title, subtitle)` | [0] Encerramento | Slide final com rodapé institucional (sem dados docentes). |

*Todos os métodos aceitam `notes="..."` com anotações e roteiro para o apresentador.*

---

## Motion Design com Manim e Blender (3D & Animações)

A skill integra dois motores de computação gráfica de ponta:

1. **Manim (Community Edition):**
   - Criação de animações vetoriais matemáticas de alta resolução (1920×1080).
   - Focado em deduções visuais passo a passo, desdobramento de sólidos (planificação) e demonstração de teoremas (ex: Princípio de Cavalieri e extrusão de volume).
   - Módulo: `scripts/motion_manim.py`.
2. **Blender (`bpy` LTS Headless):**
   - Modelagem 3D procedural e renderização física com estúdio virtual *Three-Point Lighting*.
   - Materiais PBR oficiais SENAI (Azul acetinado, Laranja reflexivo, Acrílico e Água translúcida com refração física).
   - Gera imagens estáticas em altíssima definição com fundo 100% transparente (`film_transparent = True`) e GIFs animados com giro 360° (*Turntable Loop*).
   - Módulo: `scripts/motion_blender.py`.

### Exemplo de Uso nos Slides:
```python
# Mídia 3D com texto de apoio em 2 colunas
deck.blender_figure(
    title="Rotação 3D do Prisma Regular (Blender)",
    path="assets/motion_renders/blender_prisma_hex_loop.gif",
    caption="Motion Design 3D com Blender: rotação 360° em estúdio com fundo transparente",
    side_text=[
        "Sólido tridimensional em estúdio virtual",
        "Duas bases regulares idênticas e paralelas",
        "Faces laterais retangulares conectando os vértices",
        "Chanfro (bevel) destacado pela luz de contorno"
    ],
    notes="Apresentar o prisma girando para evidenciar a congruência das bases."
)
```

---

## CLI e Execução via Roteiro JSON

Você pode gerar apresentações completas via linha de comando:

```powershell
python scripts/uaippt_deck.py roteiro.json saida.pptx
```

Se o campo `"professor"` não constar no arquivo JSON, o terminal solicitará interativamente o nome do(a) professor(a).

Exemplo de roteiro JSON em `examples/exemplo_aula.json`.

---

## Publicação e Pacotes

- **Repositório GitHub:** [https://github.com/Ujeverson/uaippt](https://github.com/Ujeverson/uaippt)
- **Pacote npm:** [https://www.npmjs.com/package/uaippt](https://www.npmjs.com/package/uaippt)
- **Comando global npm:** `npx uaippt` ou `npm install -g uaippt`

---

## Estrutura de Arquivos da Skill

```
uaippt/
├── SKILL.md                 # Especificação e guia oficial da skill
├── assets/
│   ├── template.pptx        # Template oficial calibrado (16:9)
│   ├── logo_senai.png       # Marca oficial SENAI 2024
│   ├── rodape_fatesg.png    # Faixa institucional de contato Fatesg
│   └── motion_renders/      # Modelos e renders Manim e Blender (PNG, GIF)
├── scripts/
│   ├── uaippt_deck.py       # Biblioteca principal + CLI JSON
│   ├── senai_deck.py        # Módulo proxy de retrocompatibilidade
│   ├── motion_manim.py      # Motor de animações matemáticas vetoriais com Manim
│   ├── motion_blender.py    # Motor de modelagem e render 3D em estúdio Blender
│   ├── render_preview.ps1   # Script de conferência visual automática de slides
│   └── build_template.py    # Gerador/ajustador de template mestre
└── examples/
    ├── exemplo_aula.json    # Exemplo de roteiro completo em JSON
    └── exemplo_aula.pptx    # Apresentação gerada pelo roteiro
```
