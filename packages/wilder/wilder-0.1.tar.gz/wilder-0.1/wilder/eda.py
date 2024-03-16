import pandas as pd

def eda(df):
    nom, type_colonne, pourcentage_nan,nombre_lignes_nan,valeur_max,valeur_min, valeur_moyenne, count, ecart_type,Q1, Q2,Q3,population_quartiles,duplicates = [],[],[],[],[],[],[],[],[],[],[],[],[],[]
    viz_nan = df[df.isna().any(axis=1)]
    
    print("Détails des colonnes :")
    for col in df.columns:
        if df[col].dtype == 'object':
            nom.append(col)
            type_colonne.append(df[col].dtype)
            pourcentage_nan_val = f"{df[col].isna().mean() * 100:.1f} %"
            pourcentage_nan.append(pourcentage_nan_val)
            nombre_lignes_nan.append(df[col].isna().sum())
            valeur_min.append("type objet")
            valeur_max.append("type objet")
            valeur_moyenne.append("type objet")
            ecart_type.append("type objet")
            population_quartiles.append("type objet")
            Q1.append("type objet")
            Q2.append("type objet")
            Q3.append("type objet")
            count.append(df[col].value_counts().unique().sum())
            duplicates.append(df.duplicated().sum())
        else:
            nom.append(col)
            type_colonne.append(df[col].dtype)
            pourcentage_nan_val = f"{df[col].isna().mean() * 100:.1f} %"
            pourcentage_nan.append(pourcentage_nan_val)
            nombre_lignes_nan.append(df[col].isna().sum())
            valeur_min.append(df[col].min())
            valeur_max.append(df[col].max())
            valeur_moyenne.append(round(df[col].mean(), 2))
            ecart_type.append(df[col].std())
            # Calcul des quartiles
            quartiles = df[col].quantile([0.25, 0.5, 0.75])
            Q1_value = quartiles[0.25]
            Q2_value = quartiles[0.5]
            Q3_value = quartiles[0.75]
            Q1_population = df[df[col] <= Q1_value].shape[0]
            Q2_population = df[(df[col] > Q1_value) & (df[col] <= Q2_value)].shape[0]
            Q3_population = df[(df[col] > Q2_value) & (df[col] <= Q3_value)].shape[0]
            Q4_population = df[df[col] > Q3_value].shape[0]
            population_quartiles.append((Q1_population, Q2_population, Q3_population, Q4_population))
            Q1.append(Q1_value)
            Q2.append(Q2_value)
            Q3.append(Q3_value)
            count.append(df[col].value_counts().unique().sum())
            duplicates.append(df.duplicated().sum())

    dico_data = {
        'Colonnes': nom,
        'Type_de_colonne': type_colonne,
        'Pourcentage_nan': pourcentage_nan,
        'Nombre_lignes_Nan': nombre_lignes_nan,
        'Minimum': valeur_min,
        'Maximum': valeur_max,
        'Valeur_moyenne': valeur_moyenne,
        'Ecart_type': ecart_type,
        'Nombre_de_valeurs': count,
        'Population_quartiles': population_quartiles,
        'Valeur_quartile_1': Q1,
        'Valeur_quartile_2': Q2,
        'Valeur_quartile_3': Q3,
        'Lignes_dupliquées' : duplicates
        }

    df_nan = pd.DataFrame(viz_nan)

    dataset = pd.DataFrame(dico_data)

    styled_dataset = dataset.style.apply(lambda x: ['background-color: orange; color: black' if val != '0.0 %' else '' for val in x], subset=['Pourcentage_nan']).apply(lambda x: ['background-color: red; color: black' if val != 0 else '' for val in x], subset=['Nombre_lignes_Nan']).apply(lambda x: ['background-color: purple; color: black' if val != 0 else '' for val in x], subset=['Lignes_dupliquées'])

    display(styled_dataset)
    print('')
    print('')
    print('')
    display(df_nan)
    print(f"Taille du dataset nan : {df_nan.shape[0]} lignes")

