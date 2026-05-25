"""
Ponto de entrada CLI para seeds de desenvolvimento.

Uso:
    python scripts/seed.py               # seed padrão (dev)
    python scripts/seed.py --env prod    # apenas ativa se DATABASE_URL apontar para prod
                                         # (seed de prod não existe — bloqueia por segurança)
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from nexo.seeds.seed_dev import run


def main() -> None:
    parser = argparse.ArgumentParser(description="Nexo seed runner")
    parser.add_argument(
        "--env",
        choices=["dev"],
        default="dev",
        help="Ambiente alvo (apenas 'dev' disponível)",
    )
    args = parser.parse_args()

    if args.env != "dev":
        print("Seed de produção não disponível. Use scripts de ETL manuais.", file=sys.stderr)
        sys.exit(1)

    run()


if __name__ == "__main__":
    main()
