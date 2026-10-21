# uaippt 🚀

> **Gerador inteligente de apresentações PowerPoint (.pptx) no padrão visual oficial SENAI / Faculdade SENAI Fatesg com Motion Design (Manim & Blender) e Skill para AI Coding Agents.**

[![npm version](https://img.shields.io/npm/v/uaippt.svg?color=0E4194)](https://www.npmjs.com/package/uaippt)
[![License: MIT](https://img.shields.io/badge/License-MIT-E8490F.svg)](https://opensource.org/licenses/MIT)
[![Node.js](https://img.shields.io/badge/Node.js-%3E%3D16.0.0-339933.svg?logo=node.js)](https://nodejs.org/)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB.svg?logo=python)](https://python.org/)
[![SENAI / Fatesg](https://img.shields.io/badge/SENAI-Faculdade%20Fatesg-0E4194.svg)](https://senaigoias.com.br/)

---

## ✨ Principais Recursos

- 🎨 **Identidade Visual Oficial SENAI / Fatesg:** Formato widescreen 16:9 (13,33" × 7,50"), banner de circuitos integrado ao mestre, logotipo SENAI 2024, rodapé institucional Fatesg e paleta oficial (Azul `#0E4194`, Laranja acento `#E8490F`, Petróleo `#074982`, Ciano `#4FB3D9`, Azul Claro `#E8EEF7`).
- 👨‍🏫 **Identificação Docente Exclusiva na Capa:** A skill e o CLI coletam obrigatoriamente o nome do(a) professor(a) responsável e o curso/disciplina, inserindo-os **exclusivamente no slide de capa**, mantendo as lâminas de conteúdo e encerramento limpos.
- 📐 **Calibragem Tipográfica Inteligente (*Autofit*):** Algoritmo que calcula dinamicamente o maior corpo de fonte legível (Aptos/Aptos Display), prevenindo estouro de caixas de texto.
- 🎬 **Motion Design com Manim & Blender:**
  - **Manim (CE):** Animações matemáticas vetoriais, deduções dinâmicas passo a passo e planificações geométricas desdobradas.
  - **Blender (`bpy` LTS Headless):** Modelagem procedural 3D com materiais PBR (Azul SENAI acetinado, acrílico, água translúcida), estúdio com iluminação *three-point*, fundo transparente real e rotações 360° em loop contínuo (*Turntables*).
- 🤖 **Skill Pronta para AI Coding Agents:** Projetada nativamente para **Google Antigravity**, **Claude Code**, **Cursor** e **GitHub Copilot**.
- 📦 **Multiplataforma:** Utilize via terminal npm (`npx uaippt`), biblioteca Python (`from uaippt_deck import UaipptDeck`) ou roteiro JSON.

---

## 🚀 Instalação Rápida

### 1. Via npm (Global ou npx)

Para usar a CLI interativa em qualquer projeto:

```bash
# Execução direta sem instalação:
npx uaippt create

# Ou instalação global:
npm install -g uaippt
```

### 2. Dependências Python

O núcleo de geração requer Python 3.10+:

```bash
pip install python-pptx pygments
```

*(Opcional para Motion Design avançado: `pip install manim bpy imageio-ffmpeg`)*

---

## 💻 Como Usar

### Modo 1: CLI Interativo (npx)

Crie uma apresentação completa respondendo às perguntas do terminal:

```bash
npx uaippt create minha_aula.pptx
```

O assistente solicitará:
1. **Título da apresentação**
2. **Subtítulo**
3. **Nome do(a) Professor(a)** *(obrigatório para constar na capa)*
4. **Unidade Curricular / Curso**

---

### Modo 2: Como Skill de AI Coding Agents (Google Antigravity, Cursor, Claude)

Instale a skill diretamente na pasta do seu workspace:

```bash
npx uaippt init
```

A pasta `.agents/skills/uaippt/` será criada com toda a especificação [`SKILL.md`](.agents/skills/uaippt/SKILL.md), scripts e template mestre. O agente de IA passará a acioná-la automaticamente sempre que você pedir slides ou aulas do SENAI.

---

### Modo 3: Como Biblioteca Python (`uaippt_deck`)

```python
import sys
from pathlib import Path

# Importa a biblioteca do uaippt
from uaippt_deck import UaipptDeck

deck = UaipptDeck()

# 1. Capa: Nome do professor e curso aparecem apenas aqui
deck.cover(
    title="Prismas: Área e Volume",
    subtitle="Geometria Espacial • 9º Ano",
    course="Matemática — Ensino Fundamental",
    professor="Prof. Msc. Ujeverson Tavares",
    notes="Anotações para o professor conduzir a abertura da aula."
)

# 2. Tópicos com marcadores hierárquicos
deck.bullets("Objetivos da Aula", [
    "Compreender a definição geométrica de um prisma reto",
    ("Identificar bases, faces laterais e arestas", 1),
    "Deduzir as fórmulas de Área Lateral (Al) e Área Total (At)",
    "Calcular volumes e converter para litros"
])

# 3. Divisória de seção
deck.section("Aula 1: O que é um Prisma?", "Definição geométrica e classificação")

# 4. Caixa de destaque
deck.highlight(
    title="Definição de Prisma Reto",
    statement="Prisma é um poliedro com duas bases poligonais congruentes e paralelas cujas faces laterais são retângulos perpendiculares às bases.",
    items=["As bases determinam o nome do prisma", "Arestas laterais correspondem à altura h"]
)

# 5. Motion Design 3D com Blender (2 colunas: texto + render)
deck.blender_figure(
    title="Estrutura e Decomposição: Vista Explodida 3D",
    path="assets/motion_renders/blender_vista_explodida.png",
    caption="Modelagem 3D física Blender: bases poligonais e faces laterais separadas no espaço",
    side_text=[
        "Duas bases paralelas em destaque (laranja SENAI)",
        "Faces laterais retangulares conectando os vértices",
        "Abertura espacial facilita a contagem de elementos",
        "Comprova visualmente a Relação de Euler: V - A + F = 2"
    ]
)

# 6. Motion Design com Manim (Planificação geométrica)
deck.manim_figure(
    title="Planificação Dinâmica da Superfície",
    path="assets/motion_renders/manim_planificacao.png",
    caption="Animação matemática vetorial Manim: desdobramento contínuo com cotas de altura e perímetro",
    side_text=[
        "Desdobramento contínuo das faces no plano",
        "Área lateral (Al): retângulo contínuo de base 2p e altura h",
        "Área das bases: topo e fundo adicionados",
        "Fórmula universal: At = Al + 2·Ab"
    ]
)

# 7. Slide de encerramento institucional (sem duplicação de autoria)
deck.closing(
    title="Parabéns!",
    subtitle="Unidade Curricular: Matemática • Bons estudos!"
)

# Salva o arquivo final
deck.save("Prismas_Area_e_Volume.pptx")
```

---

### Modo 4: CLI via Roteiro JSON

Gere apresentações completas a partir de especificações estruturadas em JSON:

```bash
python scripts/uaippt_deck.py roteiro.json apresentacao.pptx
```

*Exemplo de roteiro disponível em [`examples/exemplo_aula.json`](.agents/skills/uaippt/examples/exemplo_aula.json).*

---

## 📊 Métodos de Slide Disponíveis

| Método | Finalidade | Descrição |
|---|---|---|
| `cover(title, subtitle, course, professor)` | Capa | Banner superior, título de grande impacto, subtítulo com docente e curso, e rodapé institucional Fatesg. |
| `section(title, subtitle)` | Divisória | Transição entre módulos e tópicos com barra de acento laranja. |
| `bullets(title, items)` | Conteúdo | Lista hierárquica automática com marcadores oficiais SENAI. |
| `two_columns(title, left, right)` | 2 Colunas | Dois blocos paralelos de texto ou listas. |
| `comparison(title, lt, left, rt, right)` | Comparativo | Prós × Contras, Antes × Depois, Conceito × Aplicação Prática. |
| `highlight(title, statement, items)` | Destaque | Caixa com moldura azul clara e barra laranja para teoremas, regras e conceitos centrais. |
| `code(title, code, language, caption)` | Código-fonte | Bloco escuro de código com realce de sintaxe via `pygments`. |
| `table(title, header, rows, col_widths)` | Tabela | Cabeçalho azul SENAI e linhas zebradas com contraste balanceado. |
| `image(title, path, caption)` | Imagem | Imagem centralizada com proporção mantida e legenda inferior. |
| `image_text(title, path, text_items)` | Imagem Lateral | Foto grande à direita e itens descritivos à esquerda. |
| `motion_figure(title, path, caption, side_text)` | Motion Design | Insere render estático (PNG transparente), animação em loop (GIF) ou vídeo (MP4) com layout de 2 colunas. |
| `manim_figure(...)` | Manim | Atalho semântico para deduções matemáticas e fórmulas. |
| `blender_figure(...)` | Blender | Atalho semântico para sólidos, modelos físicos e iluminação de estúdio 3D. |
| `closing(title, subtitle)` | Encerramento | Slide final com identidade visual e contato institucional. |

---

## 📁 Estrutura do Repositório

```
uaippt/
├── bin/
│   └── uaippt.js            # Executável do CLI npm / npx
├── .agents/skills/uaippt/   # Skill oficial para AI Agents
│   ├── SKILL.md             # Instruções e diretrizes para o agente
│   ├── assets/
│   │   ├── template.pptx    # Template mestre 16:9 oficial
│   │   ├── logo_senai.png   # Marca SENAI 2024 colorida
│   │   ├── rodape_fatesg.png# Faixa institucional Fatesg
│   │   └── motion_renders/  # Biblioteca de renders 3D e animações
│   ├── scripts/
│   │   ├── uaippt_deck.py   # Motor principal em Python
│   │   ├── senai_deck.py    # Módulo de compatibilidade legada
│   │   ├── motion_manim.py  # Gerador de cenas e deduções Manim
│   │   ├── motion_blender.py# Motor 3D procedural e estúdio Blender
│   │   ├── render_preview.ps1# Script de validação visual de slides
│   │   └── build_template.py# Utilitário de regeneração do mestre
│   └── examples/
│       ├── exemplo_aula.json# Roteiro de exemplo
│       └── exemplo_aula.pptx# Apresentação gerada
├── package.json             # Manifesto npm
├── LICENSE                  # Licença MIT
└── README.md                # Este documento
```

---

## 📄 Licença

Distribuído sob a licença **MIT**. Consulte o arquivo [`LICENSE`](LICENSE) para obter mais informações.

---

## 👨‍💻 Autor e Mantenedor

**Prof. Msc. Ujeverson Tavares**  
- **GitHub:** [@Ujeverson](https://github.com/Ujeverson)
- **Repositório:** [https://github.com/Ujeverson/uaippt](https://github.com/Ujeverson/uaippt)
- **Faculdade SENAI Fatesg / Sistema FIEG** — Goiânia, GO
