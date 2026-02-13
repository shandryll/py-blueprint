# Guia de Contribuição

Obrigado por considerar contribuir para o Py-Blueprint. Este guia resume como configurar o ambiente, rodar checks e enviar contribuições.

---

## 1. Configurar o ambiente

1. Faça um **fork** do repositório e clone o seu fork.
2. Crie e ative o ambiente virtual:
   ```bash
   uv venv
   # Ativar: source .venv/bin/activate (Linux/Mac) ou .venv\Scripts\Activate.ps1 (Windows)
   ```
   *(Alternativa com pip: `python -m venv .venv` e ative o `.venv`.)*
3. Instale as dependências:
   ```bash
   uv sync --dev
   ```
   *(Com pip: `pip install -e ".[dev]"`.)*
4. *(Opcional)* Hooks de pre-commit: `uv run pre-commit install`

---

## 2. Fluxo de desenvolvimento

1. Crie uma branch: `git checkout -b feature/minha-feature` (ou `fix/...`, `docs/...`).
2. Faça suas alterações no código.
3. Rode os testes:
   ```bash
   make test
   # ou: uv run pytest -v
   ```
4. Rode lint e formatação:
   ```bash
   make lint
   make format
   ```
   *(Ou: `uv run ruff check . --fix` e `uv run ruff format .`.)*
5. Faça commit, push e abra um **Pull Request** na branch correspondente.

Antes do PR, garanta que **todos os testes passam** e o código está **lintado e formatado**.

---

## 3. Padrões de código

- **Estilo**: siga o Ruff (configurado no `pyproject.toml`).
- **Tipos**: use type hints em funções e métodos públicos.
- **Documentação**: docstrings em módulos, classes e funções públicas.
- **Testes**: escreva testes para novas funcionalidades; mantenha a cobertura em nível aceitável (ex.: ≥ 80% quando aplicável).

---

## 4. Commits

Use **Conventional Commits** para facilitar o histórico e o changelog:

| Prefixo   | Uso                |
|-----------|--------------------|
| `feat:`   | Nova funcionalidade |
| `fix:`    | Correção de bug     |
| `docs:`   | Só documentação     |
| `style:`  | Formatação (sem lógica) |
| `refactor:` | Refatoração       |
| `test:`   | Testes              |
| `chore:`  | Manutenção (deps, CI, etc.) |

Exemplo: `feat: adiciona filtro por categoria em produtos`.

---

## 5. Pull Requests

- Descreva de forma clara o que foi alterado e por quê.
- Referencie issues relacionadas (ex.: `Closes #42`).
- Certifique-se de que os testes e o lint passam (localmente e no CI).

---

## Dúvidas

Se tiver dúvidas, abra uma **issue** no repositório.
