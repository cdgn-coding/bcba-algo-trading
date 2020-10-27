# bCBA Algo trading

El objetivo de este proyecto es en primera instancia crear herramientas basadas en ciencias de datos y aprendizaje automatico para inversionistas de retail. Por un lado, buscamos crear portafolios que obtengan la mayor varianza del mercado (retorno-riesgo); por el otro, implementamos un regresor para el retorno de inversión que tiene una acción en distintos períodos de tiempo (corto y mediano plazo) utilizando indicadores técnicos. Para el uso de estas herramientas hemos creado un dashboard que se actualiza de forma batch cada semana en el se pueden consultar los distintos tickers que hemos incluido en nuestro trabajo (mas de 400 tickers en la bolsa de Estados Unidos y sus correspondientes CDARS). Además, se puede consultar la predicción del retorno de inversión por especie.

El regresor de retorno de inverión sobre una acción funciona como una caja negra que ha sido entrenada para entender los movimientos del mercado dados los indicadores técnicos. Este algoritmo, específicamente un ensamble de árboles, ha aprendido durante el entrenamiento a utilizar indicadores técnicos para realizar la predicción<sup>[1]</sup> de porcentaje de cambio de precio. De esta manera, cumple la función de asistente para el análisis técnico y funciona como punto de partida para realizar análisis fundamentales y así acotar los espacios de búsqueda para oportunidades en forma concreta.

En cuanto a la creación de los portafolios, hemos utilizado una técnica que se suele denominar "eigen portfolio"<sup>[2]</sup>, que no tiene una traducción literal al castellano pero que puede resumirse como: nos permite obtener pesos de portafolio por especie que capturan de forma conjunta la mayor varianza del mercado. En el fondo, esto ha sido implementado utilizando la tecnica de Principal Components Analysis (PCA) descomponiendo la matriz de covarianza de los retornos diarios por acción<sup>[3]</sup><sup>[4]</sup>.

Al principio, quisimos utilizar ciertos papers populares para inversionistas tanto empresariales como de retail. Sin embargo, nos dimos cuenta que pudimos obtener mejores resultados y un mejor enfoque de negocio dando soporte a un mayor universo del mercado, por lo que incluimos todos los tickers que tienen su correspondiente CDARS. El espacio muestral se volvio lo suficientemente grande como para que los algoritmos deban entrenarse directamente en máquinas especializadas, proveídas a traves de los servicios de Google Cloud, en especial, el AI Platform. Con todo esto aprendido y ejecutado en el proceso, el algoritmo pudo mejorar sus resultados iniciales, los cuales al momento son similares o mejores que los descritos en la referencia [1] y mejor con una mejor proyección de aplicación en el mundo de las inversiones.

## Resultados

### Regresor de cambio de precio en 3 meses

MSE|RMSE|Spearmanr Coef|Spearmanr P Value
-- | -- | --| --
0.0970|0.312|0.292|0.0

### Regresor de cambio de precio en 2 meses

MSE|RMSE|Spearmanr Coef|Spearmanr P Value
-- | -- | --| --
0.0521|0.229|0.236|0.0

### Portafolio tecnológico

Ticker | Peso normalizado
-- | --
AAPL | 17%
GOOGL | 15%
INTC | 15%
KO | 4%
MELI | 34%
MSFT | 15%

### Portafolio conservador

Este portafolio consta de industrias duras como la banca, el aluminio, el petróleo

Ticker | Peso normalizado
-- | --
ALUA | 7%,
BHIP | 8%,
BMA | 12%,
CEPU | 10%,
CVH | 7.5%,
EDN | 8.5%,
GGAL | 12%,
LOMA | 9%,
PAMP | 8%,
SUPV | 12%,
TECO2 | 6%

## Datos

Los procesos de recolección e ingenieróa de features son lentos y pesados. Si se quiere consultar los datos creados, recolectados y utilizados a lo largo del proyecto, se pueden acceder de manera publica desde [este enlace a Google Drive](https://drive.google.com/drive/folders/1loTneiVME7P8hL6v0m1nxLhh2xkCdtyX?usp=sharing): 

## Estructura del proyecto

Las notebooks sobre las que trabajamos están numeradas por orden historico de la etapa del proyecto:

* [0_Data_Gathering](./0_Data_Gathering.ipynb) contiene la recolección de datos completa. Usa a su vez un archivo de texto [ticker_list](./data/ticker_list.txt) que contiene una lista de símbolos y nombres de empresas.
* [1_Feature_Engineering](./1_Feature_Engineering.ipynb) ejecuta la generación de indicadores técnicos tanto para la primera iteración (indicadores básicos) como para la segunda iteración (indicadores mas complejos)
* [2_Return_Signals_Regression](./2_Return_Signals_Regression.ipynb) tiene el primer acercamiento hacia la implementación del modelo que permitiría predecir el retorno de inversión. No debe ejecutarse de forma local a menos que se posea una maquina suficientemente potente (y con mucha paciencia). Esta nos sirvió en primera instancia para plantear un modelo menos ambicioso y para probar el código de entrenamiento de forma interactiva.
* [3_Time_Series](./3_Time_Series.ipynb) contiene un acercamiento exploratorio para tratar de predecir el precio de una acción utilizando el modelo ARIMAX.
* [4_Backtrader](./4_Backtrader.ipynb) **WIP** ejecuta una simulacion de trading algorítmico utilizando la librería backtrader y el modelo construido.
* [5_Representation_Learning](./5_Representation_Learning.ipynb) nos sirvió para crear un modelo red neuronal de forma interactiva y plantear una solución alternativa a los árboles de decisión.
* [6_Data_Gathering_Empresas_Seleccionadas](./6_Data_Gathering_Empresas_Seleccionadas.ipynb) en esta notebook, recolectamos datos de empresas seleccionadas para la construcción de un portafolio más conservador para invertir en la banca y commodities.
* [7_Portafolio_PCA_Empresas_Seleccionadas](7_Portafolio_PCA_Empresas_Seleccionadas.ipynb) planteamos un portafolio para invertir en banca y commodities utilizando el método descrito en la introducción.
* [8_Data_Preparation_Only_USD](./8_Data_Preparation_Only_USD.ipynb) refiltramos los datos inicialmente recolectados para reentrenar el modelo solamente utilizando tickers en dólares y evitar el ruido del ratio de conversion tanto de CDARS como del peso/dólar.
* [9_Portafolio_Tecnologico_PCA](./9_Portafolio_Tecnologico_PCA.ipynb) creamos un portafolio mas arriesgado para invertir en tecnología primordialmente aunque con una parte en una empresa de consumo masivo para darle cierto soporte al portafolio.

Los modelos presentados para la regresion se encuentran en la carpeta ```training```

* ```training/classic``` contiene los algoritmos de machine learning tradicionales (ensambles de árboles) utilizando indicadores básicos.
* ```trainning/mlp``` contiene una implementación de perceptron multicapa para el mismo propósito, con los mismos datos de entrada.
* ```training/classicv2``` tiene el script de entramiento de un XGBoost (algoritmo que dio mejor resultado en el paso anterior) utilizando indicadores tecnicos mas complejos (angulos de regresion lineal en distintos periodos en el pasado, betas, etc.)
* ```training/classicv3``` contiene el script de entramiento de un XGBoost que solo utiliza tickers en dolares.

Cada uno de estos scripts produce en la nube varios archivos: los scores de test y los modelos entrenados en formato ```.joblib```. Dentro de esta misma carpeta se pueden encontrar los scripts batch que crean la tarea en AI Platform de Google Cloud Platform.

Los modelos efectivamente entrenados se encuentran en la carpetas ```models```, ```models_v2```, ```models_v3``` que corresponden con la salida de los scripts de entrenamiento descritos anteriormente. En la carpeta ```best_models``` están los mejores algoritmos entrenados entre todos los realizados junto con sus respectivos scores de: error cuadrático medio, raíz del error cuadrático medio, el coeficiente sprearman y el p valor del mismo.

## Equipo

* [David G. Nexans](https://github.com/cnexans)
* [Guido Mitolo](https://github.com/guidomitolo)
* [Thomas Artopoulos](https://github.com/thomasartopoulos)
* [Jonatan Smith](https://github.com/John31991)

## Referencias

[1] Jansen, S., 2020. Machine Learning For Algorithmic Trading - Second Edition. 2nd ed. Packt, p.512.

[2] Jansen, S., 2020. Machine Learning For Algorithmic Trading - Second Edition. 2nd ed. Packt, p.646.

[3] Tan, J., 2012. Principal Component Analysis and Portfolio Optimization. SSRN Electronic Journal,.

[4] Lei, D., 2018. Black–Litterman asset allocation model based on principal component analysis (PCA) under uncertainty. Cluster Computing, 22(S2), pp.4299-4306.
