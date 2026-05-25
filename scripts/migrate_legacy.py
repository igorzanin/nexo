"""
Migração de dados legados para o banco alvo.

Como definido em data_migration_plan.md (estratégia Big Bang Controlado),
este projeto não possui dados de produção para migrar — é um novo deployment.

Para ambientes com dados legados do Focalboard, descomente e adapte os
blocos de ETL abaixo, que seguem o mapeamento declarado em data_migration_plan.md.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


def migrate_from_focalboard(legacy_dsn: str, target_dsn: str) -> None:
    """
    ETL de dados legados do Focalboard SQLite → PostgreSQL alvo.

    Passos (conforme data_migration_plan.md):
      1. Extrair users → nexo.users
      2. Extrair teams → nexo.teams
      3. Extrair boards → nexo.boards (remapear campos snake_case)
      4. Extrair blocks → nexo.blocks (remapear root_id, parent_id)
      5. Extrair categories → nexo.categories
      6. Extrair sharing → nexo.sharing
      7. Extrair preferences → nexo.preferences
      8. Extrair file_info → nexo.file_info

    Todos os timestamps devem ser preservados como-estão (já em ms Unix BigInt).
    IDs são TEXT no legado; manter como-estão.
    """
    raise NotImplementedError(
        "Sem dados de produção para migrar (Big Bang Controlado). "
        "Implemente este método se tiver um dump legado do Focalboard."
    )


if __name__ == "__main__":
    print("Nenhum dado legado para migrar neste ambiente.")
    print("Use 'python scripts/seed.py' para popular o banco de dev.")
    sys.exit(0)
