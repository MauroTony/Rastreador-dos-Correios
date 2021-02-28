import requests
from bs4 import BeautifulSoup

def rastreio(codigo):
    status = []
    cod_status = 0 # 0 -> Rastreio não encontrado, 1 -> Postado, 2 -> Saiu para entrefa, 3 -> Entregue
    request_resultado = requests.get(f"https://www.linkcorreios.com.br/?id={codigo}")
    request_resultado.encoding = 'utf-8'
    html_resultado = request_resultado.text
    soup_resultado = BeautifulSoup(html_resultado, 'html.parser')
    div_resultado = soup_resultado.find("div", class_="singlepost")
    if div_resultado is None:
        return status, cod_status
    ul_resultados = div_resultado.find_all("ul", class_="linha_status")
    for ul_resultado in ul_resultados:
        _status = []
        li_resultados = ul_resultado.find_all('li')
        for li_resultado in li_resultados:
            _status.append(li_resultado.text)
        status.append(_status)
    ultimo_status = status[0][0]
    if "Objeto entregue" in ultimo_status:
        cod_status = 3
    elif "saiu para entrega" in ultimo_status:
        cod_status = 2
    elif "postado" in ultimo_status:
        cod_status = 1
    return status, cod_status
