# Poke Vs
Este proyecto para la materia IA, su principal objetivo es el poder predecir quien ganará en una batalla pokemon 1 vs 1, cabe aclarar que es una aproximacion tomando en cuenta las caracteristicas del pokemon, en la realidad, esto puede determinarse por la habilidad del entrenador (jugador).

## Ejecución
Para ejecutar el programa, primero ejecutaremos el comando `py .\gpdata.py`, este comando creara por medio de las bases de datos de `pokemon.csv` y `combat.csv` un archivo .csv que se usara en `nn_combat.py` para entrenar a nuestra red neuronal. Ya que tengamos nuesta base de datos creada, procedemos a ejecutar el comando `py .\nn_combat.py`, esto entrenara a nuestra red y nos dara por resultado un modelo para predecir el ganador en una batalla pokemon.

## Documentación
En los siguientes enlaces, los llevará a la documentacion del archivo que indica.

- [helpers.py](helpers.md)