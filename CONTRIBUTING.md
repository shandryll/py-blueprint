# Guia de Contribuição

Obrigado por considerar contribuir para o Py-Blueprint! Este documento fornece diretrizes para contribuir com o projeto.

## Como Contribuir

### 1. Configuração do Ambiente

1. Faça um fork do repositório
2. Clone seu fork: `git clone <seu-fork-url>`
3. Crie um ambiente virtual: `make venv`
4. Instale as dependências: `make install-dev`
5. Instale os hooks de pre-commit: `make pre-commit-install`

### 2. Processo de Desenvolvimento

1. Crie uma branch para sua feature: `git checkout -b feature/minha-feature`
2. Faça suas alterações
3. Execute os testes: `make test`
4. Verifique o linting: `make lint`
5. Formate o código: `make format`
6. Commit suas alterações: `git commit -m "feat: adiciona nova feature"`
7. Push para sua branch: `git push origin feature/minha-feature`
8. Abra um Pull Request

### 3. Padrões de Código

- Siga o estilo de código definido pelo Ruff
- Use type hints em todas as funções
- Escreva docstrings para módulos, classes e funções públicas
- Mantenha a cobertura de testes acima de 80%

### 4. Commits

Use mensagens de commit descritivas seguindo o padrão Conventional Commits:

- `feat:` Nova funcionalidade
- `fix:` Correção de bug
- `docs:` Documentação
- `style:` Formatação
- `refactor:` Refatoração
- `test:` Testes
- `chore:` Tarefas de manutenção

### 5. Testes

- Escreva testes para novas funcionalidades
- Mantenha a cobertura de testes
- Execute `make test` antes de fazer commit

### 6. Pull Requests

- Descreva claramente o que foi alterado
- Referencie issues relacionadas, se houver
- Certifique-se de que todos os testes passam
- Aguarde a revisão antes de fazer merge

## Dúvidas?

Se tiver dúvidas, abra uma issue no repositório.

