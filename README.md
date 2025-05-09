# Identificador de Cores

## Descrição do Projeto
Um sistema interativo que captura imagens via webcam, aplica processamentos avançados e identifica cores com precisão. Permite visualizar:
- Cores em RGB
- Nomes aproximados das cores
- Cores complementares
- Cores análogas (claras e escuras)

## Funcionalidades Principais
### 📷 Captura de Imagem
- Integração direta com webcam
- Captura instantânea com qualidade ajustável

### 🖼️ Processamento de Imagem
1. **Realce de Imagem** (CLAHE + Unsharp Masking)
2. **Equalização de Histograma**
3. **Segmentação Watershed**
4. **Pipeline Completo** (combina todos os métodos)

### 🎨 Identificação de Cores
- Detecção por clique do mouse
- Zoom na região selecionada
- Informações detalhadas


## Pré-requisitos
| Biblioteca     | Versão Recomendada | Instalação               |
|----------------|--------------------|--------------------------|
| OpenCV         | 4.5+              | `pip install opencv-python` |
| NumPy          | 1.20+             | `pip install numpy`        |
| Matplotlib     | 3.4+              | `pip install matplotlib`   |
| Webcolors      | 1.11+             | `pip install webcolors`    |


Link do projeto: [Colab](https://colab.research.google.com/drive/1ldlE8Aq3Xty8U_v-6Mi-yvNH_iEIOWX5?usp=sharing)

Link da apresentação: [Canva](https://www.canva.com/design/DAGmzUcHnic/m3KsyEEC2DlgsdYfxX6fbQ/edit?utm_content=DAGmzUcHnic&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton)

## Como Usar
1. **Execução no Colab**:
 ```python
 !git clone https://github.com/AndreMarques2002/PDI_2025.git
 %cd identificador-de-cores
 !python Projeto_identificador_de_cores.py
