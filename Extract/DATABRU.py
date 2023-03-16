import time
import DATABASEFUN as ute
from numpy import arange
import concurrent.futures


if __name__ == '__main__':

    start = time.perf_counter()
    # Categorias_Dirinario = {"Materias": 50, 'Noticias': 50, 'Curiosidade': 50, 'CoronaVirus': 50}
    Categorias_Dirinario = {"Materias": 50, 'Noticias': 50, 'Curiosidade': 50}

    ute.registro_paginas(2, "Noticias")
    for Categoria, Pagina in Categorias_Dirinario.items():
        with concurrent.futures.ProcessPoolExecutor() as executor:

            # categorias_links = ute.link_primeiras_paginas(Categoria)
            # p1 = executor.map(ute.registro_pagina1, categorias_links[1], categorias_links[0])

            paginas = arange(2, Pagina + 1)
            Categoria = [Categoria for x in range(len(paginas))]
            p2 = executor.map(ute.registro_paginas, paginas, Categoria)

    finish = time.perf_counter()
    print(finish)

