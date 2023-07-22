import os
import re
import chardet
import fitz  # PyMuPDF

# Função para detectar a codificação de um arquivo de texto
def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        rawdata = f.read()
        result = chardet.detect(rawdata)
        return result['encoding']

# Função para procurar as strings alvo em um arquivo de texto
def search_string_in_file(file_path, target_strings, encoding):
    with open(file_path, 'r', encoding=encoding, errors='ignore') as file:
        content = file.read()
        matches = [re.findall(target_string, content, re.IGNORECASE) for target_string in target_strings]
        return matches

# Função para procurar as strings alvo em um arquivo PDF
def search_in_pdf(file_path, target_strings):
    matches = []
    doc = fitz.open(file_path)  # Abre o arquivo PDF usando a biblioteca PyMuPDF
    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)  # Carrega a página atual
        text = page.get_text()  # Extrai o texto da página
        matches += [re.findall(target_string, text, re.IGNORECASE) for target_string in target_strings]
    doc.close()
    return matches

if __name__ == "__main__":
    #coloque a lista de strings aqui!
    target_strings = [r"Coloque", r"aqui", r"a lista de", r"strings que deseja", r"procurar!"]

    # Diretório contendo os arquivos para busca
    search_directory = "DIRECTORY HERE"

    found_matches = False  # Variável para indicar se alguma correspondência foi encontrada

    # Loop para percorrer todos os arquivos no diretório de busca
    for filename in os.listdir(search_directory):
        file_path = os.path.join(search_directory, filename)

        # Verifica se o arquivo é um PDF ou outro tipo de arquivo
        if filename.lower().endswith(".pdf"):
            matches = search_in_pdf(file_path, target_strings)  # Procura as strings alvo no PDF
        else:
            encoding = detect_encoding(file_path)  # Detecta a codificação do arquivo
            matches = search_string_in_file(file_path, target_strings, encoding)  # Procura as strings alvo em outros tipos de arquivo

        # Achatando a lista de correspondências
        flat_matches = [item for sublist in matches for item in sublist]

        # Se alguma correspondência for encontrada, imprime as palavras encontradas no arquivo
        if flat_matches:
            found_matches = True  # Indica que foram encontradas correspondências em pelo menos um arquivo
            print("##################################################")
            print(f"Palavras encontradas no arquivo '{filename}':")
            print("##################################################")
            for match in flat_matches:
                print(match)

    # Se nenhuma correspondência for encontrada em nenhum arquivo, imprime uma mensagem informando isso
    if not found_matches:
        print("#########################################################")
        print("Nenhuma palavra encontrada em nenhum arquivo analisado.")
        print("#########################################################")
