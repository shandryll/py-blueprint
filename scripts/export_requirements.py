#!/usr/bin/env python3
"""
Gera requirements.txt e requirements-dev.txt a partir do pyproject.toml
(somente dependências diretas, sem transitivas — fácil de ler e manter).
"""
from pathlib import Path

import tomllib

ROOT = Path(__file__).resolve().parent.parent
PYPROJECT = ROOT / "pyproject.toml"


def main() -> None:
    with open(PYPROJECT, "rb") as f:
        data = tomllib.load(f)

    project = data["project"]
    deps: list[str] = project.get("dependencies", [])
    optional = project.get("optional-dependencies", {})
    dev_deps: list[str] = optional.get("dev", [])

    header = (
        "# Gerado a partir de pyproject.toml (dependências diretas).\n"
        "# Para atualizar: make requirements\n\n"
    )

    # Produção: só runtime
    req_path = ROOT / "requirements.txt"
    req_path.write_text(header + "\n".join(deps) + "\n", encoding="utf-8")
    print(f"Escrito: {req_path.name} ({len(deps)} pacotes)")

    # Desenvolvimento: runtime + dev
    all_dev = deps + dev_deps
    dev_path = ROOT / "requirements-dev.txt"
    dev_path.write_text(header + "\n".join(all_dev) + "\n", encoding="utf-8")
    print(f"Escrito: {dev_path.name} ({len(all_dev)} pacotes)")


if __name__ == "__main__":
    main()
