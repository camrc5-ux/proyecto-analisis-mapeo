#Esta es una prueba de mapeo 
#Ocupo 3 librerías: folium, pandas y webrower
import folium
import webbrowser
import os

#Creamos el mapa centrado en El Progreso, Yoro
mi_mapa = folium.Map(
    location=[15.4019, -87.7958], 
    zoom_start=15,
    tiles="OpenTopoMap"  
)

#Definir los límites del municipio (prueba)
limites_el_progreso = [
    [15.4400, -87.8300],
    [15.4400, -87.7600],
    [15.3600, -87.7600],
    [15.3600, -87.8300]
]

folium.Polygon(
    locations=limites_el_progreso,
    color="red",
    weight=2,
    fill=False,
    tooltip="Límite del Municipio: El Progreso, Yoro"
).add_to(mi_mapa)

#Pin de prueba
folium.Marker(
    location=[15.4019, -87.7958],
    popup="Ejemplo de incidente en El Progreso",
    icon=folium.Icon(color="green", icon="ok-sign")
).add_to(mi_mapa)

#Guardar y abrir
archivo_html = "mapa_detallado_progreso.html"
mi_mapa.save(archivo_html)
webbrowser.open('file://' + os.path.realpath(archivo_html))

print("¡Mapa con nombres de calles generado con éxito!")