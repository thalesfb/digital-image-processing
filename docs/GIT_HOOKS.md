# Git Hooks — Convenção de commits

Conventional Commits com gitmoji em shortcode ASCII (`:books:`).

## Formato

```
:shortcode: type(scope): subject in English
```

| Parte | Regra |
|-------|-------|
| Emoji | Shortcode ASCII (`:books:`), nunca glyph Unicode |
| Type | `feat`, `fix`, `docs`, `test`, `chore`, `raw`, ... |
| Scope | Opcional — ex.: `aula2`, `notebook` |
| Subject | Inglês, imperativo, sem ponto final, máx. 72 caracteres |

### Exemplos válidos

```
:books: docs(aula2): add notebook execution guide
:sparkles: feat(aula2): implement CSV to grayscale PNG pipeline
:card_file_box: raw(aula2): add synthetic image fixtures
:bug: fix(notebook): correct BGR display for checker image
```

### Exemplos inválidos

```
docs: add readme          # falta gitmoji shortcode
:books: docs: adicionar guia   # subject em português
📚 docs: add guide         # emoji Unicode (mojibake no PowerShell)
:books: docs: add guide.   # ponto final no subject
```

## O que o hook faz

1. **`prepare-commit-msg`** — remove trailers `Co-authored-by` de ferramentas de IA
2. **`commit-msg`** — valida subject (ASCII, gitmoji, inglês) + **commitlint**

## Instalação

```powershell
# Windows (na raiz do repo)
npm install
npm run hooks:install:win
```

```bash
# Linux / macOS / Git Bash
npm install
npm run hooks:install
```

Isso define `git config core.hooksPath .githooks` e copia os scripts para `.githooks/`.

## Windows — commits com emoji

Use **shortcode** (`:bug:`), nunca cole emoji Unicode no PowerShell — vira mojibake no `git log`.

Para mensagens longas com acentos, use arquivo UTF-8:

```powershell
git commit -F commit-message.txt
```

## Gitmoji permitidos

`:sparkles:` `:bug:` `:books:` `:recycle:` `:zap:` `:package:` `:bricks:` `:card_file_box:` `:wastebasket:` `:ok_hand:` `:test_tube:` `:wrench:` `:broom:` e outros listados em `scripts/git-hooks/validate-subject.sh`.
