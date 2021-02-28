import schedule
import time
from threading import Thread
from flask import Flask, render_template, request, send_file
from scraping_rastreio import rastreio
from sms import envia_sms
from db_sqlite3 import *



app = Flask("Mauro Tony")

def agendador():
    while True:
        schedule.run_pending()
        time.sleep(60)
def automatico():
    select = select_rastreio()
    print("Executando agendador\n")
    for dados in select:
        codigo = dados[0]
        numero = dados[1]
        status, cod_status = rastreio(codigo)
        if cod_status == 3:
            remove_rastreio(codigo)
        envia_sms(numero, f"Código: {codigo}\n{status[0][0]}")

#schedule.every(12).hours.do(automatico)
schedule.every().day.at("12:00").do(automatico)
agendador_thread = Thread(target=agendador)
agendador_thread.start()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/resultado')
def resultado():
    codigo = request.args.get('codigo')
    numero = request.args.get('numero')
    if numero is None:
        return render_template('index.html')
    status, cod_status = rastreio(codigo)
    msg_error = "O rastreamento não está disponível para este código\nVerifique se o código do objeto está correto\nO objeto pode demorar até 24 horas (após postagem) para ser rastreado no sistema do Correios."
    if cod_status == 0:
        envia_sms(
            numero,
            msg_error
        )
        status = msg_error
    else:
        monta_tabelas()
        insere_rastreio(codigo, numero, status[0][0])
        envia_sms(numero, f"Código: {codigo}\n{status[0][0]}")
    return render_template('resultado.html', status=status, cod_status=cod_status, codigo=codigo, numero=numero)

@app.route('/lista')
def codigos():
    deletar = request.args.get('deletar')
    select = select_rastreio()
    visualizar = request.args.get('visualizar')
    if visualizar == "visualizar":
        codigo = select[0][0]
        numero = select[0][1]
        status, cod_status = rastreio(codigo)
        return render_template('resultado.html', status=status, cod_status=cod_status, codigo=codigo, numero=numero)
    if deletar == "deletar":
        remove_rastreio(select[0][0])
        select = select_rastreio()
    return render_template('codigos_salvos.html', select=select)


app.run(host='0.0.0.0')
