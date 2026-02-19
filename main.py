import requests
import json
import pandas as pd 

# je mets mes fonctions

def recuperer_donnees_api():
    cookies = {
        'PHPSESSID': 'ccc23f67e61ecf906bda9f736837f673',
        '_ga': 'GA1.1.884142582.1770825792',
        '_ga_VGVSFC38P2': 'GS2.1.s1770828057$o2$g0$t1770828057$j60$l0$h0',
    }
    
    headers = {
        'referer': 'https://results.timeto.com/schneider_electric_marathon_de_paris_2025/',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
    }
    
    params = {
        'act': 'GetRaceData',
        'rquest': '658',
    } 
    response = requests.get(
        'https://results.timeto.com/frontend/results/',
        params=params,
        cookies=cookies,
        headers=headers
    )
    data = json.loads(response.text)    
    
    print(f"Status: {response.status_code}")
    
    print(f"{len(data):,} coureurs disponibles")
    
    # Sauvegarder les données brutes complètes
    with open('data_brute_complete.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    with open('50k_coureurs.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
    
    return data

def search_continent(nationalite):
    if nationalite in ['KE', 'ET', 'DJ', 'MA', 'TZ', 'UG', 'ER', 'ZA', 'NG', 'CI', 'SN']:
        return 'Afrique'
    elif nationalite in ['FR', 'ES', 'IT', 'GB', 'DE', 'BE', 'NL', 'PT', 'PL', 'CH', 'AT', 'SE', 'NO']:
        return 'Europe'
    elif nationalite in ['JP', 'CN', 'IN', 'KR', 'TH', 'VN', 'MY', 'ID', 'PH']:
        return 'Asie'
    elif nationalite in ['US', 'CA', 'BR', 'MX', 'AR', 'CO', 'CL', 'PE']:
        return 'Amérique'
    elif nationalite in ['AU', 'NZ']:
        return 'Océanie'
    else:
        return 'Autre'
    return nationalite

def runner_cat(categorie):
    # je veux me baser sur le sexe et les catégories pour avoir les tranches d'âges => avoir une visu plus macro (large)
        # Déterminer le sexe
    if categorie.endswith('H'):
        sexe = "Homme"
    elif categorie.endswith('F'):
        sexe = "Femme"
    else:
        sexe = "Inconnu"

    # Déterminer la caté via et segmenter par tranche d'âge 
    if categorie in ['JUH', 'ESH', 'SEH', 'JUF', 'ESF', 'SEF']:
        tranche = "18-34 ans - [Jeune]"
    elif categorie in ['M0H', 'M1H', 'M0F', 'M1F']:
        tranche = "35-44 ans - [Jeune +]"
    elif categorie in ['M2H', 'M3H', 'M2F', 'M3F']:
        tranche = "45-54 ans - [Mid - Senior] "
    elif categorie in ['M4H', 'M5H', 'M4F', 'M5F']:
        tranche = "55-64 ans - [Senior]"
    elif categorie in ['M6H', 'M7H', 'M8H', 'M9H', 'M10H', 'M6F', 'M7F', 'M8F', 'M9F']:
        tranche = "65+ ans - [Senior +]"
    else:
        tranche = "Autre"
    
    return {
        'sexe_custom': sexe,
        'tranche_age': tranche,
        'cust_category': f"{tranche} ___ ({sexe})"
    }

def clean_data(nombre_max=52000):
    coureurs_top50K = data[:52000]
    runners_clean = []
    for coureur in coureurs_top50K:
        # Extraire les infos de base
        coureur_clean = {
            'place': coureur['computedGeneralRanking'],
            'nom': coureur['lastName'],
            'prenom': coureur['firstName'],
            'sexe': coureur['sex'],
            'categorie': coureur['category'],
            'nationalite': coureur['nationality'],
            'temps': coureur['computedRealTime'],
            'allure': coureur['computedPace'],
            'vitesse_moy': coureur['computedAverageSpeed'],
        }
        
        # Ajouter continent
        coureur_clean['continent'] = search_continent(coureur['nationality'])
        
        # Ajouter catégorisation personnalisée
        cat_info = runner_cat(coureur['category'])
        coureur_clean['cust_category'] = cat_info['cust_category']
        coureur_clean['sexe_custom'] = cat_info['sexe_custom']
        coureur_clean['tranche_age'] = cat_info['tranche_age']
        
        runners_clean.append(coureur_clean)
    
    print(f"{len(runners_clean):,} coureurs nettoyés\n")
    
    return runners_clean

def sauvegarder_json(nom_fichier):
    with open(nom_fichier, "w", encoding='utf-8') as f:
        json.dump(coureurs, f, indent=2, ensure_ascii=False)

def afficher_apercu(nombre=100):
    print(f" APERÇU DES {nombre} PREMIERS")
    for i in range(nombre):
        c = coureurs[i]
        print(f"{c['place']:4d}. {c['prenom']:12} {c['nom']:15} - {c['temps']} - {c['cust_category']}")


def sauvegarder_csv(nom_fichier):
    df = pd.DataFrame(coureurs)
    df.to_csv("50k_coureurs_propres.csv", encoding='utf-8', index=False)

# mon "if __name__"

if __name__ == "__main__":

    cookies = {
        'PHPSESSID': 'ccc23f67e61ecf906bda9f736837f673',
        '_ga': 'GA1.1.884142582.1770825792',
        '_ga_VGVSFC38P2': 'GS2.1.s1770828057$o2$g0$t1770828057$j60$l0$h0',
    }
    
    headers = {
        'referer': 'https://results.timeto.com/schneider_electric_marathon_de_paris_2025/',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
    }
    params = {
        'act': 'GetRaceData',
        'rquest': '658'} 
    response = requests.get('https://results.timeto.com/frontend/results/', params=params, cookies=cookies, headers=headers)
    data = json.loads(response.text)    

    # Les 50 000 conéttoyés
    coureurs = clean_data(nombre_max=57000)
    
    # Sauvegarder
    sauvegarder_json("50k_coureurs_propres.json")
    
    # Afficher aperçu
    afficher_apercu(nombre=101)
    
    #pour avoir le csv
    sauvegarder_csv("50k_coureurs_propres.csv")