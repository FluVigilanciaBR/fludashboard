from IPython.display import display
from folium import GeoJson

import glob
import folium
import json
import random

def map_chart():
    mapa = folium.Map(location=[-20, -30], zoom_start=4)

    for fname in glob.glob('../data/estados_2010-*.json'):
        with open(fname) as f:
            data = json.load(f)
            
            # add style info
            color = "#%03x" % random.randint(0, 0xFFF)
            data['features'][0]['properties']['stroke'] = color
            data['features'][0]['properties']['stroke-width'] = 1.5
            data['features'][0]['properties']['fill'] = color
            
            gj = GeoJson(
                data, style_function=lambda x: {
                'color' : x['properties']['stroke'],
                'weight' : x['properties']['stroke-width'],
                'opacity': 0.6,
                'fillColor' : x['properties']['fill'],
            })
            gj.layer_name = gj.data['features'][0]['properties']['nome']
            
            gj.add_to(mapa)
    # FIXME: active=False by default.None
    mapa.add_children(folium.LayerControl())
    mapa
