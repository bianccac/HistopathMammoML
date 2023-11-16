from flask import Flask, render_template, request, redirect, url_for
import os
import cv2
import numpy as np
from keras.models import load_model


# Função para pré-processamento da imagem
def preprocess_image(image_path):
    input_size = (224, 224)
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, input_size)
    image = np.expand_dims(image, axis=0)
    return image

# Função para salvar a imagem processada
def save_processed_image(processed_image, output_path):
    cv2.imwrite(output_path, processed_image)  # Salvando a imagem

# Função para realizar a previsão usando o modelo carregado
def make_prediction(processed_image):
    # Faça a previsão usando o modelo carregado
    prediction = model.predict(processed_image)
    # Aqui você pode processar a saída da previsão conforme necessário
    return prediction

app = Flask(__name__, template_folder='template')

# Carregando o modelo
model = load_model('model/modelvgg.h5')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # Verifica se foi enviado um arquivo
        if 'file' not in request.files:
            return 'Nenhum arquivo enviado.'

        file = request.files['file']

        # Verifica se o arquivo é uma imagem
        if file.filename == '':
            return 'Nenhum arquivo selecionado.'

        # Salva o arquivo na pasta 'uploaded_images'
        file_path = os.path.join('static/uploaded_images', file.filename)
        file.save(file_path)  # Salvando o arquivo fisicamente

        # Pré-processamento da imagem
        processed_image = preprocess_image(file_path)

        # Diretório para salvar a imagem processada
        processed_image_path = os.path.join('static/processed_images', 'processed_' + file.filename)

        # Salva a imagem processada
        save_processed_image(processed_image[0], processed_image_path)

        # Lógica para predição utilizando o modelo
        prediction = model.predict(processed_image)
        predicted_class = 'Benigna' if prediction[0][0] < 0.5 else 'Maligna'

        return render_template('result.html', uploaded_image=file.filename, processed_image='processed_' + file.filename, predicted_class=predicted_class)

if __name__ == '__main__':
    app.run(debug=True)
