import sqlite3
import re
import requests
from bs4 import BeautifulSoup

database = sqlite3.connect("AventuraPoste.db")
base = database.cursor()


def linksav(p=1, cate='Materias'):
    abl = {'Materias': f'https://aventurasnahistoria.uol.com.br/canal/reportagem/?page={p}',
           'Noticias': f'https://aventurasnahistoria.uol.com.br/canal/historia-hoje/?page={p}',
           'Curiosidade': f'https://aventurasnahistoria.uol.com.br/canal/almanaque/?page={p}',
           'CoronaVirus': f'https://aventurasnahistoria.uol.com.br/canal/coronavirus/?page={p}'}
    return abl[cate]


def registroposte(ids):
    print(ids)

    ids[0] = str(ids[0]).replace("'", "''")

    veripost = database.execute(f"""SELECT *FROM Poste WHERE Nome="{ids[0]}" AND Categoria='{ids[1]}' 
    AND Data='{ids[2]}' AND Titulo='{str(ids[3])}' AND Hora='{ids[5]}' AND Link='{ids[4]}'""").fetchall()
    verinome = database.execute(f"""SELECT *FROM Autores WHERE Autor="{ids[0]}" """).fetchall()

    if verinome == []:
        database.execute(f"""INSERT INTO 'Autores' ('Autor') VALUES ("{ids[0]}")""")
        print(f"{ids[0]} Registrado Concluido com sucesso!")

    if veripost == [] and database.execute(f"SELECT *FROM Poste WHERE Link='{ids[4]}'").fetchall() == []:
        database.execute(f"""INSERT INTO 'Poste' ('Nome','Categoria','Data', 'Titulo', 'Hora', 'Link') 
        VALUES ("{ids[0]}", '{ids[1]}', '{ids[2]}','{ids[3]}', '{ids[5]}','{ids[4]}')""")
        print(f"Resgistro Concluido com sucesso!")

    else:
        print("Esse poste já foi cadastrado")
    # database.commit()


def autorelist(soup, cate="Materias", pagina=0, linkp="https://aventurasnahistoria.uol.com.br/"):
    dados = list()
    cur = list()
    if pagina != 1:

        ur = re.findall(r'autor">(.+\s*\S*\S*)[|] ', str(soup), re.UNICODE)  # Nome DO autor
        print(ur)
        ur1 = re.findall('Publicado em ([0-9]+/[0-9]+/[0-9]+)', str(soup), re.UNICODE)  # Data

        ur2 = re.findall('class="col-9"><a href="(.+)"><img ', str(soup), re.UNICODE)  # Link

        hora = re.findall(', às(.[0-9]+h[0-9]+)', str(soup), re.UNICODE)
        titulo = re.findall('<p class="h4">(.+)</p><p>', str(soup), re.UNICODE)

    else:

        ur = re.findall(r'\bclass="autor">(.+?) [<]span\b', str(soup), re.UNICODE)
        ur1 = re.findall('Publicado em ([0-9]+/[0-9]+/[0-9]+)', str(soup), re.UNICODE)
        ur2 = "/" + linkp
        hora = re.findall(', às(.[0-9]+h[0-9]+)', str(soup), re.UNICODE)
        titulo = re.findall('<h1>(.+)</h1><p', str(soup), re.UNICODE)

    for f in ur:
        if str(f).count(",") > 0:
            j = str(f).split(',')
            cur.append(j[0].strip())
        elif str(f).count("|") > 0:
            j = str(f).split('|')
            cur.append(j[0].strip())
        elif str(f).count("//") > 0:
            j = str(f).split('//')
            cur.append(j[0].strip())
        else:
            cur.append(str(f).strip())

    for inde in range(len(cur)):
        jun = f"{str(cur[inde]).strip('|').strip(',').strip()}", cate,\
              f"{str(ur1[inde]).strip()}", str(titulo[inde]).strip().replace("'", ''), \
              'https://aventurasnahistoria.uol.com.br' + (str(ur2[inde]).strip() if pagina != 1 else ur2),\
              str(hora[inde]).strip()
        dados.append(jun)
        print(dados)
    return dados


def registro_pagina1(linkp, categoria):
    conec = requests.get('https://aventurasnahistoria.uol.com.br/' + linkp)

    html = BeautifulSoup(conec.text, "html.parser").decode()

    poste = autorelist(html, cate=categoria, pagina=1, linkp=linkp)
    registroposte(poste[0])


def link_primeiras_paginas(categoria):
    conec = requests.get(linksav(1, cate=categoria))
    html = BeautifulSoup(conec.text, "html.parser").decode()
    links = re.findall(r'\b href="/(.+?)"[>]<img\b', html, re.UNICODE)

    links = links[0:len(links) - 5]
    categorias = [categoria for _ in range(len(links))]

    return [categorias, links]


def registro_paginas(pagina, categorias="Noticias"):

    print(f"Categoria:{categorias}\nPagina:{pagina}")
    conec = requests.get(linksav(pagina, categorias))
    html = BeautifulSoup(conec.text, "html.parser").decode()
    lispagina = autorelist(html, categorias)
    for autores in lispagina:
        registroposte(autores)


def clear_name(name):

    if str(name).count(",") > 0:
        name = (str(name).split(','))[0].strip()

    elif str(name).count("|") > 0:
        (str(name).split("|"))[0].strip()

    elif str(name).count("//") > 0:
        (str(name).split("//"))[0].strip()

    return name
