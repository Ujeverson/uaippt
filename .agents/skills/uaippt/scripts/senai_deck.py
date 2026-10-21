"""senai_deck.py — módulo legado mantido para retrocompatibilidade.
Importa e reexporta tudo de uaippt_deck.py.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from uaippt_deck import (
    UaipptDeck, SenaiDeck, build_from_outline, TEMPLATE,
    AZUL, LARANJA, PETROLEO, CIANO, CINZA, TEXTO, AZUL_CLARO, CODE_BG, CODE_FG,
    DEFAULT_PROFESSOR, DEFAULT_COURSE, AREA
)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    print(build_from_outline(data, sys.argv[2] if len(sys.argv) > 2 else None))
