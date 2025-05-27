#Importar dependencias --- asegúrese de tenerlas instaladas!!!
import geopandas as gpd # procesar los kml s
import networkx as nx #Creación del grafo y uso del algoritmo de dijkstra
from shapely.geometry import LineString, Point #rectas, puntos, etc
import matplotlib.pyplot as plt #visualizar gráficas-  grafo sobre el mapa en este ejemplo contreto
import contextily as ctx #uso del mapa de OpenStreetMap :)
import tkinter as tk #GUI
from tkinter import ttk #GUI on steroids
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg #Usar matplotlib en la GUI

# Cargar los nodos y guardarlos en objeto de geopandas
gdf_nodos = gpd.read_file("Nodos.kml", driver="KML").to_crs(epsg=3857)

# Modificación para manejar diferentes tipos de geometría
nodo_pos = {}
for _, row in gdf_nodos.iterrows():
    geom = row["geometry"]
    if isinstance(geom, Point):
        nodo_pos[row["Name"]] = (geom.x, geom.y)
    elif isinstance(geom, LineString):
        # Usar el centroide para representar la línea como un punto
        centroid = geom.centroid
        nodo_pos[row["Name"]] = (centroid.x, centroid.y)
    else:
        # Para otros tipos de geometría, también se puede usar el centroide
        centroid = geom.centroid
        nodo_pos[row["Name"]] = (centroid.x, centroid.y)

coord_a_nombre = {v: k for k, v in nodo_pos.items()}

# Guardar los caminos (aristas) en un archivo de geopandas
gdf_caminos = gpd.read_file("export.kml", driver="KML").to_crs(epsg=3857)

#Grafooo!!!
G = nx.Graph()

for _, row in gdf_caminos.iterrows():
    geom = row["geometry"]
    if isinstance(geom, LineString):
        coords = list(geom.coords)
        for i in range(len(coords) - 1):
            p1 = coords[i]
            p2 = coords[i + 1]
            dist = LineString([p1, p2]).length
            G.add_edge(p1, p2, weight=dist)

#Facilita encontrar nodos
def encontrar_nodo_mas_cercano(coord, nodos_grafo):
    return min(nodos_grafo, key=lambda n: Point(n).distance(Point(coord)))


# Asocia los nodos a aquellos que están en el radio cercano a su cordenada
nodos_a_edificio = {}
umbral_distancia = 25  
for nombre, coord in nodo_pos.items():
    for nodo in G.nodes:
        if Point(nodo).distance(Point(coord)) <= umbral_distancia:
            nodos_a_edificio[nodo] = nombre

# Interfaz d eusuario GUI
app = tk.Tk()
app.title("Camino más corto entre dos puntos - Unisabana")
app.geometry("1000x800")

frame_controls = tk.Frame(app)
frame_controls.pack(side=tk.TOP, fill=tk.X, pady=10)

frame_plot = tk.Frame(app)
frame_plot.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Controles
inicio = tk.StringVar()
destino = tk.StringVar()
resultado = tk.StringVar()

tk.Label(frame_controls, text="Inicio:").pack(side=tk.LEFT, padx=5)
entrada_inicio = ttk.Combobox(frame_controls, textvariable=inicio, values=list(nodo_pos.keys()), width=20)
entrada_inicio.pack(side=tk.LEFT)

tk.Label(frame_controls, text="Destino:").pack(side=tk.LEFT, padx=5)
entrada_destino = ttk.Combobox(frame_controls, textvariable=destino, values=list(nodo_pos.keys()), width=20)
entrada_destino.pack(side=tk.LEFT)

tk.Label(frame_controls, textvariable=resultado, fg="blue", wraplength=400, justify="left").pack(side=tk.LEFT, padx=10)

# Gráfico
fig, ax = plt.subplots(figsize=(10, 10))
canvas = FigureCanvasTkAgg(fig, master=frame_plot)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack(fill=tk.BOTH, expand=True)


# Función para buscar y graficar camino más corto
def mostrar_ruta():
    ax.clear()
    ini = inicio.get()
    fin = destino.get()

    if not ini or not fin:
        resultado.set("Por favor, ingrese los nombres de los nodos de inicio y destino.")

    elif ini == fin:
        resultado.set("El inicio y el destino no pueden ser iguales.")
    else:
        try:
            coord_ini = nodo_pos[ini]
            coord_fin = nodo_pos[fin]
            nodo_ini = encontrar_nodo_mas_cercano(coord_ini, G.nodes)
            nodo_fin = encontrar_nodo_mas_cercano(coord_fin, G.nodes)

            path = nx.shortest_path(G, source=nodo_ini, target=nodo_fin, weight="weight")
            path_edges = list(zip(path, path[1:]))
            distancia = nx.shortest_path_length(G, source=nodo_ini, target=nodo_fin, weight="weight")

            # Convertir nodos en path a nombres si están cerca de un edificio
            path_labels = []
            nodos_etiquetados = []
            for nodo in path:
                nombre = nodos_a_edificio.get(nodo)
                if nombre and (not path_labels or path_labels[-1] != nombre):
                    path_labels.append(nombre)
                    nodos_etiquetados.append(nodo)

            # Dibujar
            nx.draw(G, pos={n: n for n in G.nodes}, ax=ax, node_size=10, node_color="gray", edge_color="lightgray")
            nx.draw_networkx_edges(G, pos={n: n for n in G.nodes}, edgelist=path_edges, edge_color="red", width=3, ax=ax)
            nx.draw_networkx_nodes(G, pos={n: n for n in path}, nodelist=path, node_color="red", node_size=30, ax=ax)
            nx.draw_networkx_nodes(G, pos={n: n for n in nodos_etiquetados}, nodelist=nodos_etiquetados, node_color="blue",
                                   node_size=60, ax=ax)
            ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik)

            ax.set_axis_off()
            ax.set_title(f"Ruta de {ini} a {fin} ({distancia:.2f} m)")
            resultado.set(f"Camino: {' --> '.join(path_labels)}\nDistancia: {distancia:.2f} m")
        except Exception as e:
            resultado.set(f"Error: {e}")
        canvas.draw()


# Botón
btn = tk.Button(frame_controls, text="Buscar ruta", command=mostrar_ruta)
btn.pack(side=tk.LEFT, padx=10)

app.mainloop()
