import ast
import copy
import csv
import random
import sys
from langdetect import detect


# from googletrans import Translator
# from langcodes import Language

# Todo: Frage, ob Sprache korrekt ist implementieren
def main():
    global output_language_words
    global vocabulary_statistic
    global vocabulary
    global input_language
    global output_language
    global swapped_vocabulary
    choose_method_of_input()
    print(vocabulary)
    first_key = next(iter(vocabulary.keys()))
    language_one = detect_language(first_key)
    language_two = detect_language(vocabulary[first_key])
    # language_one = input("Geben sie nun die Sprache an, dessen Wort zuerst gezeigt wird bei allen "
    # "Eingabeformaten.\n1. Sprache: ")
    # language_two = input("Geben sie nun die Sprache an, dessen Wort als zweites gezeigt wird bei allen "
    # "Eingabeformaten.\n2. Sprache: ")
    direction_text = f"Es würden nun die Vokabeln von {convert_language(language_two)} nach {convert_language(language_one)} abgefragt werden. \n1. Das ist nicht richtig!\n2. Das ist richtig!\n3. Beide Richtungen sollen abgefragt werden!\nEingabe ('1', '2' oder '3'): "
    direction = input(direction_text)
    if direction == "1":  # TODO
        input_language = input(
            "Bitte geben Sie die Sprache an, in der Sie die Antworten eingeben möchten:\nEingabesprache: ")
        # output_language = input("Bitte geben Sie die Sprache an, in der Sie die Vokabeln sehen möchten.\n"
        # "Systemausgabesprache: ")
        input_language_code = convert_language(input_language).lower()
        # output_language_code = convert_language(output_language).lower()
        if language_two.lower() == input_language_code:
            output_language = convert_language(language_one)
            input_language = convert_language(language_two)
            # and language_one.lower() == output_language_code) or (
            # language_two.lower() == input_language_code or language_one.lower() == output_language_code)
            # dann Erkennung ohne input language, welche Sprache
            # print("\n\n\n\n\n\nswap_vocabulary\n\n\n\n\n\n\n")
            for key, value in vocabulary.items():
                swapped_vocabulary[value] = key
            vocabulary = swapped_vocabulary
        else:
            output_language = convert_language(language_two)
            input_language = convert_language(language_one)
            print("language_one.lower(): ", language_one.lower())
            print("language_two.lower(): ", language_two.lower())
            # print("convert_language(output_language.lower()).lower(): ", output_language_code)
            print("convert_language(input_language.lower()).lower(): ", input_language_code)
    else:
        output_language = convert_language(language_two)
        input_language = convert_language(language_one)
        print("output_language: ", output_language)
    vocabulary_statistic = copy.deepcopy(vocabulary)
    initialize_vocabulary_statistic()
    output_language_words = list(vocabulary.values())
    random.shuffle(output_language_words)
    # zu_uebersetzendes_text = input("Geben Sie den zu übersetzenden Text ein: ")

    # uebersetzung = translate_with_language_names(zu_uebersetzendes_text, output_language)
    # print("Die Übersetzung von '{}' nach {} lautet: {}".format(zu_uebersetzendes_text, output_language, uebersetzung))
    print('Wenn sie die falschen Vokabeln ausgeben wollen, drücken sie in irgendein Eingabefeld das Wort "Falsche"!')
    create_csv_file_with_wrong_answers()  # Datei für Falsche Vokabeln wird erstellt
    create_csv_file_with_right_answers()  # Datei für Richtige Vokabeln wird erstellt
    test_users_vocabulary()
    if direction == "3":
        print(
            "\n\n\n\n\n\n\n\nDie Statistik vom Durchlauf in die 1. Richtung wurde oben bereits erstellt. Nun folgt die "
            "Abfrage in die zweite Richtung!\n")
        add_right_answers_to_csv_file("Ergebnisse der Abfrage", " in die zweite Richtung: ")
        add_wrong_answers_to_csv_file("Ergebnisse der Abfrage", " in die zweite Richtung: ")
        for key, value in vocabulary.items():
            swapped_vocabulary[value] = key
        vocabulary = swapped_vocabulary
        vocabulary_statistic = copy.deepcopy(vocabulary)
        initialize_vocabulary_statistic()
        output_language = convert_language(language_one)
        input_language = convert_language(language_two)
        output_language_words = list(vocabulary.values())
        random.shuffle(output_language_words)
        print(
            'Wenn sie die falschen Vokabeln ausgeben wollen, drücken sie in irgendein Eingabefeld das Wort "Falsche"!')
        test_users_vocabulary()
    # translator = Translator()
    # Ergebnis=translator.translate(zu_uebersetzendes_text,"en", "auto")
    # print(Ergebnis)


def choose_method_of_input():
    global relative_path
    global vocabulary
    global translate_spontaneous
    global vocabulary_list
    global translation
    number_of_method: str = input(
        "Möchten Sie die im Code voreingetragen Vokabeln verwenden, oder im nächsten Schritt eine Möglichkeit zur "
        "eigenen "
        "Eingabe der Vokabeln auswählen? \nGeben Sie \n'1' für eigene Vokabeln verwenden oder \n'2' für im Code "
        "voreingetragene"
        "Vokabeln verwenden ein!\n Eingabe: ")
    if number_of_method.lower() == "1":
        number_of_method = input("Wählen Sie nun eine Möglichkeit zur eigenen Eingabe!\n'1' für Vokabeln aus CSV Datei "
                                 "eingeben (1. Spalte Fremdsprache, 2. Spalte eigene Sprache)\n'2' für Vokabeln als Python "
                                 "Dictionary (ohne Dokument (im Textformat))eingeben\n'3' für Vokabeln im CSV Format, "
                                 "also Vokabeln mit Trennzeichen getrennt und Zeilenumbrüchen als '+' dargestellt einlesen\n'4' "
                                 "für Ausgabevokabel erst bei Abfrage eingeben, welche dann automatisch übersetzt wird\n'5' "
                                 "für nur Systemausgabevokabeln angeben.\nEingabe: ")
        if number_of_method.lower() == "1":  # CSV Datei als Datei
            number_of_method = input(
                "Wählen Sie eine der folgenden Möglichkeiten zum Finden der Datei:\n'1' für relativen Pfad "
                "angeben\n'2' für die 'Vokabeln.csv' Datei verwenden(muss vorher von Ihnen "
                "erstellt/bearbeitet werden).\n Eingabe: ")
            if number_of_method.lower() == "1":  # relativen Pfad angeben
                relative_path = input("Relativer Pfad: ")
            elif number_of_method.lower() == "2":  # Standard CSV Datei verwenden
                relative_path = "../../csv_documents/Vokabeln.csv"
            else:
                print("Sie haben haben eine ungültige Eingabe getätigt, bitte versuchen sie es erneut.")
                sys.exit()
            create_dict_vocabulary_out_of_csv(relative_path)
        elif number_of_method.lower() == "2":  # Python Dictionary
            vocabulary = ast.literal_eval(
                input("Geben Sie die Vokabeln als Python Dictionary in einer Zeile ein. Python Dictionary: "))
        elif number_of_method.lower() == "3":
            csv_text = input("Bitte geben Sie den Text ihrer CSV-Datei ein.\nText der CSV-Datei: ")
            delimiter = input("Bitte geben Sie das Trennzeichen an!\nTrennzeichen: ")
            create_dict_vocabulary_out_of_csv_text(csv_text, delimiter=delimiter)
        elif number_of_method.lower() == "4":  # TODO SCHWER 4: Übersetzung: Vokabeln erst bei Abfrage eingeben und dann
            # prüfen, ob das eingegebene Wort laut Wörterbuch stimmen könnte
            global read_vocabulary
            read_vocabulary = True
            translate_spontaneous = True
        elif number_of_method.lower() == "5":  # TODO SCHWER 3 (3-6): Vokabeln erst bei Abfrage prüfen, ob sie laut Wörterbuch stimmen
            # TODO 2: Übersetzung: Vokabeln Liste übersetzen und in "vocabulary" (dict) umwandeln
            translation = True
            translate_spontaneous = True
            number_of_method = input("Wählen Sie nun eine Möglichkeit zur eigenen Eingabe von nur den "
                                     "Systemausgabe-sprachen-vokabeln\n'1' für CSV-Datei\n'2' für als Python "
                                     "Liste\n'3' für Vokabeln im CSV-Format(einfach alle Vokabeln im Text Format in "
                                     "einer Zeile durch ein Trennzeichen getrennt)\n Eingabe: ")
            if number_of_method.lower() == "1":  # CSV Datei als Datei
                number_of_method = input(
                    "Wählen Sie eine der folgenden Möglichkeiten zum Finden der Datei:\n'1' für relativen Pfad "
                    "angeben\n'2' für die 'Vokabeln.csv' Datei verwenden(muss vorher von Ihnen "
                    "erstellt/bearbeitet werden).\n Eingabe: ")
                if number_of_method.lower() == "1":  # relativen Pfad angeben
                    relative_path = input("Relativer Pfad: ")
                    delimiter = input("Bitte geben Sie das Trennzeichen an!\nTrennzeichen: ")
                elif number_of_method.lower() == "2":  # Standard CSV Datei verwenden
                    relative_path = "../../csv_documents/Vokabeln.csv"
                    delimiter = input("Bitte geben Sie das Trennzeichen an!\nTrennzeichen: ")
                else:
                    print("Sie haben haben eine ungültige Eingabe getätigt, bitte versuchen Sie es erneut.")
                    sys.exit()
                vocabulary_list = create_list_vocabulary_of_csv(relative_path, delimiter=delimiter)
                vocabulary_list = list(filter(lambda x: len(x) > 0, vocabulary_list))
            elif number_of_method.lower() == "2":  # Python Liste
                vocabulary_list = eval(
                    input("Geben Sie die Vokabeln als Python Liste in einer Zeile ein. Python Liste: "))
                if translation:
                    create_dict_vocabulary_out_of_python_list(input(
                        "Geben Sie die Sprache ein, in die ihre Vokabeln übersetzt werden sollen! Sprache: "))  # TODO: nur bei Übersetzung abfragen
            elif number_of_method.lower() == "3":
                # Spalte (weil nur eine Sprache)
                vocabulary_list = input(
                    "Schreiben Sie die Wörter in eine Zeile, die mit einem Trennzeichen ihrer Wahl getrennt sind. Wörter: ")
                vocabulary_list = vocabulary_list.split(input("Geben Sie nun das Trennzeichen ein! Trennzeichen: "))
            print("Vocabulary Liste: ", vocabulary_list)
        else:
            print("Sie haben keine gültige Eingabe verwendet. Bitte versuchen Sie es erneut.")
            sys.exit()
    # TODO SCHWER 5: Übersetzung: In beide Richtungen übersetzen
    # TODO 6: Code in Englisch umschreiben (außer Konsolenausgabe)
    # TODO 7: Kommentare zur besseren Verständlichkeit des Codes schreiben
    elif number_of_method.lower() == "2":
        create_dict_vocabulary_out_of_code()
    else:
        print("Sie haben keine gültige Eingabe verwendet. Bitte versuchen Sie es erneut.")
        sys.exit()
    change_voc_list()
    print(vocabulary)


def change_voc_list():
    global vocabulary
    bool_number_vocabulary = input(
        "Möchten Sie alle Vokabeln lernen, oder nur eine bestimmte Anzahl?\n'1' für alle Vokabeln\n'2' für bestimmte "
        "Anzahl\nEingabe: ")
    if bool_number_vocabulary == 2:
        number_vocabulary_min: int = int(input("Geben sie nun den Anfangsindex der gewünschten Vokabeln an.\nDie "
                                               "Vokabeln fangen mit 0 an, in der Reihenfolge, in der Sie es "
                                               "eingegeben haben.\n Index: "))
        number_vocabulary_max: int = int(input("Geben sie nun den Endindex der gewünschten Vokabeln an. Dieser soll "
                                               "der Index der letzten gewünschten Vokabel sein.\nDie"
                                               "Vokabeln fangen mit 0 an, in der Reihenfolge, in der Sie es "
                                               "eingegeben haben.\n Index: "))
        voc_dict_changed = {}
        x: int = 0
        for key_voc, value_voc in vocabulary.items():
            if number_vocabulary_min <= x <= number_vocabulary_max:
                voc_dict_changed[key_voc] = value_voc
        vocabulary = voc_dict_changed


def detect_language(frase):
    language = detect(frase)
    return language


def create_dict_vocabulary_out_of_python_list(destinated_lang):
    pass
    # for word in vocabulary_list:
    #   vocabulary[word] = translate_word(word, destinated_lang, detect_language(word))

    # def translate_word(word, language, src_lang):
    """
    Translates a word from English to a specified language.

    Args:
    word (str): The word to be translated.
    language (str): The language to translate the word to, in written form (e.g. "Spanish", "French", etc.).

    Returns:
    str: The translated word.
    """
    # Initialize the translator object
    # translator = Translator()
    # Detect the source language (assume it's English for this example)
    # Translate the word
    # translated = translator.translate(word, src=src_lang, dest=language)
    # Return the translated word
    # return translated.text


def convert_language(lang):
    language_mapping = {
        "en": "englisch",
        "de": "deutsch",
        "fr": "französisch",
        "es": "spanisch",
        "it": "italienisch",
        "pt": "portugiesisch",
        "ru": "russisch",
        "zh": "chinesisch",
        "ja": "japanisch",
        "ar": "arabisch",
        "hi": "hindi",
        "ko": "koreanisch",
        "tr": "türkisch",
        "nl": "niederländisch",
        "pl": "polnisch",
        "sv": "schwedisch",
        "fi": "finnisch",
        "no": "norwegisch"}
    lang = lang.lower()
    if lang in language_mapping:
        return language_mapping[lang]

        # Wenn nicht, suchen wir nach dem Sprachennamen im Dictionary
    for code, language in language_mapping.items():
        if language.lower() == lang.lower():
            return code

        # Wenn weder ein gültiges Kürzel noch ein Name gefunden wurde, geben wir eine entsprechende Nachricht aus
    return "Ungültiges Sprachkürzel oder Sprache"


def create_list_vocabulary_of_csv(file_path, delimiter=","):
    word_list = []
    with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=delimiter)
        for row in csv_reader:
            word_list.extend(row)
    return word_list


def create_dict_vocabulary_out_of_csv(csv_file):
    global vocabulary
    """
    Convert CSV file to Python dictionary.

    Args:
    csv_file (str): Path to the CSV file.

    Returns:
    dict: Dictionary containing the data from the CSV file.
    """
    vocabulary = {}
    with open(csv_file, 'r', newline='', encoding='utf-8') as file:
        if file.readline().strip() == '':
            print("Die CSV-Datei ist leer.")
            sys.exit()
        dialect = csv.Sniffer().sniff(file.read(1024))
        file.seek(0)
        reader = csv.DictReader(file, dialect=dialect)
        for row in reader:
            vocabulary[row[reader.fieldnames[0]]] = row[reader.fieldnames[1]]


def create_dict_vocabulary_out_of_code():
    global vocabulary
    vocabulary = {
        "el ambiente": "Die Atmosphäre",
        "alegre": "fröhlich",
        "fascinante": "faszinierend",
        "relajado": "entspannt",
        "optimista": "optimistisch",
        "agradable": "angenehm",
        "energético": "energiegeladen",
        "pacífico": "friedlich",
        "triste": "traurig",
        "aburrido": "langweilig",
        "extraño": "seltsam",
        "deprimente": "deprimierend",
        "violento": "gewalttätig",
        "tenso": "gespannt",
        "perturbador": "beunruhigend",
        "el teclado electrónico": "das Keyboard",
        "el fagót": "das Fagott",
        "la batería": "das Schlagzeug",
        "el acordeón": "das Akkordeon",
        "la guitarra": "die Gitarre",
        "la flauta": "die Flöte",
        "la guitarra eléctrica/ el bajo": "die E-Gitarre/der Bass",
        "la trompa": "das Horn",
        "el violín": "die Violine",
        "el xilófono": "das Xylophon",
        "la trompeta": "die Trompete",
        "la arpa": "die Harfe",
        "el piano": "das Klavier",
        "el piano de cola": "der Flügel",
        "saxofón": "das Saxophon",
        "la flauta traversa": "die Querflöte",
        "el trombón": "die Posaune",
        "la tuba": "die Tuba",
        "el clarinete": "das Klarinette",
        "el tambor": "die Trommel",
        "la voz": "die Stimme",
        "suave": "sanft",
        "profunda": "tief",
        "áspera": "rau",
        "velada": "verschleiert",
        "el dueto": "das Duett",
        "fuerte": "laut/stark",
        "aguda": "hoch",
        "el coro": "der Chor",
        "la pausa": "die Pause",
        "la nota": "die Note",
        "la clave": "der Takt",
        "la negra": "die Viertelnote",
        "la blanca": "die Halbe Note",
        "la corchea": "die Achtelnote",
        "monótono": "monoton",
        "lento": "langsam",
        "enérgico": "energisch",
        "rápido": "schnell",
        "exótico": "exotisch",
        "particular": "besonders",
        "el amor": "die Liebe",
        "el/la amante": "der/die Liebhaber/in",
        "el verano": "der Sommer",
        "la vida": "das Leben",
        "bailar": "tanzen",
        "la alegría": "die Freude",
        "el desamor": "die Liebesenttäuschung",
        "el/la enemigo/-a": "der/die Feind/in",
        "el invierno": "der Winter",
        "la muerte": "der Tod",
        "descansar": "ausruhen",
        "la tristeza": "die Traurigkeit"
    }


def create_dict_vocabulary_out_of_csv_text(csv_text, delimiter=','):
    vocabular = {}
    lines = csv_text.split('+')  # Teilt den Text in Zeilen auf

    for line in lines:
        if line.strip():  # Ignoriert leere Zeilen
            word, translation = line.strip().split(delimiter)  # Trennt Wort und Übersetzung
            vocabulary[word.strip()] = translation.strip()  # Fügt das Wort und die Übersetzung zum Wörterbuch hinzu
    return vocabular


def translate_with_language_names(text, target_language):
    # Umwandeln der ausgeschriebenen Zielsprache in einen ISO-Sprachcode
    language_codes = {
        'deutsch': 'de',
        'englisch': 'en',
        'spanisch': 'es',
        'französisch': 'fr',
        'italienisch': 'it',
    }
    target_lang_code = language_codes.get(target_language.lower())

    if not target_lang_code:
        return "Fehler: Die Zielsprache wurde nicht erkannt."

    # Übersetzung durchführen und automatische Erkennung der Ausgangssprache verwenden
    # translator = Translator()
    # translated_text = translator.translate(text, dest=target_lang_code)

    # return translated_text.text


def check_if_wrong_answers_print(input_par):
    if input_par.lower() == "falsche":
        if len(wrong_ones.items()) == 0:
            print("Sie hatten noch keine Vokabeln falsch!")
        else:
            print("\nBisher hatten Sie folgende Vokabeln falsch: ")
            for key, value in wrong_ones.items():
                print(f"-    '{key}' heißt '{value}' auf ", input_language.lower())
            print("")
        return True
    return False


def create_csv_file_with_wrong_answers():
    # Öffne eine neue CSV-Datei im Schreibmodus
    with open('../../csv_documents/Nicht_gekonnt.csv', 'w', newline='') as csvfile:
        # Erstelle einen CSV-Writer
        csv_writer = csv.writer(csvfile)
        # Schreibe die Kopfzeile (Spaltennamen)
        csv_writer.writerow([input_language, output_language, 'Antwort'])


def add_wrong_answers_to_csv_file(input_language_word, output_language_word):
    with open('../../csv_documents/Nicht_gekonnt.csv', 'a', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow([input_language_word, output_language_word, user_solution])


def create_csv_file_with_right_answers():
    # Öffne eine neue CSV-Datei im Schreibmodus
    with open('../../csv_documents/Gekonnt.csv', 'w', newline='') as csvfile:
        # Erstelle einen CSV-Writer
        csv_writer = csv.writer(csvfile)
        # Schreibe die Kopfzeile (Spaltennamen)
        csv_writer.writerow([input_language, output_language])


def add_right_answers_to_csv_file(input_language_word, output_language_word):
    with open('../../csv_documents/Gekonnt.csv', 'a', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow([input_language_word, output_language_word])


def process_and_print_statistic(output_type, delimiter_vok1, delimiter_vok2):
    # TODO: falsche Ausgabe bei 2 Durchläufen mit nur einer Vokabel(1. falsch nach Auswahl ob falsch oder richtig und 2. richtig)
    # Vokabeln wurden durch csv Datei eingelesen mit vorgegebenem Pfad
    # -->Ausgabe: dass im ersten Durchlauf keine falsche Vokabel war.
    # TODO 1: Statistik im u.a. csv Format ausgeben!
    # TODO: Ursprungs-csv-Datei bearbeiten bei Falsch und richtig und Hinweis der höheren Funktionalität mit CSV
    vokabeln_statistik_copy = copy.deepcopy(vocabulary_statistic)
    groesste_zahl = 0
    for key, value in vokabeln_statistik_copy.items():
        zahl = value[vocabulary[key]]
        if zahl > groesste_zahl:
            groesste_zahl = zahl
    anzahl_der_durchlaeufe_richtig = groesste_zahl + 1
    # print("Durchläufe:", anzahl_der_durchlaeufe_richtig)
    print("Sie hatten nach ", anzahl_der_durchlaeufe_richtig,
          " Durchläufen alles richtig. Herzlichen Glückwunsch!\n")
    statistik_anzahl_falsche = {}
    statistik_falsche_woerter = {}
    statistik_falsche_woerter_without_description = {}
    statistik_richtige_woerter_without_description = {}
    for x in range(anzahl_der_durchlaeufe_richtig):
        x = f"Durchlauf:_{x}"
        statistik_falsche_woerter_without_description[x] = {}
        statistik_richtige_woerter_without_description[x] = {}
    statistik_anzahl_richtige = {}
    statistik_richtige_woerter = {}
    # print("richtig: ", anzahl_der_durchlaeufe_richtig)
    # print(vokabeln_statistik_copy)
    # print(vokabeln_statistik_copy)
    for x in range(0, anzahl_der_durchlaeufe_richtig, 1):
        # print("durchlaufe: ", x)
        durchlauf_nummer = f"Durchlauf:_{x}"
        statistik_falsche_woerter[durchlauf_nummer] = []
        statistik_richtige_woerter[durchlauf_nummer] = []
        # print(f"Durchlauf_Numemr: {durchlauf_nummer}")
        statistik_anzahl_falsche[durchlauf_nummer] = 0
        statistik_anzahl_richtige[durchlauf_nummer] = 0
        for key, value in vocabulary_statistic.items():
            if int(vokabeln_statistik_copy[key][vocabulary[key]]) - 1 >= 0:
                vokabeln_statistik_copy[key][vocabulary[key]] = int(vokabeln_statistik_copy[key][vocabulary[key]]) - 1
                statistik_anzahl_falsche[durchlauf_nummer] = statistik_anzahl_falsche[durchlauf_nummer] + 1
                statistik_falsche_woerter[durchlauf_nummer].append(
                    f"-    '{key}', was auf {output_language.lower()} '{vocabulary[key]}' heißt!")
                statistik_falsche_woerter_without_description[durchlauf_nummer][key] = vocabulary[key]
            # print(f"Du hattest {key}, was {vokabeln[key]} heißt, ")
            elif vokabeln_statistik_copy[key][vocabulary[key]] == 0:
                statistik_anzahl_richtige[durchlauf_nummer] = statistik_anzahl_richtige[durchlauf_nummer] + 1
                vokabeln_statistik_copy[key][vocabulary[key]] = -10
                statistik_richtige_woerter[durchlauf_nummer].append(
                    f"-    '{key}', was auf {output_language.lower()} '{vocabulary[key]}' heißt!")
                statistik_richtige_woerter_without_description[durchlauf_nummer][key] = vocabulary[key]
    keine = False
    for x in range(0, anzahl_der_durchlaeufe_richtig, 1):  # print wrong and right ones sorted by runs (x)
        durchlauf_nummer = f"Durchlauf:_{x}"
        if statistik_anzahl_falsche[durchlauf_nummer] > 1:  # print more than one wrong ones in the run given by x
            print(
                f"Sie hatten im {x + 1}. Durchlauf {statistik_anzahl_falsche[durchlauf_nummer]} falsche/nicht gewusste "
                f"Vokabeln und")
            print(f"Diese sind: \n")
            if output_type == "1":  # with delimiter
                for key, value in statistik_falsche_woerter_without_description[durchlauf_nummer].items():
                    print(delimiter_vok1, key, delimiter_vok2, value, delimiter_vok1)
                s_f_w_w_d_values = list(statistik_falsche_woerter_without_description[durchlauf_nummer].values())
                s_f_w_w_d_keys = list(statistik_falsche_woerter_without_description[durchlauf_nummer].keys())
                print(f"{convert_language(detect_language(s_f_w_w_d_values[0]))}e Wörter: {s_f_w_w_d_values}")
                print(f"{convert_language(detect_language(s_f_w_w_d_keys[0]))}e Wörter: {s_f_w_w_d_keys}")
            if output_type == "2":  # in Dictionary
                print(statistik_falsche_woerter_without_description[durchlauf_nummer])
            if output_type == "3":  # with explanation
                for element in statistik_falsche_woerter[durchlauf_nummer]:
                    print(element, "\n")
        elif statistik_anzahl_falsche[durchlauf_nummer] == 1:  # print the only one wrong in the run given by x
            print(
                f"Sie hatten im {x + 1}. Durchlauf eine falsche/nicht gewusste Vokabel")
            print(f"Diese ist: ")
            if output_type == "1":  # with delimiter
                for key, value in statistik_falsche_woerter_without_description[durchlauf_nummer].items():
                    print(delimiter_vok1, key, delimiter_vok2, value, delimiter_vok1)
                s_f_w_w_d_values = list(statistik_falsche_woerter_without_description[durchlauf_nummer].values())
                s_f_w_w_d_keys = list(statistik_falsche_woerter_without_description[durchlauf_nummer].keys())
                print(f"{convert_language(detect_language(s_f_w_w_d_values[0]))}e Wörter: {s_f_w_w_d_values}")
                print(f"{convert_language(detect_language(s_f_w_w_d_keys[0]))}e Wörter: {s_f_w_w_d_keys}")
            if output_type == "2":  # in Dictionary
                print(statistik_falsche_woerter_without_description[durchlauf_nummer])
            if output_type == "3":  # with explanation
                for element in statistik_falsche_woerter[durchlauf_nummer]:
                    print(element, "\n")
        else:  # print that there is no wrong one in that run given by x
            print(
                f"Sie hatten im {x + 1}. Durchlauf keine falsche/nicht gewusste Vokabeln und", end=" ")
            keine = True
        if statistik_anzahl_richtige[durchlauf_nummer] > 1:
            print(
                f"{'Sie hatten ' if keine else f'Sie hatten im {x + 1}. Durchlauf '}{statistik_anzahl_richtige[durchlauf_nummer]} gewusste Vokabeln.")
            print(f"Diese sind: \n")
            if output_type == "1":  # with delimiter
                for key, value in statistik_richtige_woerter_without_description[durchlauf_nummer].items():
                    print(delimiter_vok1, key, delimiter_vok2, value, delimiter_vok1)
                s_r_w_w_d_values = list(statistik_richtige_woerter_without_description[durchlauf_nummer].values())
                s_r_w_w_d_keys = list(statistik_richtige_woerter_without_description[durchlauf_nummer].keys())
                print("s_r_w_w_d_values: ", s_r_w_w_d_values)
                print("s_r_w_w_d_keys: ", s_r_w_w_d_keys)
                print(f"{convert_language(detect_language(s_r_w_w_d_values[0]))}e Wörter: {s_r_w_w_d_values}")
                print(f"{convert_language(detect_language(s_r_w_w_d_keys[0]))}e Wörter: {s_r_w_w_d_keys}")
            if output_type == "2":  # in Dictionary
                print(statistik_richtige_woerter_without_description[durchlauf_nummer])
            if output_type == "3":  # with explanation
                for element in statistik_richtige_woerter[durchlauf_nummer]:
                    print(element, "\n")
        elif statistik_anzahl_richtige[durchlauf_nummer] == 1:
            print(
                f"{'Sie hatten ' if keine else f'Sie hatten im {x + 1}. Durchlauf '}eine gewusste Vokabel.")
            print(f"Diese ist: ")
            if output_type == "1":  # with delimiter
                for key, value in statistik_richtige_woerter_without_description[durchlauf_nummer].items():
                    print(delimiter_vok1, key, delimiter_vok2, value, delimiter_vok1)
                s_r_w_w_d_values = list(statistik_falsche_woerter_without_description[durchlauf_nummer].values())
                s_r_w_w_d_keys = list(statistik_falsche_woerter_without_description[durchlauf_nummer].keys())
                print(f"{convert_language(detect_language(s_r_w_w_d_values[0]))}e Wörter: {s_r_w_w_d_values}")
                print(f"{convert_language(detect_language(s_r_w_w_d_keys[0]))}e Wörter: {s_r_w_w_d_keys}")
            if output_type == "2":  # in Dictionary
                print(statistik_richtige_woerter_without_description[durchlauf_nummer])
            if output_type == "3":  # with explanaition
                for element in statistik_richtige_woerter[durchlauf_nummer]:
                    print(element, "\n")
        else:
            print(
                f"{'Sie hatten ' if keine else f'Sie hatten im {x + 1}. Durchlauf '}keine gewussten Vokabeln.")
        dict_right_ones = {}
        for y in range(0, x, 1):
            dn = f"Durchlauf:_{y}"
            if statistik_anzahl_richtige[dn] > 0:
                for key, value in statistik_richtige_woerter_without_description[dn].items():
                    dict_right_ones[key] = value
        if len(list(dict_right_ones.keys())) > 0:
            print("Außerdem hatten Sie in vorherigen Durchläufen schon folgende ", len(dict_right_ones),
                  " Vokabeln gekonnt:")
            if output_type == "1":  # with delimiter
                for key, value in dict_right_ones[dn].items():
                    print(delimiter_vok1, key, delimiter_vok2, value, delimiter_vok1)
                d_r_o_values = list(dict_right_ones[dn].values())
                d_r_o_keys = list(dict_right_ones[dn].keys())
                print(f"{convert_language(detect_language(d_r_o_values[0]))}e Wörter: {d_r_o_values}")
                print(f"{convert_language(detect_language(d_r_o_keys[0]))}e Wörter: {d_r_o_keys}")
            if output_type == "2":  # im dictionary
                print(dict_right_ones)
            if output_type == "3":  # with explanations
                for key, value in dict_right_ones.items():
                    print(f"-    '{key}', was auf {output_language.lower()} '{vocabulary[key]}' heißt!\n")
    for key, value in vocabulary_statistic.items():
        vokabeln_statistik_copy[key] = value[vocabulary[key]]
    # for i in range(0, groesste_zahl + 1, 1):
    # for key, value in vokabeln_statistik_copy.items(): #TODO: Statt print Anweisungen liste oder dict verwenden
    # if value == i:
    # if output_type == "1":  # Trennzeichen
    # print(f"{delimiter_vok1}{key}{delimiter_vok2}{vocabulary[key]}")
    # elif output_type == "2":  # Dictionary
    # print(f"{key}: ", "{", vocabulary[key], ": ", value, "}")
    # elif output_type == "3":  # Erläuterungen
    # print(f"Sie hatten '{key}', was '{vocabulary[key]}' heißt, {value} mal falsch.")
    dict_wrong_ones_sorted_count_often = {}
    for i in range(0, groesste_zahl + 1, 1):
        i = str(i)
        dict_wrong_ones_sorted_count_often[str(i)] = {}
        for key, value in vokabeln_statistik_copy.items():  # TODO: Statt print Anweisungen liste oder dict verwenden
            if value == i:
                dict_wrong_ones_sorted_count_often[str(i)][key] = value
        if output_type == "1":  # with delimiter TODO: Einfügen, dass dict_wrong_ones_sorted_count_often leer sein kann
            for key, value in dict_wrong_ones_sorted_count_often[str(i)].items():
                print(delimiter_vok1, key, delimiter_vok2, value, delimiter_vok1)
            d_w_o_s_c_o_values = list(dict_wrong_ones_sorted_count_often[str(i)].values())
            d_w_o_s_c_o_keys = list(dict_wrong_ones_sorted_count_often[str(i)].keys())
            if len(d_w_o_s_c_o_values) > 0:
                print("d_w_o_s_c_o_values.index('möglichkeit'): ", d_w_o_s_c_o_values.index('möglichkeit'))
                print("d_w_o_s_c_o_values[1]: ", d_w_o_s_c_o_values[1])
                print("d_w_o_s_c_o_values[0]: ", d_w_o_s_c_o_values[0])
                print(f"{convert_language(detect_language(d_w_o_s_c_o_values[0]))}e Wörter: {d_w_o_s_c_o_values}")
                print(f"{convert_language(detect_language(d_w_o_s_c_o_keys[0]))}e Wörter: {d_w_o_s_c_o_keys}")
        if output_type == "2":  # in Dictionary
            print(dict_wrong_ones_sorted_count_often[str(i)])
        if output_type == "3":  # with explanaition
            for element in statistik_richtige_woerter[durchlauf_nummer]:
                print(element, "\n")
    return ()


def initialize_vocabulary_statistic():
    for key, value in vocabulary_statistic.items():
        vocabulary_statistic[key] = {value: 0}


def save_vocabulary_as_wrong(input_language_word, output_language_word):
    wrong_ones[input_language_word] = output_language_word
    add_wrong_answers_to_csv_file(input_language_word, output_language_word)
    index = output_language_words.index(output_language_word)
    output_language_words.pop(index)
    output_language_words.append(output_language_word)
    vocabulary_statistic[input_language_word] = {
        output_language_word: int(vocabulary_statistic[input_language_word][output_language_word]) + 1}


def save_vocabulary_as_right(input_language_word, output_language_word):
    print("Richtig!\n")
    if input_language_word in wrong_ones:
        del wrong_ones[input_language_word]
    right_ones[input_language_word] = output_language_word
    index = output_language_words.index(output_language_word)
    output_language_words.pop(index)
    # german_words.remove(output_language_word)
    add_right_answers_to_csv_file(input_language_word, output_language_word)


def process_input_if_option_or_solution(word, name_glob_var, i_text):
    globvar = input(i_text).strip().lower()
    if name_glob_var == "selected_option":
        global selected_option
        selected_option = globvar
    elif name_glob_var == "user_solution":
        global user_solution
        user_solution = globvar
    else:
        print("\n\n\n\n\nFehler\n\n\n\n\n")
    falsch = check_if_wrong_answers_print(globvar)
    if falsch:
        process_input_if_option_or_solution(word, name_glob_var, i_text)


def check_acceptance_of_wrong_vocabulary(input_language_word, output_language_word):
    # prüft ob Eingabe ein "?" für nicht gewusst war, oder ob sie falsch war.
    if user_solution != "?":
        compare_each_character(input_language_word)
        process_input_if_option_or_solution(input_language_word, "selected_option",
                                            f"Das war leider falsch. Die richtige Antwort ist: '{input_language_word}'\nMöchten "
                                            "Sie es trotzdem "
                                            "akzeptieren?\n1. Ja\n2. Nein\nGeben Sie '1' oder '2' ein!\nZahl: ")
        if "1" in selected_option:
            save_vocabulary_as_right(input_language_word, output_language_word)
            print("Es wurde erfolgreich akzeptiert.")
        else:
            save_vocabulary_as_wrong(input_language_word, output_language_word)
    else:
        print("Die richtige Antwort ist: '{}'\n".format(input_language_word))
        save_vocabulary_as_wrong(input_language_word, output_language_word)


# def frage(word):
# global user_solution
# user_solution = input(f"Was ist die {fremdsprache.lower()}e Übersetzung für '{word}'?\nAntwort: ").strip().lower()
# falsch = pruefen_print(user_solution)
# if falsch:
#   frage(word)


# Durchgehen der Vokabeln
def compare_each_character(input_language_word):
    i = 0
    y = 0
    if len(user_solution) <= len(input_language_word):
        for buchstabe_1 in user_solution:
            if buchstabe_1 == input_language_word[i]:
                break
            else:
                y += 1
            i += 1
    else:
        print("Sie haben zu viele Buchstaben eingegeben!")
    if y == len(user_solution):
        print("Das ganze Wort ist falsch! Es stimmt kein Buchstabe überein!")
        return
    i = 0
    if len(user_solution) <= len(input_language_word):
        for buchstabe in user_solution:
            if buchstabe != input_language_word[i]:
                print("Sie haben einen Fehler beim {}!".format(buchstabe))
            i += 1
    # else:
    # print("Sie haben zu viele Buchstaben eingegeben")


def test_users_vocabulary():
    global user_solution
    length_german_words = len(output_language_words)
    for i in range(0, length_german_words):
        output_language_word = output_language_words[0]
        print("Sie haben noch verbleibende Vokabeln: ", len(output_language_words))
        process_input_if_option_or_solution(output_language_word, "user_solution",
                                            f"Was ist die {input_language.lower()}e Übersetzung für '{output_language_word}'?\nAntwort: ")
        input_language_word = None
        for key, value in vocabulary.items():
            if value == output_language_word:
                input_language_word = key
                break
        # Check the answer
        if user_solution == input_language_word:
            save_vocabulary_as_right(input_language_word, output_language_word)
        else:
            check_acceptance_of_wrong_vocabulary(input_language_word, output_language_word)
    if len(wrong_ones) != 0:
        print(f"Deine bisher noch nicht gekonnten Vokabeln sind:")
        keys = list(wrong_ones.keys())
        for index in range(0, len(keys), 1):
            if 0 <= index < len(keys):
                print(f"-    {keys[index]}, was {wrong_ones[keys[index]]} heißt!\n")
    user_solution = "------"
    add_wrong_answers_to_csv_file("------", "------")
    add_right_answers_to_csv_file("------", "------")
    if len(output_language_words) != 0:
        test_users_vocabulary()
    else:
        print("Sehr gut, Sie haben es geschafft!")
        boolean = False
        while not boolean:
            type_of_statistic_print = input(
                "Wählen Sie aus, wie die Statistik ausgegeben werden soll!\n1. Zuordnung mit "
                "Trennzeichen\n2. Python Dicctionary\n3. mit Erläuterungen\nEingabe: ")
            if type_of_statistic_print != "1" and type_of_statistic_print != "2" and type_of_statistic_print != "3":
                print(
                    "Sie haben eine ungültige Eingabe getätigt. Sie müssen entweder '1', '2' oder '3' eingeben. Versuchen Sie es erneut!")
                boolean = False
            else:
                boolean = True
        if type_of_statistic_print == "1":
            delimiter_vok1 = input(
                "Geben Sie nun ihr Trennzeichen ein, um Vokabelpakete voneinander zu trennen! Trennzeichen: ")
            delimiter_vok2 = input(
                "Geben Sie nun ihr Trennzeichen ein, um die Vokabeln eines Vokabelpakets voneinander zu trennen! Trennzeichen: ")
        else:
            delimiter_vok1 = None
            delimiter_vok2 = None
        process_and_print_statistic(type_of_statistic_print, delimiter_vok1, delimiter_vok2)


# Globales:
wrong_ones: dict = {}
right_ones: dict = {}
vocabulary: dict = {}
swapped_vocabulary: dict = {}
vocabulary_statistic: dict = copy.deepcopy(vocabulary)
output_language_words: list = list(vocabulary.values())
input_language: str = ""
output_language: str = ""
user_solution: str = ""
selected_option: str = ""
relative_path: str = ""
read_vocabulary: bool = False
translate_spontaneous: bool = False
translation: bool = False
vocabulary_list: list = []
if __name__ == "__main__":
    main()
# TODO INTERESSANT UND LERNEN 8: In objektorientierte Programmierung umwandeln
# TODO BENUTZERFREUNDLICHKEIT 9: grafische Benutzeroberfläche schreiben (z.B. HTML, JavaScript, css)

# TODO gleiche Vokabeln in einer Sprache einlesen können Bsp.: prosperity,Wohlstand + affluence,Wohlstand (anderen
# primär key verwenden)
# TODO Ausgabe verbessern
