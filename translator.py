import requests
from bs4 import BeautifulSoup
from sys import argv
from sys import exit


def main():

    languages = ["arabic", "german", "english", "spanish", "french", "hebrew", "japanese", "dutch", "polish",
                 "portuguese", "romanian", "russian", "turkish", "all"]

    if argv[1].lower() not in languages:
        print(f"Sorry, the program doesn't support {argv[1].capitalize()}")
        exit()
    elif argv[2].lower()  not in languages:
        print(f"Sorry, the program doesn't support {argv[2].capitalize()}")
        exit()

    f_language, t_language, word = argv[1].lower(), argv[2].lower(), argv[3].lower()

    if t_language != 'all':
        language_pair = f_language + "-" + t_language
        connect_to_server(word, t_language, language_pair)
    else:
        for lang in languages[: 13]:
            if lang != f_language:
                t_language = lang
                language_pair = f_language + "-" + t_language
                connect_to_server(word, t_language, language_pair)


def connect_to_server(word, t_language, language_pair):
    url = f'https://context.reverso.net/translation/{language_pair}/{word}'
    headers = {'User-Agent': 'Mozilla/5.0'}
    s = requests.Session()
    website_response = s.get(url, headers=headers)
    if website_response.status_code == 404:
        print(f"Sorry, unable to find {word}")
        exit()
    elif website_response.status_code != 200:
        print('Something wrong with your internet connection')
        exit()

    soup = BeautifulSoup(website_response.content, 'html.parser')
    translations = [i.text.strip() for i in soup.find_all('a', class_='translation')]
    examples_from = [i.text.strip() for i in soup.find_all('div', class_='src ltr')]
    examples_to = [j.text.strip() for j in soup.find_all('div', class_=['trg ltr', 'trg rtl', 'trg rtl arabic'])]

    file_contents = ''
    file_contents += f'{t_language.capitalize()} Translations:\n'
    for i in translations[:]:
        file_contents += i + "\n"
    file_contents += '\n'
    file_contents += f'{t_language.capitalize()} Example:\n'
    for i, j in zip(examples_from[:], examples_to[:]):
        file_contents += i + '\n'
        file_contents += j + '\n'
    file_contents += '\n'
    file_name = f'{word}.txt'
    with open(file_name, 'a', encoding="utf-8") as file:
        file.write(file_contents)
    print(file_contents, end='')


main()

