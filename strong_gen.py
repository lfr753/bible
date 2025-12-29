import re
import json
import os

def parse_html(text):

    data = []
    content = re.search(
        r'Mot original</b></td>[\s\n]*<td bgcolor=#D2BB17><b>Origine du mot</b></td>[\s\n]*</tr>[\s\n]*<tr>[\s\n]*<td.*?>.*?</td>[\s\n]*<td.*?>(.*?)</td>',
        text,
        re.DOTALL
    )
    origin = content.group()[1]
    
    content = re.search(
        r'Mot translittéré</b></td>[\s\n]*<td bgcolor=#D2BB17><b>Entrée du <acronym title="Theological Dictionary of the New Testament">TDNT</acronym></b></td>[\s\n]*</tr>[\s\n]*<tr>[\s\n]*<td.*?>(.*?)</td>[\s\n]*<td.*?>(.*?)</td>',
        text,
        re.DOTALL
    )
    
    trans = content.group()[1]
    tdnt = content.group()[2]
    
    content = re.search(
        r'Prononciation phonétique</b></td>[\s\n]*<td bgcolor=#D2BB17><b>Type de mot</b></td>[\s\n]*</tr>[\s\n]*<tr>[\s\n]*<td.*?>(.*?)<a href=.*?</a></td>[\s\n]*<td.*?>(.*?)</td>',
        text,
        re.DOTALL
    )
    
    phon = content.group()[1]
    typ = content.group()[2]
    
    content = re.search(
        r'Définition :</b></td>[\s\n]*</tr>[\s\n]*<tr>[\s\n]*<td colspan=2>(.*?)</td>[\s\n]*</tr>[\s\n]*<tr>[\s\n]*<td colspan=2 bgcolor=#D2BB17><b>Traduction générale par :</b></td>[\s\n]*</tr>[\s\n]*<tr>[\s\n]*<td colspan=2>(.*?)</td>',
        text,
        re.DOTALL
    )

    definition = content.group()[1]    
    trad = content.group()[2]
    
    data.append({
        "origin": origin,
        "trans": trans,
        "tdnt": tdnt,
        "phon": phon,
        "typ": typ,
        "definition": definition,
        "trad": trad
    })

    return data


def convert_html_folder(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print("ok")

    for filename in os.listdir(input_folder):
        if filename.lower().endswith(".html"):
            input_path = os.path.join(input_folder, filename)
            with open(input_path, "r") as f:
                print(input_path)
                text = f.read()

            if filename in ['strong-grec-4495.html', 'strong-grec-825.html']: continue
            json_data = parse_html(text)

            # Nom du fichier JSON identique au fichier USFM
            base_name = os.path.splitext(filename)[0].replace("strong-grec-", "")
            output_path = os.path.join(output_folder, f"{base_name}.json")
            with open(output_path, "w", encoding="utf-8") as out_file:
                json.dump(json_data, out_file, ensure_ascii=False, indent=2)

            print(f"Converti : {filename} → {base_name}.json")


# ------------------------------
# Exemple d'utilisation
# ------------------------------
input_folder = "./strong/strong_grec"   # dossier contenant les fichiers .usfm
output_folder = "./strong/G"  # dossier où seront enregistrés les JSON
# ------------------------------
# input_folder = "./usfm/ugnt"   # dossier contenant les fichiers .usfm
# output_folder = "./json/ugnt"  # dossier où seront enregistrés les JSON
# ------------------------------
# input_folder = "./usfm/lxx"   # dossier contenant les fichiers .usfm
# output_folder = "./json/lxx"  # dossier où seront enregistrés les JSON

convert_html_folder(input_folder, output_folder)
