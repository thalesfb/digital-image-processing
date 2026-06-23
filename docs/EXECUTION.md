# Guia de execução — Experimentos PDI

## Regra obrigatória: ambiente virtual

Nunca execute `python`, `pip` ou notebooks com o Python global do sistema.

| Onde | Como garantir o `.venv` |
|------|-------------------------|
| Terminal | `. .\scripts\activate.ps1` — o prompt deve mostrar `(.venv)` |
| Notebook | Kernel **PDI (.venv)** no canto superior direito |
| Cursor/VS Code | Interpretador: `.venv\Scripts\python.exe` (configurado em `.vscode/settings.json`) |

Confirme antes de cada sessão:

```powershell
. .\scripts\activate.ps1
.\scripts\verify-env.ps1
```

## Checklist rápido (primeira vez)

- [ ] Python 3.11+ instalado
- [ ] Node.js 20+ instalado (hooks de commit)
- [ ] Git for Windows com **Git Bash** (hooks)
- [ ] `.\scripts\setup.ps1` executado na raiz
- [ ] Kernel **PDI (.venv)** selecionado no notebook
- [ ] `npm install` + `npm run hooks:install:win` (opcional mas recomendado)

## Fluxo por aula

### 1. Ativar ambiente (obrigatório)

```powershell
cd C:\dev\digital-image-processing
. .\scripts\activate.ps1
.\scripts\verify-env.ps1
```

Confirme: o prompt deve mostrar `(.venv)` e o verify deve imprimir `[OK] .venv ativo nesta sessao`.

### 2. Abrir o notebook

Abra o notebook correspondente à aula desejada no Cursor/VS Code:
- Aula 2: `experiment/Aula 2/notebook.ipynb`
- Aula 3: `experiment/Aula 3/notebook.ipynb`
- Aula 4: `experiment/Aula 4/notebook.ipynb`
- Aula 5: `experiment/Aula 5/notebook.ipynb`
- Aula 6: `experiment/Aula 6/notebook.ipynb`

**Importante:** selecione o kernel **PDI (.venv)** (canto superior direito) em cada notebook aberto.

### 3. Executar em ordem

Execute as células **de cima para baixo**, preenchendo as seções de resposta propostas. Abaixo estão as estruturas de cada experimento:

#### Aula 2 — Formação da Imagem
- Parte 0: Setup, caminhos e verificação de ambiente.
- Parte 1: Leitura de imagem CSV -> PNG.
- Parte 2: Geração de imagens sintéticas (`gradient_gray.png`, `checker_color.png`, `constant_150.png`).
- Parte 3: Somar brilho (+100) em tons de cinza (ingênuo vs saturado).
- Parte 4: Somar brilho em imagem colorida (canais BGR/RGB).
- Parte 5: Processamento em lote (batch pipeline).
- Parte 6: Síntese e ponte para histogramas.

#### Aula 3 — Histograma
- Parte 0: Setup de fixtures e dependências.
- Parte 1: Histograma em escala de cinza (`cv2.calcHist`).
- Parte 2: Histograma por canal em imagem colorida (BGR).
- Parte 3: Equalização global de histograma (`cv2.equalizeHist`).
- Parte 4: Limiarização linear (thresholding binário).
- Parte 5: Conversão para escala de cinza e realce local de contraste (CLAHE).
- Parte 6: Correção Gamma (transformação não-linear por LUT).
- Parte 7: Síntese e checklist conceitual.

#### Aula 4 — Operações Lógicas e Aritméticas
- Parte 0: Setup e carregamento de imagens (`mandril.tif`, `quadrado.png`, `tesoura.png`).
- Parte 1: Negativo da imagem e escalonamento de intensidade para `[100, 200]`.
- Parte 2: Combinação aritmética de imagens (blending), ajuste de brilho/contraste e normalização.
- Parte 3: Operações lógicas bit a bit (AND, OR, XOR, NOT) sobre máscaras binárias.
- Parte 4: Síntese de aplicações reais de aritmética/lógica.

#### Aula 5 — Pseudo-Coloração
- Parte 0: Setup e carregamento de dados estruturados de sensoriamento remoto e radiologia.
- Parte 1: Pseudo-coloração simples utilizando o colormap `JET`.
- Parte 2: Comparação de colormaps (JET, HOT, TURBO, VIRIDIS, INFERNO) em imagens de sensoriamento remoto.
- Parte 3: Pseudo-coloração em imagem médica (radiografia) usando colormaps adequados (BONE vs JET).
- Parte 4: Pseudo-coloração em tempo real via Webcam (com simulação/fallback offline).
- Parte 5: Aplicação interativa dinâmica completa para testar e salvar imagens pseudo-coloridas.
- Parte 6: Síntese conceitual e fechamento.

#### Aula 6 — Operações de Filtragem
- Experimento 1: Diferença absoluta e equalização básica.
- Experimento 2: Identificação de divergências em máscaras.
- Experimento 3: Subtração para identificação de defeitos em placas de circuito (PCB).
- Experimento 4: Transformação linear de brilho.
- Experimento 5: Transformação de potência (Ajuste Gamma).
- Experimento 6: Equalização de Histograma Global (comparativos lado-a-lado).
- Experimento 7: Equalização Adaptativa (CLAHE) para melhoria de contraste local.
- Experimento 8: Suavização passa-baixa combinada com detector Canny (Bordas).
- Experimento 9: Remoção de ruído Sal e Pimenta usando Filtros Medianos.
- Experimento 10: Melhoria de Nitidez com máscara Unsharp Masking.
- Experimento 11: Análise comparativa de detecção de bordas pré e pós-nitidez.

### 4. Verificar saídas

As saídas de cada aula são guardadas na subpasta `data/output/` correspondente a cada aula (as quais estão ignoradas no versionamento pelo `.gitignore`).

### 5. Responder às tarefas

Preencha as células **Respostas** com suas observações após ver os gráficos — isso fixa o aprendizado e cumpre as exigências pedagógicas do roteiro.

## Convenções de pastas (padrão infra)

| Pasta | Tipo | Versionar? |
|-------|------|------------|
| `imagem.csv`, imagens de entrada | Fonte imutável | Sim |
| `data/synthetic/` | Fixtures geradas | Opcional |
| `data/output/` | Artefatos de execução | Não (`.gitignore`) |
| `.venv/` | Ambiente Python | Não |
| `node_modules/` | Deps dos hooks | Não |

**Regra:** nunca edite manualmente arquivos em `data/output/` esperando que persistam no git.

## Troubleshooting

### Kernel não aparece

```powershell
. .\scripts\activate.ps1
pip install ipykernel
python -m ipykernel install --user --name=pd-images --display-name="PDI (.venv)"
```

Reinicie o Cursor e selecione o kernel.

### `ModuleNotFoundError: cv2`

O kernel não está usando o `.venv`. Selecione **PDI (.venv)** ou reative o ambiente.

### `ROOT` / `imagem.csv` não encontrado

Execute o notebook com cwd em `experiment/Aula 2/` ou na raiz do repo — a Parte 0 detecta ambos.

### Projeto no caminho errado

O repositório deve ficar em `C:\dev\digital-image-processing`. Evite rodar a partir do Google Drive.

### Commit rejeitado pelo hook

Leia a mensagem de erro e ajuste para o formato em [`GIT_HOOKS.md`](GIT_HOOKS.md).

Exemplo:

```powershell
git commit -m ":books: docs: add execution guide for aula 2"
```

## Verificar ambiente

```powershell
.\scripts\verify-env.ps1
```
