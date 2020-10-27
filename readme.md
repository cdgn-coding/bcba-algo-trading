# bCBA Algo trading

El objetivo de este proyecto es en primera instancia crear herramientas basadas en ciencias de datos y aprendizaje automatico para inversionistas de retail. Por un lado buscamos crear portafolios que obtengan la mayor varianza del mercado (retorno-riesgo); por otro lado implementamos un regresor para el retorno de inversion que tiene accion en distintos periodos de tiempo de corto y mediano plazo, utilizando varios indicadores tecnicos. Para el uso de estas herramientas hemos creado un dashboard que se actualiza de forma batch cada semana, en el se pueden consultar los distintos tickers que hemos incluido en nuestro trabajo (mas de 400 tickers en la bolsa de estados unidos y sus correspondientes CDARS) y ademas, se puede consultar la prediccion del retorno de inversion por especie.

El regresor de retorno de inverion sobre una accion, funciona como una caja negra que ha sido entrenada para entender los movimientos del mercado dados los indicadores tecnicos, este algoritmo, especificamente un ensamble de arboles, durante el entrenamiento ha aprendido a utilizar indicadores tecnicos para realizar la prediccion. De esta manera, cumple la funcion de asistente para el analisis tecnico y un punto de partida para realizar analisis fundamentales y acotar los espacios de busqueda de oportunidades.

En cuanto a la creacion de los portafolios, hemos utilizado una tecnica que se suele denominar "eigen portfolio", que no tiene una traduccion literal al castellano pero en palabras simples: nos permite obtener pesos de portafolio por especie que capturan de forma conjunta la mayor varianza del mercado. En el fondo, esto ha sido implementado utilizando la tecnica de Principal Components Analysis (PCA) que descompone una matriz en sus autovectores (eigen vectors, de ahi eigen portfolio), esta matriz a descomponer es la matriz de covarianza de los retornos diarios por accion.

Al principio, habiamos querido utilizar ciertos papeles populares para inversionistas tanto empresariales como de retail, sin embargo nos dimos cuenta que pudimos obtener mejores resultados y un mejor enfoque de negocio dando soporte a un mayor universo del mercado, por lo que incluimos todos los tickers que tienen su correspondiente CDARS. El espacio muestral se volvio lo suficientemente grande como para que corrieramos los algoritmos directamente en maquinas especializadas, proveidas a traves de los servicios de Google Cloud, especificamente, el AI Platform. Con todo esto aprendido y ejecutado en el proceso, el algoritmo pudo obtener mejores resultados y mejor proyeccion de aplicacion en el mundo de las inversiones. 

## Estructura del proyectadasdo

Las notebooks sobre las que trabajamos estan numeradas por orden historico de la etapa del proyecto:

* [0_Data_Gathering](./0_Data_Gathering.ipynb) contiene la recoleccion de datos completa. Usa a su vez un archivo de texto [ticker_list](./data/ticker_list.txt) que contiene una lista de simbolos y nombres de empresas.
* [1_Feature_Engineering](./1_Feature_Engineering.ipynb) ejecuta la generacion de indicadores tecnicos tanto para la primera iteracion (indicadores basicos) como para la segunda iteracion (indicadores mas complejos)
* [2_Return_Signals_Regression](./2_Return_Signals_Regression.ipynb) tiene el primer acercamiento hacia la implementacion del modelo que permitiria predecir el retorno de inversion, no debe ejecutarse de forma local a menos que se posea una maquina suficientemente potente (y paciencia). Esta nos sirvio en primera instancia para plantear un modelo menos ambicioso y probar el codigo de entrenamiento de forma interactiva.
* [3_Time_Series](./3_Time_Series.ipynb) contiene un acercamiento exploratorio para tratar de predecir el precio de una accion utilizando el modelo ARIMAX.
* [4_Backtrader](./4_Backtrader.ipynb) **WIP** ejecuta una simulacion de trading algoritmico utilizando la libreria backtrader y el modelo construido.
* [5_Representation_Learning](./5_Representation_Learning.ipynb) nos sirvio para crear un modelo red neuronal de forma interactiva y plantear una solucion alternativa a los arboles de decision.
* [6_Data_Gathering_Empresas_Seleccionadas](./6_Data_Gathering_Empresas_Seleccionadas.ipynb) en esta notebook, recolectamos datos de empresas seleccionadas para la construccion de un portafolio mas conservador para invertir en la banca y commodities.
* [7_Portafolio_PCA_Empresas_Seleccionadas](7_Portafolio_PCA_Empresas_Seleccionadas.ipynb) planteamos un portafolio para invertir en banca y commodities utilizando el metodo descrito en la introduccion.
* [8_Data_Preparation_Only_USD](./8_Data_Preparation_Only_USD.ipynb) refiltramos los datos inicialmente recolectados para reentrenar el modelo solamente utilizando tickers en dolares y evitar el ruido del ratio de conversion tanto de CDARS como del peso/dolar.
* [9_Portafolio_Tecnologico_PCA](./9_Portafolio_Tecnologico_PCA.ipynb) creamos un portafolio mas arriesgado para invertir en tecnologia primordialmente aunque con una parte en una empresa de consumo masivo para darle cierto soporte al portafolio.

Los modelos presentados para la regresion se encuentran en la carpeta ```training```

* ```training/classic``` contiene los algoritmos de machine learning tradicionales (ensambles de arboles) utilizando indicadores basicos.
* ```trainning/mlp``` contiene una implementacion de perceptron multicapa para el mismo proposito, con los mismos datos de entrada.
* ```training/classicv2``` tiene el script de entramiento de un XGBoost (algoritmo que dio mejor resultado en el paso anterior) utilizando indicadores tecnicos mas complejos (angulos de regresion lineal en distintos periodos en el pasado, betas, etc.)
* ```training/classicv3``` contiene el script de entramiento de un XGBoost que solo utiliza tickers en dolares.

Cada uno de estos scripts produce en la nube varios archivos: los scores de test y los modelos entrenados en formato ```.joblib```. Dentro de esta misma carpeta se pueden encontrar los scripts batch que crean la tarea en AI Platform de Google Cloud Platform.

Los modelos efectivamente entrenados se encuentran en la carpetas ```models```, ```models_v2```, ```models_v3``` que corresponden con la salida de los scripts de entrenamiento descritos anteriormente y, en la carpeta ```best_models``` estan los mejores algoritmos entrenados entre todos los realizados junto con sus respectivos escores de: error cuadratico medio, raiz del error cuadratico medio, el coeficiente sprearman y el p valor del mismo.

## Equipo

[Guido Mitolo](https://github.com/guidomitolo) \
[Thomas Artopoulos](https://github.com/thomasartopoulos)\
[Jonatan Smith](https://github.com/John31991)\
[David G. Nexans](https://github.com/cnexans)

## Referencias

[Algorithmic Trading 101](https://towardsdatascience.com/algorithmic-trading-101-1f9bb503e22a)\
[How My Machine Learning Trading Algorithm Outperformed the SP500 For 10 Years](https://towardsdatascience.com/the-austrian-quant-my-machine-learning-trading-algorithm-outperformed-the-sp500-for-10-years-bf7ee1d6a235)\
[Application of Machine Learning Techniques to Trading](https://medium.com/auquan/https-medium-com-auquan-machine-learning-techniques-trading-b7120cee4f05)\
[Machine Learning for Day Trading](https://towardsdatascience.com/machine-learning-for-day-trading-27c08274df54)\
[Deep Reinforcement Learning for Automated Stock Trading](https://towardsdatascience.com/deep-reinforcement-learning-for-automated-stock-trading-f1dad0126a02)\
[DeepDow — Portfolio optimization with deep learning](https://towardsdatascience.com/deepdow-portfolio-optimization-with-deep-learning-a3ffdf36eb00)
