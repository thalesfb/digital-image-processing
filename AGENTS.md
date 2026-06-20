# Diretrizes de Contribuição e Governança do Repositório (AGENTS.md)

Este documento define os princípios operacionais, a governança de código e os controles de qualidade que devem ser seguidos por qualquer desenvolvedor, estudante ou ferramenta automatizada que contribua com este repositório.

---

## 1. Princípios e Limites de Operação

Todas as modificações e novos experimentos neste repositório devem seguir três regras principais:
- **Segurança de Execução (Safe-by-Default):** Nenhum script ou notebook deve conter caminhos de arquivos absolutos (hardcoded) específicos de uma máquina local. Sempre utilize caminhos relativos baseados no diretório raiz do repositório usando a biblioteca `pathlib`.
- **Previsibilidade e Idempotência:** Scripts utilitários de geração (como criadores de notebooks e imagens sintéticas) devem ser idempotentes, ou seja, podem ser executados múltiplas vezes consecutivas sem causar duplicações de dados ou falhas de execução.
- **Documentação Obrigatória:** Qualquer adição de novos experimentos ou refatoração estrutural deve ser acompanhada imediatamente da atualização das documentações associadas (o guia de execução [`docs/EXECUTION.md`](docs/EXECUTION.md) e este guia).

---

## 2. Hierarquia de Fontes de Verdade

Em caso de divergência ou ambiguidades nas configurações do repositório, a seguinte ordem de prioridade deve ser considerada:

1. **Comportamento em tempo de execução dos Notebooks:** O código em Python funcional dentro de `experiment/Aula*/notebook.ipynb` é a especificação definitiva do laboratório.
2. **Scripts auxiliares e geradores:** Os códigos de `scripts/one_time/` e `scripts/run_ci_tests.py`.
3. **Slides e orientações teóricas oficiais do professor:** Arquivos em [`docs/slides/`](docs/slides/).
4. **Guias de documentação local:** [`docs/EXECUTION.md`](docs/EXECUTION.md) e `README.md`.

---

## 3. Classificação de Risco de Alterações

Para garantir que o repositório permaneça sempre operacional para entrega de atividades de laboratório, as alterações de código são classificadas em três níveis de risco:

### 🟢 Nível SEGURO (SAFE)
- Correções de digitação (typos) em células de texto Markdown nos notebooks.
- Adição de novos comentários esclarecedores no código Python.
- Atualização ou inclusão de notas de guias explicativos locais.
- *Ação necessária:* Apenas certificar que a estrutura de markdown é válida.

### 🟡 Nível ATENÇÃO (YELLOW)
- Modificações em algoritmos ou fórmulas matemáticas de transformação de pixels (ex: ajuste de normalização, equalização, convoluções).
- Inclusão ou substituição de imagens de entrada (fixtures sintéticas) nas pastas `data/input/`.
- Alterações em parâmetros de visualização de gráficos do Matplotlib.
- *Ação necessária:* Executar obrigatoriamente o script `scripts/verify-env.ps1` e rodar a validação local headless (`scripts/run_ci_tests.py`) antes de realizar o commit.

### 🔴 Nível CRÍTICO (RED)
- Remoção ou renomeação de notebooks de aulas já consolidados (ex: `notebook.ipynb`).
- Alteração na estrutura canonical de pastas do repositório (ex: renomear a pasta `experiment/`).
- Atualização ou adição de novas regras nas ferramentas de validação de qualidade locais (git hooks ou commitlint).
- Modificação no arquivo `.gitignore` que afete o isolamento das pastas `data/output/`.
- *Ação necessária:* Verificação local completa do ambiente, validação de compatibilidade em todos os sistemas operacionais suportados (Windows e Unix-like) e aprovação explícita para fusão das ramificações (branches).

---

## 4. Controles Obrigatórios de Qualidade

1. **Execução Isolada no Ambiente Virtual:** Nunca instale pacotes globais ou execute notebooks utilizando o interpretador do sistema. A ativação prévia via `. .\scripts\activate.ps1` é mandatória para qualquer desenvolvedor.
2. **Isolamento de Artefatos Gerados:** Todos os experimentos salvam suas imagens resultantes exclusivamente no subdiretório `data/output/` correspondente de sua pasta. É expressamente proibido commitar arquivos gerados nessas pastas, garantindo que o `.gitignore` continue ignorando `experiment/**/data/output/` corretamente.
3. **Fallback para Ambientes Headless:** Algoritmos que utilizam captura em tempo real (como câmeras/webcams) devem obrigatoriamente implementar caminhos de fallback (geração simulada de frames ou carregamento de arquivos estáticos/vídeos) caso o hardware de captura não seja detectado. Isso garante a continuidade de execução em testes automatizados.

---

## 5. Padronização de Commits (Conventional Commits + Gitmojis)

Para manter o histórico do Git limpo e profissional, todas as mensagens de commits devem utilizar o padrão semântico abaixo:

```text
:<gitmoji>: <tipo>(<escopo>): <mensagem curta em inglês>
```

### Exemplos Úteis:
* Inclusão de funcionalidade: `:sparkles: feat(aula5): add pseudo-coloration webcam pipeline`
* Atualização de documentação: `:books: docs: update build scripts instructions`
* Correção de erros: `:bug: fix(aula3): repair mismatched axis quote in matplotlib`
* Refatoração estrutural: `:recycle: refactor: organize slide pdfs to docs/slides/`

Consulte a lista completa de atalhos e regras em [`docs/GIT_HOOKS.md`](docs/GIT_HOOKS.md).

---

## 6. Checklist de Entrega e Handoff

Antes de finalizar qualquer modificação e considerá-la pronta para entrega ou revisão, realize o seguinte checklist de 5 passos:

- [ ] **Passo 1:** Ative o ambiente virtual e execute a validação de sanidade:
  ```powershell
  . .\scripts\activate.ps1
  .\scripts\verify-env.ps1
  ```
- [ ] **Passo 2:** Rode o testador automático local headless para garantir que nenhum notebook quebrou ou possui erros de runtime:
  ```powershell
  python scripts/run_ci_tests.py
  ```
- [ ] **Passo 3:** Certifique-se de que os notebooks estão com as células limpas de saídas desnecessárias e que as respostas teóricas estão devidamente preenchidas nas seções `Respostas` (se aplicável).
- [ ] **Passo 4:** Verifique o `git status` para ter certeza de que nenhuma imagem de saída temporária ou arquivo de cache (`__pycache__`, `.ipynb_checkpoints`) está sendo enviado por engano.
- [ ] **Passo 5:** Realize o commit seguindo a estrutura semântica com o respectivo gitmoji.

---

## 7. Antipadriões de Desenvolvimento (Proibidos)

- **Anti-padrão 1:** Modificar código diretamente sem ter ativado o kernel **PDI (.venv)** no Jupyter.
- **Anti-padrão 2:** Commitar arquivos de imagem de teste grandes ou desordenados diretamente na raiz do repositório.
- **Anti-padrão 3:** Criar symlinks de sistema para gerenciar diretórios de experimentos, o que quebra a compatibilidade cruzada com Windows/Powershell.
- **Anti-padrão 4:** Deixar prints infinitos ou loops que causem travamentos no ambiente de terminal.
