"""
    Get Pokemon Data (gpdata)
    Estos scripts se encargan de ordenar los datos de nuestros datasets
    para su uso en nuestra red neuronal
"""
import pandas as pd
import helpers as hp

# Calcular el type_factor para cada combate
def get_type_factor(row):
    # Obtener los tipos del Pokémon 1 y 2 de los DataFrames por ID
    pokemon1 = pokemon_df[pokemon_df["#"] == row["First_pokemon"]]
    pokemon2 = pokemon_df[pokemon_df["#"] == row["Second_pokemon"]]

    # Verificar que hemos encontrado los Pokémon
    if pokemon1.empty or pokemon2.empty:
        print(f"Error: Pokémon no encontrado. First_pokemon: {row['First_pokemon']}, Second_pokemon: {row['Second_pokemon']}")
        return 0  # Valor por defecto en caso de error

    # Extraer tipos de Pokémon 1 y Pokémon 2
    types1 = [pokemon1["Type 1"].values[0], pokemon1["Type 2"].values[0]]
    types2 = [pokemon2["Type 1"].values[0], pokemon2["Type 2"].values[0]]
    
    # Calcular el type_factor usando la función definida
    return hp.normalize_tf(types1, types2)

# Calcular las diferencias de estadísticas entre Pokémon 1 y 2
def get_stat_differences(row):
    # Obtener las estadísticas de los Pokémon 1 y 2
    pokemon1 = pokemon_df[pokemon_df["#"] == row["First_pokemon"]]
    pokemon2 = pokemon_df[pokemon_df["#"] == row["Second_pokemon"]]

    # Extraer las estadísticas de Pokémon 1 y Pokémon 2
    stats1 = pokemon1[["HP", "Attack", "Defense", "Sp. Atk", "Sp. Def", "Speed", "Legendary"]].values[0]
    stats2 = pokemon2[["HP", "Attack", "Defense", "Sp. Atk", "Sp. Def", "Speed", "Legendary"]].values[0]

    # Calcular las diferencias de estadísticas
    stat_diff = stats1 - stats2

    # Retornar las diferencias como un diccionario para asignarlo fácilmente a las columnas
    return {
        "HP_diff": stat_diff[0],
        "Attack_diff": stat_diff[1],
        "Defense_diff": stat_diff[2],
        "Sp_Atk_diff": stat_diff[3],
        "Sp_Def_diff": stat_diff[4],
        "Speed_diff": stat_diff[5],
        "Legendary_diff": stat_diff[6]
    }

# Cargar los datos de Pokémon y los combates
pokemon_df = pd.read_csv("datasets/pokemon.csv")
battles_df = pd.read_csv("datasets/combats.csv")

pokemon_df = hp.preprocess_pokemon_data(pokemon_df)

# Aplicar la función para obtener el type_factor en cada combate
battles_df["type_factor"] = battles_df.apply(get_type_factor, axis=1)

# Calcular las diferencias de las estadísticas y asignarlas a las columnas correspondientes
stat_diff_df = battles_df.apply(get_stat_differences, axis=1)

# Convertir el diccionario de diferencias en columnas separadas
battles_df = pd.concat([battles_df, pd.DataFrame(stat_diff_df.tolist())], axis=1)

# Modificar la columna 'Winner'
# Si First_pokemon ganó, asignamos 1, si Second_pokemon ganó, asignamos 0
hp.update_winner_column(battles_df)

# Normalizamos los datos (estadisticas) en un rango de [-10.0, 10.0]
columns_to_normalize = ["type_factor","HP_diff","Attack_diff","Defense_diff","Sp_Atk_diff","Sp_Def_diff","Speed_diff","Legendary_diff"]
battles_df = hp.normalize_columns(battles_df, columns_to_normalize, min_val=-10.0, max_val=10.0)

# Guardamos los datos para su uso en la red neuronal de batallas
battles_df.to_csv("datasets/combat_train.csv", index=False)

print(pokemon_df.head())
print(battles_df.head())
