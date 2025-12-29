import subprocess
from bs4 import BeautifulSoup
import re
import time

chap_num = [
    50,
    40,
    27,
    36,
    34,
    24,
    21,
    4,
    31,
    24,
    22,
    25,
    29,
    36,
    10,
    13,
    10,
    42,
    150,
    31,
    12,
    8,
    66,
    52,
    5,
    48,
    12,
    14,
    3,
    9,
    1,
    4,
    7,
    3,
    3,
    3,
    2,
    14,
    4,
    28,
    16,
    24,
    21,
    28,
    16,
    16,
    13,
    6,
    6,
    4,
    4,
    5,
    3,
    6,
    4,
    3,
    1,
    13,
    5,
    5,
    3,
    5,
    1,
    1,
    1,
    22]

book_name = [
    "GEN",
    "EXO",
    "LEV",
    "NUM",
    "DEU",
    "JOS",
    "JDG",
    "RUT",
    "1SA",
    "2SA",
    "1KI",
    "2KI",
    "1CH",
    "2CH",
    "EZR",
    "NEH",
    "EST",
    "JOB",
    "PSA",
    "PRO",
    "ECC",
    "SNG",
    "ISA",
    "JER",
    "LAM",
    "EZK",
    "DAN",
    "HOS",
    "JOL",
    "AMO",
    "OBA",
    "JON",
    "MIC",
    "NAM",
    "HAB",
    "ZEP",
    "HAG",
    "ZEC",
    "MAL",
    "MAT",
    "MRK",
    "LUK",
    "JHN",
    "ACT",
    "ROM",
    "1CO",
    "2CO",
    "GAL",
    "EPH",
    "PHP",
    "COL",
    "1TH",
    "2TH",
    "1TI",
    "2TI",
    "TIT",
    "PHM",
    "HEB",
    "JAS",
    "1PE",
    "2PE",
    "1JN",
    "2JN",
    "3JN",
    "JUD",
    "REV"]


bible = "BDS"
bible_id = "21"
has_intro = True

bible = "NBS"
bible_id = "104"
has_intro = False

bible = "LSG"
bible_id = "93"
has_intro = True

for book in range(len(book_name)):
# for book in range(13,14):
    print(f"{book_name[book]} : {chap_num[book]}")

    if has_intro:
        with open(f"{bible}/{book+1}.0.html", "w") as f:
            url = f"https://www.bible.com/fr/bible/{bible_id}/{book_name[book]}.INTRO1.{bible}"
            print(url)

            # Exécute wget et récupère la sortie dans une variable
            result = subprocess.run(
                ["wget", "-qO-", url],  # -q = silencieux, -O- = écrit sur stdout
                capture_output=True,
                text=True
            )

            html = result.stdout

            soup = BeautifulSoup(html, "html.parser")
            elem = soup.find("div", {"data-testid":"chapter-content" })
            elem = soup.find("div", {"class":re.compile(r"^ChapterContent_chapter")})

            f.write(str(elem))

        time.sleep(1)

    for chap in range(1, chap_num[book]+1):
        with open(f"{bible}/{book+1}.{chap}.html", "w") as f:
            url = f"https://www.bible.com/fr/bible/{bible_id}/{book_name[book]}.{chap}.{bible}"
            print(url)

            # Exécute wget et récupère la sortie dans une variable
            result = subprocess.run(
                ["wget", "-qO-", url],  # -q = silencieux, -O- = écrit sur stdout
                capture_output=True,
                text=True
            )

            html = result.stdout

            soup = BeautifulSoup(html, "html.parser")
            elem = soup.find("div", {"data-testid":"chapter-content" })
            elem = soup.find("div", {"class":re.compile(r"^ChapterContent_chapter")})

            f.write(str(elem))

        time.sleep(1)

    
