import folium
import os

#Creamos el mapa base centrado en El Progreso
mi_mapa = folium.Map(
    location=[15.4019, -87.7958], 
    zoom_start=15,
    tiles="OpenTopoMap"
)

nombre_mapa_js = mi_mapa.get_name()

# Definir límites de El Progreso (opcional)
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


# código HTML/CSS/JS con envíos de coordenadas URL
macro_html = f"""
<style>
    #btn-agregar {{
        position: fixed; top: 20px; right: 20px; z-index: 9999; 
        background-color: #28a745; color: white; padding: 12px 20px; 
        font-size: 16px; font-weight: bold; border: none; border-radius: 8px; 
        box-shadow: 0 4px 6px rgba(0,0,0,0.3); cursor: pointer;
    }}
    #btn-agregar.activo {{ background-color: #dc3545; }}
    #info-coordenadas {{
        position: fixed; bottom: 20px; left: 20px; z-index: 9999; 
        background: white; padding: 10px 15px; border-radius: 5px; 
        box-shadow: 0 2px 5px rgba(0,0,0,0.3); font-family: Arial, sans-serif; font-size: 14px;
    }}
</style>

<button id="btn-agregar">➕ Agregar Incidencia</button>
<div id="info-coordenadas">Haz clic en "Agregar Incidencia" para activar el modo reporte.</div>

<script>
window.addEventListener('DOMContentLoaded', function() {{
    var map = {nombre_mapa_js};
    var modoReporteActivo = false;
    var latSeleccionada = null;
    var lngSeleccionada = null;
    var marcadorTemporal = null;

    var btnAgregar = document.getElementById('btn-agregar');
    var infoCoo = document.getElementById('info-coordenadas');

    btnAgregar.addEventListener('click', function(e) {{
        e.stopPropagation();
        modoReporteActivo = !modoReporteActivo;
        
        if (modoReporteActivo) {{
            btnAgregar.classList.add('activo');
            btnAgregar.innerHTML = "❌ Cancelar Reporte";
            infoCoo.innerHTML = "<b>Modo activo:</b> Haz clic en el mapa donde ocurrió el incidente.";
        }} else {{
            modoReporteActivo = false;
            btnAgregar.classList.remove('activo');
            btnAgregar.innerHTML = "➕ Agregar Incidencia";
            infoCoo.innerHTML = "Modo cancelado.";
            if (marcadorTemporal) {{
                map.removeLayer(marcadorTemporal);
                marcadorTemporal = null;
            }}
        }}
    }});

    map.on('click', function(e) {{
        if (!modoReporteActivo) return;

        latSeleccionada = e.latlng.lat;
        lngSeleccionada = e.latlng.lng;

        if (marcadorTemporal !== null) {{
            map.removeLayer(marcadorTemporal);
        }}

        var contenidoPopup = `
            <div style="text-align: center; font-family: Arial, sans-serif; min-width: 160px;">
                <b>¿Confirmar ubicación?</b><br>
                <span style="font-size: 11px; color: gray;">Lat: ${{latSeleccionada.toFixed(5)}}, Lng: ${{lngSeleccionada.toFixed(5)}}</span><br><br>
                <button id="btn-confirmar-ubicacion" style="background-color: #007bff; color: white; border: none; padding: 6px 12px; border-radius: 4px; cursor: pointer; width: 100%;">
                    ✅ Confirmar Ubicación
                </button>
            </div>
        `;

        marcadorTemporal = L.marker([latSeleccionada, lngSeleccionada]).addTo(map)
            .bindPopup(contenidoPopup)
            .openPopup();

        infoCoo.innerHTML = "<b>Pin colocado.</b> Abre el globo para confirmar.";
    }});

    // Al confirmar, viajamos al formulario pasando las coordenadas directamente en el enlace
    document.addEventListener('click', function(e) {{
        if (e.target && e.target.id === 'btn-confirmar-ubicacion') {{
            e.stopPropagation(); 

            if (latSeleccionada !== null && lngSeleccionada !== null) {{
                // Redirigimos adjuntando lat y lng en la URL de forma limpia
                window.location.href = "formulario_incidente.html?lat=" + latSeleccionada + "&lng=" + lngSeleccionada;
            }}
        }}
    }});
}});
</script>
"""

mi_mapa.get_root().html.add_child(folium.Element(macro_html))

archivo_html = "index.html"
mi_mapa.save(archivo_html)
print(f"¡Módulo de mapa actualizado: {archivo_html}!")
