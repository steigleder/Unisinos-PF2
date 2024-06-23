#-----Script utilizado para Análise de Conteúdos
#-----
#-----Utilização:
#-----1.utilizar arquivo CSV contendo notícias para análise
#-----2.o arquivo deve possuir 3 colunas: title; description; date;

import pandas as pd
import re
import chardet

# -----Detectar encoding do csv
with open("data1.csv", 'rb') as f:
    result = chardet.detect(f.read())

encoding = result['encoding']
print(f"Detectado encoding: {encoding}")

# ------Função para limpar e validar linhas
def clean_csv(file_path, encoding, delimiter=";"):
    with open(file_path, 'r', encoding=encoding) as f:
        lines = f.readlines()

    total_lines = 0
    valid_lines = 0
    invalid_lines = 0
    cleaned_lines = []

    for line in lines:
        total_lines += 1
        if line.count(delimiter) == 3:
            cleaned_lines.append(line)
            valid_lines += 1
        else:
            invalid_lines += 1

    cleaned_content = "".join(cleaned_lines)

    # ------Gera novo arquivo limpo
    with open("cleaned_data1.csv", 'w', encoding=encoding) as f:
        f.write(cleaned_content)

    return total_lines, valid_lines, invalid_lines

# mostra a quantidade de linhas válidas que encontrou
total_lines, valid_lines, invalid_lines = clean_csv("data1.csv", encoding)

print(f"Total de linhas analisadas: {total_lines}")
print(f"Total de linhas válidas: {valid_lines}")
print(f"Total de linhas inválidas: {invalid_lines}")

# Leitura do arquivo CSV limpo
data = pd.read_csv("cleaned_data1.csv", delimiter=";")

contagem_title = {}
contagem_description = {}

#------definição das duas categorias para a análise de conteúdo: evento e impacto
#------definição das palavas-chave que são consideradas por categoria
categorias = {
    "incidente": ["ameaça", "ataque", "ataque cibernético", "ciber ameaça", "ciber ataque", "ciber fraude", "código", "malicioso", "coleta de informações", "conteúdo abusivo", "crimeware", "engenharia social", "espionagem", "hacker", "hacking", "incidente", "infosec", "intrusão", "invasão", "keylogger", "malware", "negação de serviço", "phishing", "ransomware", "roubo de dados", "violação de dados", "vírus", "vulnerabilidade"],
    "impacto": ["acesso não autorizado", "fora do ar", "confidencialidade", "corrupção", "criptografia", "dados confidenciais", "disponibilidade", "falha", "impacto", "indisponibilidade", "indisponível", "integridade", "interrompe", "interrompida", "interrompido", "interrupção", "mitiga", "paralisa", "paralisou", "perda", "perde", "prejuízo", "repara", "reparou", "resgata", "resgate", "restabelece", "restabelecimento", "restaura", "vazados", "vazamento", "vazar"],
}

for index, row in data.iterrows():
    #------pré-processamento do título e descrição
    title = row['title'].lower()
    description = row['description'].lower()

    #------ processamento do título
    for cat, keywords in categorias.items():
        for keyword in keywords:
            # Utilizando expressões regulares para encontrar a palavra-chave no texto, sem restringir a palavras inteiras
            if re.search(keyword, title):
                contagem_title.setdefault(cat, 0)
                contagem_title[cat] += 1

    # ----- processamento da descrição
    for cat, keywords in categorias.items():
        for keyword in keywords:
            if re.search(keyword, description):
                contagem_description.setdefault(cat, 0)
                contagem_description[cat] += 1

# ------apresentação dos resultados
print("\nContagem de ocorrências por categoria no TÍTULO das notícias:")
for cat, freq in contagem_title.items():
    print(f"{cat}: {freq}")

print("\nContagem de ocorrências por categoria na DESCRIÇÃO das notícias:")
for cat, freq in contagem_description.items():
    print(f"{cat}: {freq}")
