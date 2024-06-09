# -*- coding: utf-8 -*-
"""Classificador.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1MGrA_ytKnEnv7va7hoKmBm0JkQO7jnTs
"""

# Para montar a pasta do google drive
from google.colab import drive
drive.mount('/content/drive')

#!pip install kaggle -q

#!mkdir -p ~/.kaggle

#!cp kaggle.json ~/.kaggle

#!chmod 600 ~/.kaggle/kaggle.json

#%cd /content/
#!kaggle datasets download -d paultimothymooney/chest-xray-pneumonia

#!mkdir -p '/content/drive/MyDrive/Colab Notebooks/chest-xray-pneumonia'

#!unzip chest-xray-pneumonia.zip -d '/content/drive/MyDrive/Colab Notebooks/chest-xray-pneumonia'

#origem1 = "/content/drive/MyDrive/Colab Notebooks/chest-xray-pneumonia/chest_xray/chest_xray/val/NORMAL"
#origem2 = "/content/drive/MyDrive/Colab Notebooks/chest-xray-pneumonia/chest_xray/chest_xray/test/NORMAL"
#destino = "/content/drive/MyDrive/Colab Notebooks/chest-xray-pneumonia/chest_xray/chest_xray/train/NORMAL"

# Mover os arquivos da pasta de origem para a pasta de destino
#!mv "{origem1}"/* "{destino}"/
#!mv "{origem2}"/* "{destino}"/

#origem1 = "/content/drive/MyDrive/Colab Notebooks/chest-xray-pneumonia/chest_xray/chest_xray/val/PNEUMONIA"
#origem2 = "/content/drive/MyDrive/Colab Notebooks/chest-xray-pneumonia/chest_xray/chest_xray/test/PNEUMONIA"
#destino = "/content/drive/MyDrive/Colab Notebooks/chest-xray-pneumonia/chest_xray/chest_xray/train/PNEUMONIA"

# Mover os arquivos da pasta de origem para a pasta de destino
#!mv "{origem1}"/* "{destino}"/
#!mv "{origem2}"/* "{destino}"/

#!rm '/content/drive/MyDrive/Colab Notebooks/chest-xray-pneumonia/chest_xray/chest_xray/train/.DS_Store'
#!rm '/content/drive/MyDrive/Colab Notebooks/chest-xray-pneumonia/chest_xray/chest_xray/train/NORMAL/.DS_Store'
#!rm '/content/drive/MyDrive/Colab Notebooks/chest-xray-pneumonia/chest_xray/chest_xray/train/PNEUMONIA/.DS_Store'

import os
import numpy as np
from skimage import color, io
from skimage.transform import resize
from sklearn.utils import shuffle
from imblearn.over_sampling import SMOTE
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn import svm
from sklearn.model_selection import cross_val_score, KFold
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt
from keras.preprocessing.image import ImageDataGenerator
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import RandomForestClassifier
from keras.models import Sequential
from keras.layers import Flatten, Dense, Dropout
from keras.applications.vgg16 import VGG16
from keras.applications.resnet50 import ResNet50
from keras.applications.efficientnet import EfficientNetB0
import matplotlib.pyplot as plt

# Caminho das imagens
train_dir = "/content/drive/MyDrive/Colab Notebooks/chest-xray-pneumonia/chest_xray/chest_xray/train"
classes_unicas = ['NORMAL', 'PNEUMONIA']

# Inicializar contadores para cada classe
normal_cont = 0
pneumonia_cont = 0

# Percorrer cada diretório de classe e contar o número de amostras
for nome_classe in os.listdir(train_dir):
    caminho_classe = os.path.join(train_dir, nome_classe)
    if os.path.isdir(caminho_classe):
        if nome_classe == "NORMAL":
            normal_cont += len(os.listdir(caminho_classe))
        elif nome_classe == "PNEUMONIA":
            pneumonia_cont += len(os.listdir(caminho_classe))

print("Normal: ", normal_cont)
print("Pneumonia: ", pneumonia_cont)

# Para gerar um conjunto de imagens com maior variedade
datagen = ImageDataGenerator(
        rescale = 1./255,  # Normalização de imagem
        rotation_range = 30,  # Girar aleatoriamente algumas imagens de treinamento em 30 graus
        zoom_range = 0.2, # Ampliar aleatoriamente em 20% algumas imagens de treinamento
        width_shift_range=0.1,  # Deslocar aleatoriamente as imagens horizontalmente em 10% da largura
        height_shift_range=0.1,  # Deslocar aleatoriamente as imagens verticalmente em 10% da altura
        horizontal_flip = True)  # Virar imagens aleatoriamente na horizontal

imagens = []
rotulos = []

# Loop através das classes
for classe in classes_unicas:
    # Caminho para a pasta da classe atual
    caminho_classe = os.path.join(train_dir, classe)

    # Listar todos os arquivos na pasta da classe atual
    arquivos = os.listdir(caminho_classe)

    # Loop através dos arquivos da classe atual
    for arquivo in arquivos:
        # Caminho completo para o arquivo
        caminho_arquivo = os.path.join(caminho_classe, arquivo)

        # Carregar a imagem usando skimage
        imagem = io.imread(caminho_arquivo)

        # Converter imagem colorida para escala de cinza
        if len(imagem.shape) > 2:
            imagem = color.rgb2gray(imagem)

        # Redimensionar a imagem para um tamanho comum
        imagem_redimensionada = resize(imagem, (224, 224))

        # Adicionar a imagem redimensionada à lista de imagens
        imagens.append(imagem_redimensionada)
        rotulos.append(classe)

# Converter as listas em arrays numpy
imagens = np.array(imagens)
rotulos = np.array(rotulos)

# Aplicando a normalização usando o datagen
imagens = datagen.standardize(imagens)

# Embaralhar os dados
imagens, rotulos = shuffle(imagens, rotulos, random_state=35)

# Achatar as imagens para poder usar o SMOTE
X = imagens.reshape(imagens.shape[0], -1)

# Converter as strings de classe para números
y = np.where(rotulos == "NORMAL", 0, 1)

# Aplicar SMOTE
smote = SMOTE(random_state=35)
X_resampled, y_resampled = smote.fit_resample(X, y)

## Opção apenas para modelos CNN ##
# Colocar no formato padrão necessário
X_resampled = X_resampled.reshape(X_resampled.shape[0], 224, 224)

# Converter para RGB
X_resampled = np.repeat(X_resampled[:, :, :, np.newaxis], 3, axis=-1)

# Normalizar os valores dos pixels para o intervalo [0, 255]
X_resampled = (X_resampled - X_resampled.min()) / (X_resampled.max() - X_resampled.min()) * 255

# Converter os valores para o tipo de dados uint8
X_resampled = X_resampled.astype(np.uint8)

# Exibir imagem
plt.imshow(X_resampled[0])
plt.show()

# Reshape para 2D (224x224)
image_reshaped = X_resampled[0].reshape(224, 224)

# Exibir imagem
plt.imshow(image_reshaped, cmap='gray')
plt.show()

# Contar os valores únicos e suas contagens
valores_unicos, contagens = np.unique(y_resampled, return_counts=True)

# Exibir os valores únicos e suas contagens
for valor, contagem in zip(valores_unicos, contagens):
    print(f"{valor}: {contagem}")

# Criando os dados de treinamento e teste
X_train, X_test, y_train, y_test = train_test_split(X_resampled, y_resampled, test_size=0.3, random_state=35)
print(X_train.shape)
print(y_train.shape)

# Preparar modelos e pipelines
models = []
models.append(('LogisticRegression', Pipeline([('scaler', StandardScaler()), ('classifier', LogisticRegression(max_iter=1000))])))
#models.append(('DecisionTree', Pipeline([('scaler', StandardScaler()), ('classifier', DecisionTreeClassifier())])))
#models.append(('SVM', Pipeline([('scaler', StandardScaler()), ('classifier', svm.SVC())])))
#models.append(('MLP', Pipeline([('scaler', StandardScaler()), ('classifier', MLPClassifier())])))
#models.append(('RandomForest', Pipeline([('scaler', StandardScaler()), ('classifier', RandomForestClassifier())])))

# Inicializar variáveis para rastrear o melhor modelo
scoring = 'f1'
results = []
best_model = None
best_score = 0.0
best_name = ''

# Verificando as pontuações dos modelos
for name, model in models:
    kfold = KFold(n_splits=10, random_state=7, shuffle=True)
    cv_results = cross_val_score(model, X_train, y_train, cv=kfold, scoring=scoring)
    results.append(cv_results)
    msg = "%s: %f (%f)" % (name, cv_results.mean(), cv_results.std())
    print(msg)

    # Verificar se o modelo atual tem uma pontuação média de F1 melhor que o melhor modelo rastreado
    if cv_results.mean() > best_score:
        best_score = cv_results.mean()
        best_model = model
        best_name = name

"""LogisticRegression: 0.971580 (0.004059)<br>
DecisionTree: 0.884704 (0.017724)<br>
SVM: 0.970194 (0.009212)<br>
MLP: 0.969387 (0.010221)<br>
RandomForest: 0.956846 (0.009232)
"""

# Treinar e avaliar o melhor modelo no conjunto de teste
hist = best_model.fit(X_train, y_train)
test_score = best_model.score(X_test, y_test)
print("Melhor modelo: %s com F1-score: %f" % (best_name, best_score))
print("Score do teste para melhor modelo: %f" % test_score)

"""Melhor modelo: LogisticRegression com F1-score: 0.971580<br>
Score do teste para melhor modelo: 0.963729
"""

# Avaliar modelo no conjunto de teste
y_pred = best_model.predict(X_test)

# Utilizando as métricas de classificação
cm = confusion_matrix(y_test, y_pred)
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)

# Mostrando o resultado obtido através das métricas
# Matriz de confusão
disp = ConfusionMatrixDisplay(confusion_matrix=cm)
disp.plot()
plt.show()
print(cm)
# Quantos aprovados e reprovados foram preditos corretamente
print("Acurácia: {:.2f}".format(accuracy))
# Do número total de preditos como aprovados, quantos são mesmo aprovados
print("Precisão: {:.2f}".format(precision))
# Do número total de aprovados na base de dados, quantos foram preditos como aprovados
print("Recall: {:.2f}".format(recall))
# Média harmônica entre precisão e recall
print("F1: {:.2f}".format(f1))

"""[[1229   28]<br>
 [  65 1242]]<br>
Acurácia: 0.96<br>
Precisão: 0.98<br>
Recall: 0.95<br>
F1: 0.96

Observando as métricas usadas, dos 5 modelos testados, o que obteve os melhores resultados foi a Regressão Logística.
"""

# Modelo CNN padrão
# Definir a estrutura da RNA
#model = Sequential()
#model.add(Flatten())
#model.add(Dense(units = 128, activation = 'relu', input_dim=50176))
#model.add(Dropout(0.2))
#model.add(Dense(units = 1, activation = 'sigmoid'))
#model.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])

# Modelo CNN para deep learning
# Modelo VGG
model_conv = VGG16(include_top = False, weights = 'imagenet', input_shape = (224, 224, 3), pooling = 'max', classes = 2)
# Modelo ResNet
#model_conv = ResNet50(include_top = False, weights = 'imagenet', input_shape = (224, 224, 3), pooling = 'max', classes = 2)
#Modelo Efficient
#model_conv = EfficientNetB0(include_top = False, weights = 'imagenet', input_shape = (224, 224, 3), pooling = 'max', classes = 2)

model = Sequential()
model.add(model_conv)
model.add(Flatten())
model.add(Dense(units = 128, activation = 'relu'))
model.add(Dropout(0.2))
model.add(Dense(units = 1, activation = 'sigmoid'))
model.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])

# Treinar a RNA
history = model.fit(X_train, y_train, steps_per_epoch = 100, epochs=20, validation_data=(X_test, y_test))

# Mostrar o histórico da função perda
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'validation'], loc='upper right')
plt.show()

# Avaliar modelo no conjunto de teste
p_pred = model.predict(X_test)

# Extrair os rótulos das classes previstas
y_pred = np.where(p_pred > 0.5, 1, 0)

# Utilizando as métricas de classificação
cm = confusion_matrix(y_test, y_pred)
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)

# Mostrando o resultado obtido através das métricas
# Matriz de confusão
disp = ConfusionMatrixDisplay(confusion_matrix=cm)
disp.plot()
plt.show()
print(cm)
# Quantos aprovados e reprovados foram preditos corretamente
print("Acurácia: {:.2f}".format(accuracy))
# Do número total de preditos como aprovados, quantos são mesmo aprovados
print("Precisão: {:.2f}".format(precision))
# Do número total de aprovados na base de dados, quantos foram preditos como aprovados
print("Recall: {:.2f}".format(recall))
# Média harmônica entre precisão e recall
print("F1: {:.2f}".format(f1))

"""Valores CNN:<br>
[[1177   80]<br>
 [  63 1244]]<br>
Acurácia: 0.94<br>
Precisão: 0.94<br>
Recall: 0.95<br>
F1: 0.95

Valores VGG:<br>
[[1180  100]<br>
 [  30 1254]]<br>
Acurácia: 0.95<br>
Precisão: 0.93<br>
Recall: 0.98<br>
F1: 0.95<br>

Valores ResNet:<br>
[[1277    3]<br>
 [ 502  782]]<br>
Acurácia: 0.80<br>
Precisão: 1.00<br>
Recall: 0.61<br>
F1: 0.76<br>

Valores Efficient:<br>
[[1275    5]<br>
 [ 149 1135]]<br>
Acurácia: 0.94<br>
Precisão: 1.00<br>
Recall: 0.88<br>
F1: 0.94<br>

Observando as métricas usadas, dos 4 modelos de CNN testados, o que obteve os melhores resultados foi a VGG.
"""

