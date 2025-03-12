import barcode
from barcode.writer import ImageWriter
import cv2
from pyzbar.pyzbar import decode
import numpy as np
from PIL import Image
import streamlit as st

import streamlit as st
import cv2
import barcode
from barcode.writer import ImageWriter
from pyzbar.pyzbar import decode
import time

# Escolher o tipo de código de barras (EAN13, Code128, etc.)
codigo = barcode.get_barcode_class('code128')

# Gerar o código de barras
codigo_barras = codigo('PS27', writer=ImageWriter())

# Salvar como imagem
codigo_barras.save("codigo_barras")


# Função de escaneamento do código de barras
def escanear_codigo():
    cap = cv2.VideoCapture(0)

    # Verifica se a câmera foi aberta corretamente
    if not cap.isOpened():
        st.error("Erro ao acessar a câmera! Verifique se está conectada corretamente.")
        return

    st.write("📸 **Aponte o código de barras para a câmera...**")

    # Criar um espaço para exibir o preview
    placeholder = st.empty()

    codigo_detectado = None

    # Loop para capturar imagens da câmera
    while True:
        ret, frame = cap.read()
        if not ret:
            st.error("Erro ao capturar imagem da câmera!")
            break

        # Decodificar códigos de barras
        for barcode in decode(frame):
            codigo_detectado = barcode.data.decode("utf-8")
            break  # Para a leitura assim que encontrar um código

        # Mostrar o preview da câmera
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Converter para RGB
        placeholder.image(frame, channels="RGB", use_container_width=True)

        # Se o código foi detectado, interrompe o loop
        if codigo_detectado:
            break

        time.sleep(0.1)  # Pequeno delay para evitar uso excessivo de CPU

    cap.release()  # Liberar a câmera

    # Apagar o preview e exibir apenas o código detectado
    placeholder.empty()

    if codigo_detectado:
        st.success(f"✅ **Código Detectado:** `{codigo_detectado}`")
    else:
        st.warning("Escaneamento cancelado ou sem código detectado!")


# Interface do Streamlit
st.title("📷 Leitor de Código de Barras com Streamlit")

# Exibe o botão "Escanear Código"
escanear_button = st.button("📌 Escanear Código")

if escanear_button:
    escanear_codigo()








