import sqlite3

banco = sqlite3.connect("""D:\PROJETOS PY\FreeCodeCamp Python\DATABASE\AventuraPoste.db""")

Lista_Autores = banco.execute("""SELECT *FROM Autores""").fetchall()
#print(Lista_Autores)
Contador = 0
Dicionario_Resultados  = dict()
for Autor in Lista_Autores:
    Busca_Dados = banco.execute(f"""SELECT *FROM Poste WHERE Nome LIKE "{Autor[1]}" """).fetchall()
    Contador += len(Busca_Dados)
    Dicionario_Resultados[f"{Autor[1]}"] = len(Busca_Dados)
    #print(f"""AUTOR:{Autor[1]}\nNumero:{len(Busca_Dados)}\n""")
#print(f"""TOTAL DE PUBLICAÇOES FOI: {Contador}""")
#print(Dicionario_Resultados)

#Organização do Dicionario para fazer o ranking
ParaOrganizar = sorted(Dicionario_Resultados.keys(), key=Dicionario_Resultados.get, reverse=True)
Dicionario_Certo = dict()
for x in ParaOrganizar:
    Dicionario_Certo[x] = Dicionario_Resultados[x]
#print(Dicionario_Certo)
for d, posiçao in enumerate(Dicionario_Certo.items()):
    print(f"""{d+1} - Autor: {posiçao[0]} Publicaçoes: {posiçao[1]}""")
