# Proyecto final - Pensamiento Lógico
## Por: Ana Sofía Rodriguez Ferro, Mariana Catalina Sandoval Pérez, Daniel Mateo Segura Briceno.
## A: Cristian Camilo Penagos Torres
### Facultad de Ingeniería. 26 de Mayo de 2025

### Introducción
 El presente proyecto tiene como finalidad representar el campus de la Universidad de La Sabana mediante un grafo no dirigido. Cada edificio, punto de interés o espacio funcional es representado como un vértice del grafo, mientras que las conexiones entre ellos (caminos peatonales o rutas directas) son las aristas, ponderadas por la distancia real en metros. Esta estructura permite simular el mapa del campus y facilitar la búsqueda del camino más corto entre dos ubicaciones. Además de la representación matemática, el proyecto incluye una visualización gráfica del grafo y una interfaz interactiva que permite a los usuarios ingresar un origen y un destino para obtener la ruta óptima dentro de la universidad.


### Objetivos
Objetivo general: 
* Diseñar e implementar un sistema de grafo que modele la Universidad de La Sabana, con funcionalidades para visualizar el mapa del campus y calcular el camino más corto entre dos ubicaciones.

Objetivos específicos: 
* Construir un grafo ponderado a partir de las distancias reales entre edificios y puntos de interés del campus.
* Desarrollar una función que utilice el algoritmo de Dijkstra para encontrar la ruta más corta entre dos nodos.
* Visualizar el grafo usando la biblioteca networkx de Python.
* Integrar una interfaz gráfica con tkinter que permita la interacción del usuario de forma amigable y dinámica.
* Promover el trabajo en equipo, la división de tareas y la aplicación de estructuras de datos en un contexto real.

### Elaboración del proyecto
Con el fin de comprender a mayor profundidad el concepto de grafos, caminos y sus implicaciones en las ciencias de la computación, se ha desarrollado el presente proyecto de la siguiente manera.
#### Fase 1: Desarrollo experimental
Las primeras medidas entre los puntos del campus fueron almacenadas en Excel y guardadas como csv. A partir de aquí, utilizando solo networkx y pandas
se logró desarrollar un programa capaz de calcular la ruta entre dos nodos y mostrarla, careciendo de una interfaz gráfica, la visualización del grafo o algún contexto.
#### Fase 2: Integración de Interfaces Gráficas de Usuario (GUI)
Se implementan dos combobox (o listas de selección), así como una visualización del grafo respectivo usando matplotlib. Sin embargo, las ubicaciones y conexiones del grafo estaban lejos de ser precisas y acordes a la realidad.
Esto representó in desafío, pues aunque el cálculo en las rutas que es el principal requerimiento funcional era exitoso, la interacción con el usuario no era favorable.
#### Fase 3: Replanteamiento del plan de acción - Cambio de herramientas
Tras investigar en Google, StackOverflow, la documentación de Python y ChatGPT, se optó por tomar otro camino y aprovechar otras herramientas existentes. Es aquí donde Google Earth y overpass turbo
toman protagonismo como se explica:
* En Google Earth, se ha creado un proyecto con los puntos donde están los edificios. Esto ha dado el archivo Nodos.kml (Keyhole Markup Language, que se usa para almacenar y manipular datos geográficos)
* De manera análoga, Overpass Turbo ha delimitado los senderos peatonales, estos datos se han almacenado en el archivo export.kml
* Usando geopandas (librería de python que facilita la lectura de archivos geográficos como los kml), se ha extraido la información de los archivos. Y se ha almacenado en un diccionario de manera que a cada nodo/arista
  se le asocian sus coordenadas en el mapa
* Luego, el grafo se crea usando networkx. Esta librería permite el uso de shortest_path y shortest_path_lenght para encontrar el camino más corto entre dos nodos. De la misma forma, facilita relacionar los nodos con las aristas.
* Para favorecer el procesamiento, como cada nodo tiene una única coordenada, se establece un radio de 2.5m para que se considere una coordenada asociada a un nodo.
* Visualización: A partir de la fase dos se ha extraido el componente de tkinter que crea el GUI y las Combobox
* Nueva integración visual con contextily: contextily nos permite extraer el mapa de OpenStreetMap -framework opensource que contiene mapas geniales-, y al estar en coordenadas la info, es posible precisar que parte
  del mapa se requiere para la visualización. Finalmente esto se asocia a matplotlib (librería por excelencia de vissualización) y finalmente se incluye en el GUI
DONE!

### Ejecución del código
Para poder ejecutar este proyecto en su pc se requiere la instalación de Python 3.13 y las siguientes dependencias (todas se pueden agregar mediante pip install en terminal)
* geopandas
* networkx
* shapely
* matplotlib
* contextily

tkinter no requiere instalación, pues viene incluida en Python desde la versión 3.algo

#### Paso 0: Cree o seleccione un entorno virtual para la ejecución
Puede seguir este tutorial: https://docs.python.org/3/library/venv.html

#### Paso 1: Clone este repositorio en su pc
Desde su editor de código de preferencia, clone este repositorio.
Si por otra parte no desea clonarlo todo, asegurese de incluir en el mismo directorio los archivos:
* main.py
* Nodos.kml
* export.kml
#### Paso 2: Verifique la instalación de dependencias
Puede correr la siguiente linea en terminal para completar este paso

```pip install geopandas networkx shapely matplotlib contextily```
Nota: Si aun genera conflicto, instale las dependencias una por una

#### Paso 3: Ejecute el código
Ejecute main.py para visualizar el archivo

### Notas
Cualquier inquietud al respecto puede comunicarse vía MS Teams con los responsables del proyecto citados en la parte superior.
Gracias por su tiempo este semestre profe, fue una materia muy divertida!

