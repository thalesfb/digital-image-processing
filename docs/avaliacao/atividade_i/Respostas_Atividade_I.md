# Respostas — Atividade Avaliativa I
**Componente Curricular:** Processamento Digital de Imagens  
**Professor:** Fabricio Bizotto  

---

### Questão 1
**A. Explique os principais elementos de um sistema de processamento digital de imagens e como eles interagem para produzir uma imagem processada.**

Um sistema de processamento digital de imagens (PDI) é composto por elementos integrados que atuam desde a captura da cena física até a exibição ou tomada de decisão automática. Os componentes fundamentais e suas interações são:

1. **Dispositivos de Aquisição/Sensores:** Capturam a energia física do ambiente (refletida ou emitida) e a convertem em sinais analógicos contínuos de tensão ou corrente. Câmeras digitais (sensores CCD/CMOS), scanners 3D e sensores biomédicos (raios-X, ressonância magnética) são exemplos típicos.
2. **Digitalizador (Conversor A/D):** Converte a saída elétrica analógica do sensor de aquisição em dados digitais binários compreensíveis pelo computador.
3. **Hardware Especializado de Processamento:** Realiza cálculos de alta performance diretamente em matrizes de pixels de forma paralela. Composto por placas de processamento em tempo real (DSP, FPGAs) ou placas gráficas dedicadas (GPUs).
4. **Computador de Propósito Geral:** Gerencia o sistema operacional, armazena os dados temporários em memória RAM e executa a lógica de controle geral.
5. **Software de Processamento de Imagens:** Contém os algoritmos de processamento implementados (ex: OpenCV, bibliotecas como NumPy e PIL). Permite aplicar filtros, transformações e análise estatística.
6. **Dispositivos de Exibição:** Monitores, telas e displays que convertem os valores digitais finais de volta em luz visível para interpretação por parte do usuário.
7. **Dispositivos de Armazenamento:** Discos rígidos, SSDs e bancos de dados em rede onde as imagens originais e tratadas são arquivadas.
8. **Dispositivos de Comunicação:** Permitem a transmissão e o compartilhamento de imagens pela internet ou redes de dados industriais locais.

*Fluxo de interação:* A cena física real é focada no sensor óptico, digitalizada pelo conversor analógico-digital, carregada e manipulada na memória pelo software do computador (auxiliado por hardware de aceleração), exibida na tela do usuário e arquivada em um armazenamento permanente.

**B. Explique também amostragem e a quantização.**

- **Amostragem (Discretização Espacial):** É o processo de conversão das coordenadas contínuas $(x, y)$ da imagem real em coordenadas discretas. A imagem é dividida em uma grade (matriz) de pequenas sub-regiões discretas chamadas **pixels** (elementos de imagem). O número total de amostras determina a resolução espacial da imagem (ex: 640x480 pixels).
- **Quantização (Discretização de Amplitude):** É o processo de conversão dos valores de intensidade de luz contínuos em um número discreto de níveis discretos (geralmente associados a inteiros). O valor de brilho ou cor medido em cada pixel é mapeado para um nível inteiro discreto. A quantidade de níveis disponíveis depende do número de bits ($b$) utilizados para armazenar cada pixel (ex: uma imagem de 8 bits possui $2^8 = 256$ níveis possíveis de intensidade, variando de 0 a 255).

---

### Questão 2
**O que é o histograma de uma imagem? Explique duas técnicas de modificação por histograma e seus efeitos em uma imagem.**

**Histograma de uma imagem:**  
O histograma é uma ferramenta estatística que contabiliza a distribuição de tons de cinza ou cores em uma imagem. Ele é representado por um gráfico de barras em que o eixo horizontal ($x$) representa os níveis de intensidade de brilho (por exemplo, de 0 a 255 em 8 bits) e o eixo vertical ($y$) indica o número absoluto (ou a proporção de probabilidade) de pixels que possuem cada um desses valores de intensidade.

**Duas técnicas de modificação por histograma e seus efeitos:**

1. **Equalização de Histograma Global (Global Histogram Equalization):**
   - *Funcionamento:* Utiliza a Função de Distribuição Acumulada (CDF) normalizada das intensidades originais para criar uma função de mapeamento que espalha e redistribui os níveis concentrados por toda a faixa dinâmica de 0 a 255. O histograma resultante tende a ser aproximadamente uniforme (plano).
   - *Efeito:* Aumenta drasticamente o contraste global da imagem, realçando detalhes em regiões excessivamente escuras ou claras. Pode, no entanto, amplificar ruídos indesejados e gerar descontinuidades visuais se o histograma original for excessivamente concentrado.
2. **CLAHE (Contrast Limited Adaptive Histogram Equalization - Equalização Adaptativa de Histograma Limitada por Contraste):**
   - *Funcionamento:* Divide a imagem em sub-regiões quadradas chamadas blocos ou *tiles* (ex: 8x8) e realiza a equalização de histograma individualmente dentro de cada um desses blocos. Para evitar a amplificação indesejada de ruído em áreas uniformes, limita a inclinação da função de distribuição acumulada (através do parâmetro *clip limit*). O algoritmo reconstrói a imagem suavizando as transições de borda entre os blocos por meio de interpolação bilinear.
   - *Efeito:* Melhora o contraste local e preserva pequenos detalhes finos em diferentes partes da imagem de maneira independente, funcionando de forma excelente sob condições de iluminação complexas e não uniformes (como radiografias médicas e imagens com sombras parciais).

---

### Questão 3
**Considere o seguinte trecho de código em Python utilizando a biblioteca OpenCV:**

```python
import cv2
img = cv2.imread("imagem.jpg", 0)
_, img_binaria = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
cv2.imwrite("resultado.jpg", img_binaria)
```

**Explique:**

- **Como a imagem é carregada:** A imagem `"imagem.jpg"` é lida no disco por meio da função `cv2.imread()`. A passagem do segundo parâmetro como `0` (que equivale ao modo `cv2.IMREAD_GRAYSCALE`) converte diretamente a imagem colorida original de múltiplos canais (BGR) para uma escala de cinzas de canal único, economizando memória e preparando o dado para algoritmos de limiarização.
- **O significado dos parâmetros utilizados na função `cv2.threshold`:**
  - `img`: O array NumPy bidimensional contendo a imagem em tons de cinza que servirá como entrada.
  - `127`: O valor do limiar fixo (limite de decisão).
  - `255`: O valor máximo que será atribuído aos pixels que atenderem ao critério estabelecido pela regra de limiarização.
  - `cv2.THRESH_BINARY`: A flag de tipo que aplica a binarização clássica, matematicamente expressa como:
    $$f_{binaria}(x, y) = \begin{cases} 255 & \text{se } img(x, y) > 127 \\ 0 & \text{caso contrário} \end{cases}$$
- **Qual será o efeito da limiarização sobre a imagem original:** A imagem resultante `"resultado.jpg"` será estritamente binária (monocromática), contendo apenas pixels de valor 0 (preto absoluto) e 255 (branco absoluto). Todos os detalhes intermediários e tons degradês de cinza serão removidos, restando apenas contornos e silhuetas que superaram ou ficaram abaixo da intensidade de brilho 127.
- **Em quais situações práticas esse tipo de processamento pode ser útil:** Esse processamento é ideal para separação rápida entre objeto de interesse e plano de fundo (fundo homogêneo), muito comum em:
  - Sistemas de reconhecimento óptico de caracteres (OCR) para digitalização de documentos e livros (onde as letras são pretas e a folha branca).
  - Leitura de códigos de barra e QR codes em esteiras de logística.
  - Análise dimensional automatizada em linhas de montagem industrial (medição de formas e furos em chapas metálicas contrastantes).

---

### Questão 4
**Observe o código abaixo:**

```python
import cv2
img = cv2.imread("imagem.jpg", 0)
hist = cv2.calcHist([img], [0], None, [256], [0, 256])
img_eq = cv2.equalizeHist(img)
```

**Explique:**

- **A finalidade de cada operação realizada pelo código:**
  - `img = cv2.imread(...)`: Carrega a imagem do disco no modo escala de cinza de 8 bits.
  - `hist = cv2.calcHist(...)`: Executa a varredura na matriz de pixels de `img` e calcula a frequência de ocorrência para cada um dos 256 níveis de intensidade possíveis.
  - `img_eq = cv2.equalizeHist(...)`: Aplica o mapeamento de redistribuição de histograma global na imagem `img` para aumentar e distribuir uniformemente o contraste das intensidades de cinza.
- **O que representa a variável `hist`:** Representa um vetor NumPy unidimensional de tamanho $256 \times 1$, onde o índice $i$ armazena a contagem total de pixels presentes na imagem que possuem exatamente o tom de cinza correspondente a $i$.
- **Qual é o objetivo da função `equalizeHist`:** O objetivo é normalizar a distribuição do brilho da imagem, expandindo as intensidades que estão muito concentradas em uma faixa estreita (baixo contraste) ao longo de toda a gama de tons de 0 a 255. Isso melhora a legibilidade visual da imagem e facilita a segmentação por algoritmos posteriores.
- **Em quais tipos de imagens a equalização de histograma tende a produzir melhores resultados:** Ela produz excelentes resultados em imagens de baixo contraste original, que parecem lavadas, muito opacas, excessivamente escuras (subexpostas) ou muito brilhantes (superexpostas). Exemplo: imagens aéreas sob neblina, fotografias médicas de tecidos moles ou imagens subaquáticas escuras.

---

### Questão 5
**Explique o funcionamento do código a seguir. Qual é a principal vantagem do método utilizado (Limiarização automática de Otsu)? Que tipo de tarefa esse método pode ser útil?**

```python
import cv2
img = cv2.imread("imagem.jpg", 0)

valor, resultado = cv2.threshold(
    img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
)

print(valor)
```

**Funcionamento do código:**
1. A imagem é carregada em tons de cinza.
2. A função `cv2.threshold` é invocada com a soma das flags `cv2.THRESH_BINARY + cv2.THRESH_OTSU`. O limiar inicial é fornecido como `0`, pois o OpenCV irá desconsiderá-lo e acionará o algoritmo de Otsu para varrer o histograma e calcular automaticamente o limiar de binarização ideal.
3. O algoritmo de binarização clássico é aplicado utilizando o limiar descoberto.
4. O valor calculado é salvo na variável `valor` (exibido na tela com `print(valor)`) e a imagem binária correspondente é retornada na variável `resultado`.

**Principal vantagem do método de Otsu:**
Sua principal vantagem é a **automação e robustez**. Por ser um método adaptativo baseado em estatística de histograma, ele determina o limiar ideal sem nenhuma intervenção manual ou parametrização prévia (hardcoded). O algoritmo de Otsu alcança isso calculando o ponto de corte que minimiza a variância intraclasse das populações de pixels classificadas como fundo e objeto (ou equivalentemente, que maximiza a variância interclasses).

**Tipos de tarefa em que o método pode ser útil:**
- Segmentação automatizada em tempo real onde a iluminação ambiente é flutuante ou variável (ex: robótica móvel, monitoramento agrícola ou câmeras industriais).
- Pipelines de processamento em lote de imagens digitalizadas onde a tonalidade do papel e o contraste da tinta variam significativamente entre arquivos.
- Divisão prévia de imagens médicas para delimitar contornos de órgãos ou lesões biológicas sem calibração manual de limiar.
