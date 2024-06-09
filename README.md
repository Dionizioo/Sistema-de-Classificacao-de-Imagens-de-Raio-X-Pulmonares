# Sistema de Classificação de Imagens de Raio-X Pulmonares

<div style="text-align: center;">
  <img src="https://github.com/Dionizioo/Sistema-de-Classificacao-de-Imagens-de-Raio-X-Pulmonares/assets/88460475/490777d2-46c4-49e1-b9cf-535263614649" alt="raio" />
</div>

## Projeto de Sistema de Classificação de Imagens
**Disciplina:** Visão Computacional  
**Professor:** Leonardo Gomes Tavares  

---

### Identificação e Descrição

**Equipe:**
- João Vitor Maciel de Brito 
- Jennifer Mayara de Paiva Goberski 
- Marcel Antunes Raposo 
- Vinicius Dionizio Patrocinio 

**Tema:**  
Classificação de pulmões através da análise de imagens de raio X.

**Objetivo:**  
Classificar entre pulmão saudável ou com pneumonia viral ou bacteriana através das imagens provenientes de exames de raio X pulmonar.

**Banco de Dados:**  
[Chest X-Ray Images (Pneumonia) - Kaggle](https://www.kaggle.com/datasets/paultimothymooney/chest-xray-pneumonia)

**Descrição do Banco:**
- O conjunto de dados é composto por imagens de Raio-X do tórax de crianças de 1 a 5 anos, obtidas do Centro Médico de Mulheres e Crianças de Guangzhou.
- As imagens foram submetidas a triagem de qualidade por especialistas, com diagnósticos revisados por dois médicos.
- O conjunto de dados está organizado em 3 pastas (treino, teste, validação) e contém subpastas para cada categoria de imagem (Pneumonia/Normal).
- Existem 5.863 imagens de Raio-X (JPEG) e 2 categorias (Pneumonia/Normal).

### Revisão de Literatura: Uso de bancos de dados de imagens de raio-x dos pulmões

- **Nimalsiri et al. (2023):** Criaram um dataset de imagens de raio-x, utilizando técnicas de segmentação para retirar áreas da imagem que não são de interesse.
- **Ivusic et al. (2022):** Apresentaram uma base de imagens com anotações de regiões de interesse feitas por profissionais da área radiológica.
- **Yang et al. (2022):** Divulgaram uma coleção de anotações/segmentações de manifestações radiológicas pulmonares consistentes com a tuberculose.
- **Sapountzakis, Theofilou e Tzouveli (2023):** Estudaram a detecção de COVID-19 em imagens de raio-x do pulmão utilizando diversos métodos de deep learning.
- **Hasan, Alom e Ali (2021):** Realizaram testes de modelos de deep learning para a detecção de casos de COVID-19 e pneumonia.
- **Ouerhani, Boulares e Mahjoubi (2023):** Compararam abordagens para a detecção de pneumonia pediátrica usando imagens de raio-x do tórax.
- **Sreena, Ponraj e Deepa (2021):** Apresentaram bases de dados públicas de raio-x dos pulmões para utilização em pesquisas que envolvam detecção de doenças.

### Materiais e Métodos

**Tipo e Objeto de Pesquisa:**
- Realizar uma análise comparativa entre técnicas de machine learning e deep learning para a construção de um classificador de imagens com duas saídas.

**Metodologia:**
- Ambiente de programação: Google Colab
- Linguagem: Python
- Banco de Imagens: Kaggle
- Pré-processamento: Conversão para tons de cinza, redimensionamento para 224x224 pixels, normalização e data augmentation
- Técnicas de Data Augmentation: Rotação, ampliação, deslocamentos horizontais ou verticais, e inversão
- Equilíbrio de dados: SMOTE
- Divisão dos dados: 70% treinamento, 30% teste
- Modelos: Regressão Logística, SVM, Árvore de Decisão, MLP, CNN (VGG, Efficient Net), Floresta Aleatória
- Avaliação: Validação cruzada (K-fold), matriz de confusão, acurácia, precisão, recall, F1 score

### Resultados

**Modelos de Aprendizado de Máquina Tradicional:**
- **Regressão Logística:** F1 média de 0.971580
- **Árvore de Decisão:** F1 média de 0.884704
- **SVM:** F1 média de 0.970194

**Modelos de Aprendizado Profundo:**
- **MLP:** F1 média de 0.969387
- **VGG:** F1 média de 0.956846
- **Efficient Net:** F1 média de 0.971580
- **Floresta Aleatória:** F1 média de 0.963729

### Conclusão

O projeto de classificação de imagens de raio-X pulmonares para detectar pneumonia apresentou resultados promissores, com modelos de aprendizado profundo (especialmente VGG e EfficientNet) obtendo desempenhos superiores em comparação aos modelos tradicionais de aprendizado de máquina. A acurácia, precisão, recall e F1 score evidenciaram uma maior capacidade de generalização e identificação das características relevantes nas imagens.
