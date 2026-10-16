import os
import requests
from dotenv import load_dotenv
from folium import Map, Marker, Popup, Icon

load_dotenv()

s = requests.Session()
res = s.post(
    f"http://api.olhovivo.sptrans.com.br/v2.1/Login/Autenticar?token={os.getenv('SPTRANS_TOKEN')}"
)
print("Autenticação:", res.text)

codigo_linha = 671

res_paradas = s.get(f"http://api.olhovivo.sptrans.com.br/v2.1/Parada/BuscarParadasPorLinha?codigoLinha={codigo_linha}")
paradas = res_paradas.json()

res_pos = s.get(f"http://api.olhovivo.sptrans.com.br/v2.1/Posicao/Linha?codigoLinha={codigo_linha}")
posicoes = res_pos.json()
veiculos = posicoes.get("vs", [])

lat, lon = paradas[0]["py"], paradas[0]["px"]
m = Map(location=[lat, lon], zoom_start=14)
#m = Map(location=[lat, lon], zoom_start=14, tiles="Esri.WorldStreetMap")

for i in paradas:
    Marker(location=[i["py"], i["px"]], popup=Popup(f"Parada: {i.get('np', 'N/A')}", max_width="150"), icon=Icon(color="blue", icon="info-sign")).add_to(m)

for v in veiculos:
    Marker(location=[v["py"], v["px"]], popup=Popup(f"Ônibus ID: {v['p']}", max_width="150"), icon=Icon(color="green", icon="bus", prefix="fa")).add_to(m)

m.save("mapa_onibus.html")
print("Mapa gerado e salvo com sucesso como 'mapa_onibus.html'!")
