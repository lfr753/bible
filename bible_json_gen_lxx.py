import re
import json
import os

def parse_usfm_words(text):
     # Infos générales
    book_id_match = re.search(r'\\id\s+([A-Z0-9]+)', text)
    title_match = re.search(r'\\h\s+([^\n]+)', text)

    result = {
        "book_id": book_id_match.group(1) if book_id_match else None,
        "title": title_match.group(1) if title_match else None,
        "chapters": {}
    }

    chapters = re.split(r'(?=\\c\s+\d+)', text)
    for ch in chapters:
        ch_match = re.search(r'\\c\s+(\d+)', ch)
        if not ch_match:
            continue
        cnum = ch_match.group(1)
        result["chapters"][cnum] = {}

        verses = re.split(r'(?=\\v\s+\d+)', ch)
        for v in verses:
            v_match = re.match(r'\\v\s+(\d+)', v)
            if not v_match:
                continue
            vnum = v_match.group(1)

            words = []
            for w_match in re.finditer(
                r'\\w\s+([^\|]+)\|lemma="([^"]+)"\s+strong="([^"]+)"\s+x-morph="([^"]+)"\\w\*',
                v
            ):
                word_text, lemma, strong, x_morph = w_match.groups()
                words.append({
                    "text": word_text,
                    "lemma": lemma,
                    "strong": strong,
                    "x-morph": x_morph
                })

            # Chercher un apparatus JSON éventuel
            apparatus_match = re.search(
                r'\\zApparatusJson\s+({.*?})\\zApparatusJson\*', v, re.DOTALL
            )
            apparatus = json.loads(apparatus_match.group(1)) if apparatus_match else None

            result["chapters"][cnum][vnum] = {
                "words": words
            }
            if apparatus:
                result["chapters"][cnum][vnum]["apparatus"] = apparatus

    return result


def convert_usfm_folder(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print("ok")

    for filename in os.listdir(input_folder):
        if filename.lower().endswith(".usfm"):
            input_path = os.path.join(input_folder, filename)
            with open(input_path, "r", encoding="utf-8") as f:
                text = f.read()

            json_data = parse_usfm_words(text)

            # Nom du fichier JSON identique au fichier USFM
            base_name = os.path.splitext(filename)[0]
            output_path = os.path.join(output_folder, f"{base_name}.json")
            with open(output_path, "w", encoding="utf-8") as out_file:
                json.dump(json_data, out_file, ensure_ascii=False, indent=2)

            print(f"Converti : {filename} → {base_name}.json")


# ------------------------------
# Exemple d'utilisation
# ------------------------------
input_folder = "./usfm/lxx"   # dossier contenant les fichiers .usfm
output_folder = "./json/lxx"  # dossier où seront enregistrés les JSON

convert_usfm_folder(input_folder, output_folder)
