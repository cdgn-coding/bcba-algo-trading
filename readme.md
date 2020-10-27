# bCBA Algo trading

El objetivo de este proyecto es en primera instancia crear herramientas basadas en ciencias de datos y aprendizaje automatico para inversionistas de retail. Por un lado buscamos crear portafolios que obtengan la mayor varianza del mercado (retorno-riesgo); por otro lado implementamos un regresor para el retorno de inversion que tiene una accion en distintos periodos de tiempo (corto y mediano plazo), utilizando indicadores tecnicos. Para el uso de estas herramientas hemos creado un dashboard que se actualiza de forma batch cada semana, en el se pueden consultar los distintos tickers que hemos incluido en nuestro trabajo (mas de 400 tickers en la bolsa de estados unidos y sus correspondientes CDARS) y ademas, se puede consultar la prediccion del retorno de inversion por especie.

El regresor de retorno de inverion sobre una accion, funciona como una caja negra que ha sido entrenada para entender los movimientos del mercado dados los indicadores tecnicos. Este algoritmo, especificamente un ensamble de arboles, durante el entrenamiento ha aprendido a utilizar indicadores tecnicos para realizar la prediccion<sup>[1]</sup> de porcentaje de cambio de precio. De esta manera, cumple la funcion de asistente para el analisis tecnico y punto de partida para realizar analisis fundamentales y acotar los espacios de busqueda para oportunidades en forma concreta.

En cuanto a la creacion de los portafolios, hemos utilizado una tecnica que se suele denominar "eigen portfolio"<sup>[2]</sup>, que no tiene una traduccion literal al castellano pero en palabras simples: nos permite obtener pesos de portafolio por especie que capturan de forma conjunta la mayor varianza del mercado. En el fondo, esto ha sido implementado utilizando la tecnica de Principal Components Analysis (PCA) descomponiendo la matriz de covarianza de los retornos diarios por accion<sup>[3]</sup><sup>[4]</sup>.

Al principio, habiamos querido utilizar ciertos papeles populares para inversionistas tanto empresariales como de retail, sin embargo nos dimos cuenta que pudimos obtener mejores resultados y un mejor enfoque de negocio dando soporte a un mayor universo del mercado, por lo que incluimos todos los tickers que tienen su correspondiente CDARS. El espacio muestral se volvio lo suficientemente grande como para que los algoritmos deban entrenarse directamente en maquinas especializadas, proveidas a traves de los servicios de Google Cloud, en especial, el AI Platform. Con todo esto aprendido y ejecutado en el proceso, el algoritmo pudo mejorar sus resultados iniciales, los cuales al momento son similares o mejores que los descritos la referencia [1] y mejor proyeccion de aplicacion en el mundo de las inversiones. 

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

* [David G. Nexans](https://github.com/cnexans)
* [Guido Mitolo](https://github.com/guidomitolo) \
* [Thomas Artopoulos](https://github.com/thomasartopoulos)\
* [Jonatan Smith](https://github.com/John31991)\

## Referencias

[1] Jansen, S., 2020. Machine Learning For Algorithmic Trading - Second Edition. 2nd ed. Packt, p.512.
[2] Jansen, S., 2020. Machine Learning For Algorithmic Trading - Second Edition. 2nd ed. Packt, p.646.
[3] Tan, J., 2012. Principal Component Analysis and Portfolio Optimization. SSRN Electronic Journal,.
[4] Lei, D., 2018. Black–Litterman asset allocation model based on principal component analysis (PCA) under uncertainty. Cluster Computing, 22(S2), pp.4299-4306.