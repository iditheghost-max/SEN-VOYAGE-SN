import pandas as pd
import os

def maj_stock(df_stock, mouvement):
    """
    Met à jour le stock selon un mouvement (entrée ou sortie).
    Args:
        df_stock (pd.DataFrame): Stock actuel.
        mouvement (dict): {'produit': str, 'quantite': int, 'type': 'entree'|'sortie'}
    Returns:
        pd.DataFrame: Stock mis à jour.
    """
    produit = mouvement['produit']
    quantite = mouvement['quantite']
    if produit not in df_stock['produit'].values:
        df_stock = pd.concat([df_stock, pd.DataFrame([{'produit': produit, 'stock': 0}])], ignore_index=True)
    idx = df_stock[df_stock['produit'] == produit].index[0]
    if mouvement['type'] == 'entree':
        df_stock.at[idx, 'stock'] += quantite
    elif mouvement['type'] == 'sortie':
        df_stock.at[idx, 'stock'] -= quantite
    return df_stock

def charger_stock(fichier='stock.csv'):
    if os.path.exists(fichier):
        return pd.read_csv(fichier)
    return pd.DataFrame(columns=['produit', 'stock'])

def sauvegarder_stock(df_stock, fichier='stock.csv'):
    df_stock.to_csv(fichier, index=False)

# Exemple d'utilisation
if __name__ == "__main__":
    stock = charger_stock()
    mouvement = {'produit': 'PC', 'quantite': 5, 'type': 'entree'}
    stock = maj_stock(stock, mouvement)
    sauvegarder_stock(stock)
    print(stock)
