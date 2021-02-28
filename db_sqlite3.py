import sqlite3
import os.path

def monta_tabelas():
    try:
        conn = sqlite3.connect('rastreios.db')
        c = conn.cursor()
        sql = "CREATE TABLE lista_rastreios (codigo TEXT PRIMARY KEY, telefone TEXT, ultimo_status TEXT);"
        c.execute(sql)
    except sqlite3.DatabaseError as e:
        print(e)
    finally:
        conn.close()

def insere_rastreio(codigo, numero, status):
    try:
        conn = sqlite3.connect('rastreios.db')
        c = conn.cursor()
        sql = f"INSERT INTO lista_rastreios(codigo, telefone, ultimo_status) VALUES('{codigo}', '{numero}', '{status}');"
        c.execute(sql)
        c.execute("commit;")
    except sqlite3.DatabaseError as e:
        print(e)
    finally:
        conn.close()

def remove_rastreio(codigo):
    try:
        conn = sqlite3.connect('rastreios.db')
        c = conn.cursor()
        sql = f"DELETE FROM lista_rastreios WHERE codigo = '{codigo}';"
        c.execute(sql)
        c.execute("commit;")
    except sqlite3.DatabaseError as e:
        print(e)
    finally:
        conn.close()

def select_rastreio():
    try:
        conn = sqlite3.connect('rastreios.db')
        c = conn.cursor()
        sql = "SELECT codigo, telefone, ultimo_status FROM lista_rastreios;"
        c.execute(sql)
        select = c.fetchall()
    except sqlite3.DatabaseError as e:
        print(e)
    finally:
        conn.close()
    return select

