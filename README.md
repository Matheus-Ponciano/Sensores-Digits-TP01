<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a id="readme-top"></a>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Índice</summary>
  <ol>
    <li>
      <a href="#sobre-o-projeto">Sobre o Projeto</a>
      <ul>
        <li><a href="#recursos">Recursos</a></li>
      </ul>
    </li>
    <li>
      <a href="#prerequisitos">Prerequisitos</a>
    </li>
    <li><a href="#usando">Usando</a>
      <ul>
        <li><a href="#executando">Executando</a></li>
        <li><a href="#funcionalidades">Funcionalidades</a></li>
      </ul>
    </li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## Sobre o Projeto

![Exemplo][imagem_670]

Esse projeto é o trabalho 1 da disciplina SSC0715 - Sensores Inteligentes. É um reconhecedor visual de dígitos, em tempo real, a partir da visão de uma ESP-CAM. A ESP-CAM coleta as imagens e envia através da própria rede WIFI local "Digits-Network", o processamento das imagens é feito em python com OpenCV e um modelo CNN-2D realiza o reconhecimento de cada dígito.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Recursos

Softwares, bibliotecas e placa arduino utilizados no projeto.

#### Software

* [![Python][Python-badge]][python-url]
* [![Tensorflow][TensorFlow-badge]][tensorflow-url]
* [![OpenCV][OpenCV-badge]][opencv-url]
* [![Arduino][Arduino-badge]][arduino-url]

#### Sensor

![ESP-CAM][imagem_espcam]

Seeed Studio XIAO ESP32-S3 Sense

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Prerequisitos

Para obter uma cópia do projeto, siga os passos:

1. Clone do repositório
   ```sh
   git clone https://github.com/Matheus-Ponciano/Sensores-Digits-TP01.git
   ```
2. Instalar pacotes pip 
   ```sh
   pip install numpy tensorflow matplotlib opencv-python
   ```
3. Mudar o url do git remoto para evitar push para o projeto base remote url
   ```sh
   git remote set-url origin github_username/repo_name
   git remote -v # confirmar mudança
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->
## Usando

Use this space to show useful examples of how a project can be used. Additional screenshots, code examples and demos work well in this space. You may also link to more resources.

### Executando

Para executar o projeto, siga os passos:

1. Alimente a ESP-CAM e faça upload do código de Arduino em ./espcam/espcam.ino.
2. A ESP-CAM deve então servir como um access point da rede "Digits-Network". Conecte-se com a senha padrão "12345678"
3. Execute o script ./digit_recognize_opencv.py. Pegará automaticamente o feed da câmera e carregará o modelo de CNN-2d "Modelo.keras".
4. Duas janelas abrirão, uma com a visão da câmera e o número identificado (Multi-Digit ESP32 Recognition), e outra com a visão da câmera processada com thresholding (Thresholded Inverted Image).

Caso queira alterar os parâmetros da CNN:

1. Abra o Python Notebook ./digits.ipynb.
2. Altere a rede ou o método de treinamento do modelo.
3. Execute todas as células.

### Funcionalidades

Enquanto estiver funcionando, o script tentará reconhecer dígitos na imagem de feed da câmera. Para isso, é aplicado um thresholding de binarização invertida na imagem para transformar ela em preto e branco. É aplicado então um identificador de contorno para determinar as caixas delimitadoras para os dígitos presentes, que servirão para seccionar os espaços com dígitos para reconhecimento pela CNN. Os dígitos reconhecidos serão então agrupados em um número exibido na parte superior da janela "Multi-Digit ESP32 Recognition" e as caixas delimitadoras encontradas serão demarcadas.

Foram implementados dois métodos de thresholding, o de Média Adaptativa Gausseana e o Otsu. Para trocar entre eles e observar os efeitos, segure a tecla "t". 

![thresholding-gauss][imagem_174_gauss]
![thresholding-otsu][imagem_174_otsu]



<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[imagem_670]: images/670.png
[imagem_174_gauss]: images/174_gauss.png
[imagem_174_otsu]: images/174_otsu.png
[imagem_espcam]: images/xiaoesp32s3sense.jpg

<!-- Shields.io badges. You can a comprehensive list with many more badges at: https://github.com/inttter/md-badges -->
[python-url]: https://www.python.org/
[tensorflow-url]: https://www.tensorflow.org/
[opencv-url]: https://www.opencv.org/
[arduino-url]: https://www.arduino.cc/
[Python-badge]: https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=fff
[Arduino-badge]: https://img.shields.io/badge/Arduino-008184.svg?logo=arduino
[OpenCV-badge]: https://img.shields.io/badge/OpenCV-5C3EE8?logo=opencv&logoColor=fff
[TensorFlow-badge]: https://img.shields.io/badge/TensorFlow-ff8f00?logo=tensorflow&logoColor=white
