# Requirements - Organização de Dependências

Esta pasta contém os arquivos de dependências organizados para uso com `pip`.

## Estrutura

- **`base.txt`**: Dependências de runtime (produção)
- **`dev.txt`**: Dependências de desenvolvimento (inclui base.txt + ferramentas de dev)

## Uso

### Instalação de dependências de produção

```bash
pip install -r requirements/base.txt
```

### Instalação de dependências de desenvolvimento

```bash
pip install -r requirements/dev.txt
```

## Sincronização com pyproject.toml

Os arquivos nesta pasta devem ser mantidos sincronizados com `pyproject.toml`:

- `base.txt` ↔ `[project] dependencies`
- `dev.txt` ↔ `[project.optional-dependencies] dev`

## Nota sobre UV

Se você estiver usando `uv` (recomendado), as dependências são gerenciadas automaticamente pelo `pyproject.toml`.
Estes arquivos são apenas para compatibilidade com `pip`.
