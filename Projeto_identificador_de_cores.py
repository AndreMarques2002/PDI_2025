Agora que a imagem já foi salva, vamos montar o drive para que ela possa ser utilizada nos processamentos que virão a seguir incluindo a exibição da mesma na tela. Caso ainda não tenha sido feita a conecção de nenhuma conta será solicitada que alguma conta se conecte ao Google Drive.

# **Identificação de cores**
Caro participante, agradecemos a sua participação nesta atividade onde pretendemos demonstrar como alguns processos de captura e processamento digital de imagens ocorrem. Essa demonstração se dará através da execução do Sistema Digital de Imagem que elaboramos, onde o usuário irá capturar uma imagem, através de uma Webcam, a imagem será apresentada, o usuário então irá executar alguns processamentos digitais sobre esta imagem, de forma a que possam ser apresentadas 4 imagens para a escolha da que melhor representa o objeto, após o que a imagem será apresentada e o usuário poderá escolher através do mouse, sobre qual parte da imagem deseja saber a côr exata, com a indicação do seu RGB, e sua côr complementar.

A execução de todos os passos, bem como toda esta introdução, estão se dando através do Google Colab, que é um aplicativo que combina a Edição de texto com a implementação de códigos de programação, nos quais é possível tanto a entrada de dados pelo usuário como a apresentação de resultados na tela, como você poderá ver a seguir através do passo a passo que será apresentado.

**Importação de Bibliotecas**


 para que os códigos possam ser executados é necessário instalar e importar as bibliotecas necessárias. Por conta da instalação de algumas bibliotecas, as vezes a importação apresenta uma falha, indicada por um sinal vermelho no play de execução, caso isto ocorra, entre na aba "Ambiente de execução", clique em Reiniciar Seção e execute novamente o play.

Clique no indicador de play que se encontra dentro dos colchetes abaixo   [ \ ]
"""

# Commented out IPython magic to ensure Python compatibility.
# %% Instalação e Configuração Inicial
!pip install ipympl
!pip install ipyevents

# %matplotlib widget

from google.colab import output
output.enable_custom_widget_manager()

import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
from google.colab import drive
from google.colab.output import eval_js
from base64 import b64decode
import ipywidgets as widgets
from IPython.display import display, clear_output, Javascript, Image
import webcolors, colorsys

"""**Função para capturar imagem via webcam**

Agora vamos executar a função que irá capturar a imagem através da Webcan.

Clique no indicador de play que se encontra dentro dos colchetes abaixo [ \ ]
"""

def take_photo(filename, quality):
  js = Javascript('''
    async function takePhoto(quality) {
      const div = document.createElement('div');
      const capture = document.createElement('button');
      capture.textContent = 'Capture';
      div.appendChild(capture);

      const video = document.createElement('video');
      video.style.display = 'block';
      const stream = await navigator.mediaDevices.getUserMedia({video: true});

      document.body.appendChild(div);
      div.appendChild(video);
      video.srcObject = stream;
      await video.play();

      // Resize the output to fit the video element.
      google.colab.output.setIframeHeight(document.documentElement.scrollHeight, true);

      // Wait for Capture to be clicked.
      await new Promise((resolve) => capture.onclick = resolve);

      const canvas = document.createElement('canvas');
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      canvas.getContext('2d').drawImage(video, 0, 0);
      stream.getVideoTracks()[0].stop();
      div.remove();
      return canvas.toDataURL('image/jpeg', quality);
    }
    ''')
  display(js)
  data = eval_js('takePhoto({})'.format(quality))
  binary = b64decode(data.split(',')[1])
  with open(filename, 'wb') as f:
    f.write(binary)
  return filename

"""**Conexão com o Google Drive e webcam**

Agora, Após acionar o play que segue abaixo, caso algum login não tenha sido realizado, o Google irá solicitar a realização de login por duas vezes, a câmera será ligada e a imagem vai aparecer na tela. Para capturar a imagem basta clicar no retângulo escrito captura para que a imagem seja salva e possa ser utilizada pelo aplicativo.


Clique no indicador de play que se encontra dentro dos colchetes abaixo   [ \ ]
"""

# Montar o Google Drive
drive.mount('/content/drive/')

image_path = "/content/drive/MyDrive/Colab Notebooks/"
filename=os.path.join(image_path,'photo1.jpg')
quality=0.8

try:
  take_photo(filename, quality)

  print('Imagem gravada em {}'.format(filename))

  # Show the image which was just taken.
  display(Image(filename))
except Exception as err:
  # Errors will be thrown if the user does not have a webcam or if they do not
  # grant the page permission to access it.
  print(str(err))

original_img = cv2.imread(filename)

if original_img is None:
    raise ValueError("Imagem não encontrada. Verifique o caminho.")

# Converter BGR para RGB para exibição
original_img_rgb = cv2.cvtColor(original_img, cv2.COLOR_BGR2RGB)

plt.figure(figsize=(6,6))
plt.imshow(original_img_rgb)
plt.title("Imagem capturada")
plt.axis('off')
plt.show()

"""**Filtros de Realce**


O primeiro processamento que será realizado é o de realce.

Clique no indicador de play que se encontra dentro dos colchetes abaixo   [ \ ]
"""

def apply_enhancement(img):
    # Realce utilizando CLAHE (Adaptive Histogram Equalization)
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
    l_clahe = clahe.apply(l)
    lab_clahe = cv2.merge((l_clahe, a, b))
    img_clahe = cv2.cvtColor(lab_clahe, cv2.COLOR_LAB2BGR)

    # Filtro de nitidez (Unsharp Masking)
    gaussian = cv2.GaussianBlur(img_clahe, (0,0), 2.0)
    img_sharp = cv2.addWeighted(img_clahe, 1.5, gaussian, -0.5, 0)

    # Filtro bilateral para reduzir ruído preservando bordas
    img_bilateral = cv2.bilateralFilter(img_sharp, 9, 75, 75)
    return img_bilateral

enhanced_img = apply_enhancement(original_img)
enhanced_img_rgb = cv2.cvtColor(enhanced_img, cv2.COLOR_BGR2RGB)

"""#Imagem com Realce (Filtro de Nitidez e Bilateral)#

Para ver a Imagem com o primeiro processamento:

Clique no indicador de play que se encontra dentro dos colchetes abaixo [ \ ]
"""

plt.figure(figsize=(6,6))
plt.imshow(enhanced_img_rgb)
plt.title("Imagem com Realce")
plt.axis('off')
plt.show()

"""**Equalização de Histograma**

O segundo processamento é o de Equalização de Histograma

Clique no indicador de play que se encontra dentro dos colchetes abaixo   [ \ ]
"""

def apply_histogram_equalization(img):
    # Converter para espaço YCrCb para equalizar apenas o canal Y (luminância)
    img_ycrcb = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)
    y, cr, cb = cv2.split(img_ycrcb)
    y_eq = cv2.equalizeHist(y)
    img_ycrcb_eq = cv2.merge((y_eq, cr, cb))
    img_eq = cv2.cvtColor(img_ycrcb_eq, cv2.COLOR_YCrCb2BGR)
    return img_eq

# Aplicar equalização
equalized_img = apply_histogram_equalization(original_img)
equalized_img_rgb = cv2.cvtColor(equalized_img, cv2.COLOR_BGR2RGB)

"""#Imagem com Equalização de Histograma#
Para ver a Imagem com o segundo processamento:

Clique no indicador de play que se encontra dentro dos colchetes abaixo [ \ ]
"""

plt.figure(figsize=(6,6))
plt.imshow(equalized_img_rgb)
plt.title("Imagem com Equalização de Histograma")
plt.axis('off')
plt.show()

"""**Segmentação com Watershed**

O terceiro processamento é o de Segmentação que irá marcar um contorno na imagem, para realizar o processamento e apresentar a imagem resultante na tela:

Clique no indicador de play que se encontra dentro dos colchetes abaixo   [ \ ]
"""

def apply_watershed(img):
    # Converter para escala de cinza e aplicar thresholding
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # Operações morfológicas
    kernel = np.ones((3,3), np.uint8)
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)
    sure_bg = cv2.dilate(opening, kernel, iterations=3)

    # Determinar foreground com transformação de distância
    dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
    ret, sure_fg = cv2.threshold(dist_transform, 0.7*dist_transform.max(), 255, 0)

    sure_fg = np.uint8(sure_fg)
    unknown = cv2.subtract(sure_bg, sure_fg)

    # Marcação e aplicação do watershed
    ret, markers = cv2.connectedComponents(sure_fg)
    markers = markers + 1
    markers[unknown == 255] = 0
    markers = cv2.watershed(img, markers)
    img[markers == -1] = [255, 0, 0]  # Bordas em vermelho
    return img

# Aplicar watershed na imagem equalizada
processed_img = apply_watershed(equalized_img)
processed_img_rgb = cv2.cvtColor(processed_img, cv2.COLOR_BGR2RGB)

plt.figure(figsize=(6,6))
plt.imshow(processed_img_rgb)
plt.title("Imagem Segmentada")
plt.axis('off')
plt.show()

"""**Pipeline de Pré-processamento**

O último processamento é a junção de todos os processamentos, para executar este processamento e visualizar a imagem na tela:

Clique no indicador de play que se encontra dentro dos colchetes abaixo   [ \ ]
"""

def full_preprocessing(img):
    # Passo 1: Realce
    img_enhanced = apply_enhancement(img)

    # Passo 2: Equalização de Histograma (canal Y do espaço YCrCb)
    ycrcb = cv2.cvtColor(img_enhanced, cv2.COLOR_BGR2YCrCb)
    y, cr, cb = cv2.split(ycrcb)
    y_eq = cv2.equalizeHist(y)
    img_eq = cv2.merge((y_eq, cr, cb))
    img_eq = cv2.cvtColor(img_eq, cv2.COLOR_YCrCb2BGR)

    # Passo 3: Watershed
    gray = cv2.cvtColor(img_eq, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    kernel = np.ones((3,3), np.uint8)
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)
    sure_bg = cv2.dilate(opening, kernel, iterations=3)
    dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
    ret, sure_fg = cv2.threshold(dist_transform, 0.7*dist_transform.max(), 255, 0)
    sure_fg = np.uint8(sure_fg)
    unknown = cv2.subtract(sure_bg, sure_fg)
    ret, markers = cv2.connectedComponents(sure_fg)
    markers = markers + 1
    markers[unknown==255] = 0
    markers = cv2.watershed(img_eq, markers)
    img_eq[markers==-1] = [255, 0, 0]
    return img_eq

final_img = full_preprocessing(original_img)
final_img_rgb = cv2.cvtColor(final_img, cv2.COLOR_BGR2RGB)

plt.figure(figsize=(6,6))
plt.imshow(final_img_rgb)
plt.title("Imagem Processada Completa")
plt.axis('off')
plt.show()

"""**Visualização Comparativa dos Histogramas**

Agora vamos exibir o histograma da imagem original e da imagem Equalizada.  
Clique no indicador de play que se encontra dentro dos colchetes abaixo   [ \ ]
"""

# %% Visualização dos Resultados Processados
plt.figure(figsize=(15, 4))
# Para equalização, processamos a imagem no espaço YCrCb
ycbcr = cv2.cvtColor(original_img, cv2.COLOR_BGR2YCrCb)
y, cr, cb = cv2.split(ycbcr)
y_eq = cv2.equalizeHist(y)
img_eq_temp = cv2.merge((y_eq, cr, cb))
img_eq_rgb = cv2.cvtColor(img_eq_temp, cv2.COLOR_YCrCb2RGB)

titles = ['1 - Original', '2 - Equalização de Histograma', '3 - Realce (CLAHE + Unsharp)', '4 - Pré-processamento Completo']
images = [original_img_rgb, img_eq_rgb, enhanced_img_rgb, final_img_rgb]

# %% Comparação dos Histogramas
plt.figure(figsize=(15, 6))
colors = ('r', 'g', 'b')

# Histograma da imagem original
plt.subplot(1, 2, 1)
for i, color in enumerate(colors):
    hist = cv2.calcHist([original_img], [i], None, [256], [0, 256])
    plt.plot(hist, color=color)
plt.title('Histograma - Original')
plt.xlim([0, 256])
plt.grid(True)

# Histograma após equalização
plt.subplot(1, 2, 2)
img_eq_bgr = cv2.cvtColor(img_eq_temp, cv2.COLOR_YCrCb2BGR)
for i, color in enumerate(colors):
    hist = cv2.calcHist([img_eq_bgr], [i], None, [256], [0, 256])
    plt.plot(hist, color=color)
plt.title('Histograma - Após Equalização')
plt.xlim([0, 256])
plt.grid(True)
plt.tight_layout()
plt.show()

"""#Visualização Comparativa das Imagens#

Agora vamos exibir as 4 imagens para que possa ser escolhida a que melhor representa o objeto a ter a côr identificada.
Clique no indicador de play que se encontra dentro dos colchetes abaixo [ \ ]


"""

plt.figure(figsize=(15, 4))
for i in range(4):
    plt.subplot(1, 4, i+1)
    plt.imshow(images[i])
    plt.title(titles[i], fontsize=12)
    plt.axis('off')
    if i > 0:  # Adiciona um histograma nas imagens processadas
        plt.colorbar(orientation='horizontal', fraction=0.05, pad=0.05)
plt.tight_layout()
plt.show()

"""**Escolha e Apresentação da Imagem**

 Diante das 4 imagens apresentadas, escolha através do preenchimento do número 1-2-3 ou 4 em um campo retangular, a que melhor representa o objeto:

1.   Imagem Original
2.   Imagem Equalizada pelo Histograma

3.   Imagem com Realce

4.   Imagem Pré-processada Completa

Primeiro

Clique no indicador de play que se encontra dentro dos colchetes abaixo   [ \ ]

Depois

Preencha o retângulo com o número escolhido
"""

userInput = int(input("Escolha o número da imagem. 1 - Original. 2 - Equalização de Histograma. 3 - Realce (CLAHE + Unsharp). 4 - Pré-processamento Completo "))
if userInput == 1:
  imageEscolhida = original_img_rgb
elif userInput == 2:
  imageEscolhida = equalized_img_rgb
elif userInput == 3:
  imageEscolhida = enhanced_img_rgb
else:
  imageEscolhida = final_img_rgb

imageEscolhida

"""##Identificação de Cores##

Agora será exibida a imagem sobre a qual iremos identificar a côr, após o processamento será exibida uma parte da imagem, a descrição da côr com seus códigos de RGB e a côr complementar, sendo que se desejar verificar outras regióes é só clicar novamente que as descrições serão apresentadas.

Primeiro para aparecer a Imagem

Clique no indicador de play que se encontra dentro dos colchetes abaixo   [ \ ]

Em seguida para escolher a região

Clique com o mouse sobre a região a ter a côr identificada.
"""

def get_color_name(rgb):
    try:
        return webcolors.rgb_to_name(rgb)
    except ValueError:
        pass
    r, g, b = rgb[0]/255, rgb[1]/255, rgb[2]/255
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    h *= 360
    s *= 100
    v *= 100
    if v < 15:
        return "Preto"
    if s < 10 and v > 90:
        return "Branco"
    if s < 20 and 20 < v < 90:
        return f"Cinza{' claro' if v > 60 else ' escuro'}" if s > 5 else "Cinza"
    color_ranges = [
        (0, 15, "Vermelho"), (15, 35, "Laranja"), (35, 65, "Amarelo"),
        (65, 165, "Verde"), (165, 200, "Azul-ciano"), (200, 250, "Azul"),
        (250, 290, "Roxo"), (290, 330, "Magenta"), (330, 360, "Rosa")
    ]
    color = next((name for (start, end, name) in color_ranges if start <= h < end), "Vermelho")
    modifiers = []
    if s < 40:
        modifiers.append("Pálido" if v > 50 else "Opaco")
    elif s > 80:
        modifiers.append("Vívido")
    if v < 40:
        modifiers.append("Escuro")
    elif v > 85:
        modifiers.append("Claro")
    if modifiers:
        return " ".join(modifiers + [color.lower()])
    return color

def get_complementary_color(rgb):
    r, g, b = rgb
    return (255 - r, 255 - g, 255 - b)

def get_analogous_colors(rgb):
    r, g, b = rgb
    return [
        (min(255, int(r*1.3)), min(255, int(g*1.3)), min(255, int(b*1.3))),
        (max(0, int(r*0.7)), max(0, int(g*0.7)), max(0, int(b*0.7)))
    ]

def create_color_table(colors, names):
    fig, ax = plt.subplots(figsize=(15, 2))
    ax.axis('off')
    table_data = []
    for color, name in zip(colors, names):
        rgb_str = f"RGB: {color[0]}, {color[1]}, {color[2]}"
        table_data.append([name, rgb_str, ""])  # Add an empty column for color
    table = ax.table(
        cellText=table_data,
        colLabels=["Nome da Cor", "Valores RGB", "Cor"],
        cellLoc='center',
        loc='center',
        colColours=['#f0f0f0', '#f0f0f0', '#f0f0f0']
    )
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.scale(1, 2)
    for i, color in enumerate(colors):
        table[(i+1, 2)].set_facecolor(np.array(color)/255)
    return fig

try:
  image = imageEscolhida
except NameError:
    try:
        image = original_img_rgb
    except NameError:
        image = (np.random.rand(200, 300, 3) * 255).astype(np.uint8)

if image.dtype in [np.float32, np.float64]:
    image = (image * 255).astype(np.uint8)

fig, ax = plt.subplots(figsize=(10, 10))
ax.imshow(image)
ax.set_title("Clique na imagem para análise de cor")
ax.axis('off')

def on_click(event):
    if event.xdata is None or event.ydata is None:
        return
    x = int(event.xdata)
    y = int(event.ydata)
    height, width = image.shape[:2]
    if x < 0 or x >= width or y < 0 or y >= height:
        print("Clique fora da área da imagem!")
        return
    print(f"Coordenadas clicadas: x={x}, y={y}")
    pixel = image[y, x]
    print(f"Valor RGB: {pixel}")
    main_color = tuple(pixel.tolist())
    main_name = get_color_name(main_color)
    comp_color = get_complementary_color(main_color)
    comp_name = get_color_name(comp_color)
    analogous_light, analogous_dark = get_analogous_colors(main_color)
    light_name = get_color_name(analogous_light)
    dark_name = get_color_name(analogous_dark)
    plt.figure(figsize=(8, 4))
    plt.subplot(1, 2, 1)
    margin = 60
    x0 = max(0, x - margin)
    x1 = min(width, x + margin)
    y0 = max(0, y - margin)
    y1 = min(height, y + margin)
    zoom = image[y0:y1, x0:x1]
    plt.imshow(zoom)
    offset_x = x - x0
    offset_y = y - y0
    plt.scatter([offset_x], [offset_y], c='red', marker='x')
    plt.title(f'Zoom na posição ({x}, {y})')
    plt.axis('off')
    plt.subplot(1, 2, 2)
    color_patch = np.full((200, 200, 3), main_color, dtype=np.uint8)
    plt.imshow(color_patch)
    plt.title(f'RGB: {main_color}\n{main_name}')
    plt.axis('off')
    plt.tight_layout()
    plt.show()
    combined_colors = [main_color, comp_color, analogous_light, analogous_dark]
    color_names = [f"Cor Original: {main_name}", f"Complementar: {comp_name}",
                   f"Análoga Clara: {light_name}", f"Análoga Escura: {dark_name}"]
    table_fig = create_color_table(combined_colors, color_names)
    plt.show()

cid = fig.canvas.mpl_connect('button_press_event', on_click)
plt.show()
