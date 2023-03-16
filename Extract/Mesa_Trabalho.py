import sqlite3
import operator

banco = sqlite3.connect("""D:\PROJETOS PY\FreeCodeCamp Python\DATABASE\AventuraPoste.db""")

Lista_Autores = banco.execute("""SELECT *FROM Autores""").fetchall()
#print(Lista_Autores)
Contador = 0
Dicionario_Resultados  = dict()
Dic_Categorias = dict()

Categorias = "Materias", "Noticias", "Curiosidade", "CoronaVirus"
for Autor in Lista_Autores:
    for categoria in Categorias:
        Busca_Dados = banco.execute(f"""SELECT *FROM Poste WHERE Nome LIKE "{Autor[1]}" AND Categoria LIKE "{categoria}" """).fetchall()
        #Contador += len(Busca_Dados)
        Dic_Categorias[f"{categoria}"] = len(Busca_Dados)

    Dicionario_Resultados[f"{Autor[1]}"] = Dic_Categorias.copy()
    #print(Dicionario_Resultados)
    #print(f"""AUTOR:{Autor[1]}\nNumero:{len(Busca_Dados)}\n""")
#print(f"""TOTAL DE PUBLICAÇOES FOI: {Contador}""")
#print(Dicionario_Resultados)
print(Dicionario_Resultados)