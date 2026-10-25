# ==========================================================
# PROJETO FINAL: SISTEMA DE GERENCIAMENTO DE BIBLIOTECA
# ==========================================================


# ==========================================================
# ETAPA 0 - PREPARAR O ARMAZENAMENTO LOCAL
# ==========================================================

# Importa o módulo json para salvar e ler os livros em JSON.
# JSON é um formato usado para armazenar informações
# de maneira estruturada.
import json

# Importa Path para trabalhar com caminhos de arquivos e pastas.
# pathlib é o módulo que reúne ferramentas para trabalhar com caminhos.
# Path é a classe usada para representar esses caminhos.
from pathlib import Path


# No Visual Studio Code, não é necessário conectar o Google Drive.
# Os dados serão salvos em um arquivo JSON no computador.
# __file__ representa o caminho deste arquivo Python.
# resolve() obtém o caminho completo.
# parent identifica a pasta onde o programa está salvo.
PASTA_PROGRAMA = Path(__file__).resolve().parent


# ==========================================================
# ETAPA 1 - VARIÁVEIS GLOBAIS
# ==========================================================

# Lista que armazenará todos os livros cadastrados.
# Cada livro será representado por um dicionário.
# A lista começa vazia e será preenchida com os dados
# do arquivo JSON, caso ele já exista.
livros = []

# Caminho do arquivo onde os livros serão armazenados permanentemente.
# O arquivo ficará na mesma pasta deste programa Python.
# O arquivo será criado automaticamente quando os dados forem salvos.
ARQUIVO_DADOS = PASTA_PROGRAMA / "livros.json"


# ==========================================================
# ETAPA 2 - CARREGAR E SALVAR OS DADOS
# ==========================================================

def carregar_livros():
    """Carrega os livros salvos no arquivo JSON."""

    global livros

    # Se o arquivo ainda não existir, começa com uma lista vazia.
    if not ARQUIVO_DADOS.exists():
        livros = []
        print("Nenhum arquivo de dados encontrado.")
        print("Você poderá cadastrar os primeiros livros.")
        return

    try:
        # Abre o arquivo no modo de leitura.
        # "r" vem de read, que significa ler.
        # encoding="utf-8" permite interpretar textos com acentos.
        with ARQUIVO_DADOS.open("r", encoding="utf-8") as arquivo:

            # Transforma o conteúdo JSON em uma lista Python.
            dados = json.load(arquivo)

        # Confere se os dados carregados são uma lista.
        if not isinstance(dados, list):
            print("Erro: o arquivo não contém uma lista válida.")
            print("Verifique o arquivo livros.json antes de continuar.")
            return

        # Confere se cada livro contém os campos utilizados pelo sistema.
        # Essa verificação evita erros ao listar, pesquisar ou emprestar livros.
        campos_obrigatorios = {
            "titulo",
            "autor",
            "ano",
            "disponivel"
        }

        dados_validos = all(
            isinstance(livro, dict)
            and campos_obrigatorios.issubset(livro.keys())
            and isinstance(livro["titulo"], str)
            and isinstance(livro["autor"], str)
            and isinstance(livro["ano"], int)
            and livro["disponivel"] in ("Sim", "Não")
            for livro in dados
        )

        if not dados_validos:
            print("Erro: um ou mais livros possuem dados inválidos.")
            print("Verifique o arquivo livros.json antes de continuar.")
            return

        # Substitui a lista vazia pelos livros encontrados no arquivo.
        livros = dados

        print(f"{len(livros)} livro(s) carregado(s) do arquivo local.")

    except (json.JSONDecodeError, OSError) as erro:
        # Mostra uma mensagem se não for possível ler o arquivo.
        print(f"Não foi possível carregar os livros: {erro}")
        print("Verifique o arquivo livros.json antes de continuar.")


def salvar_livros():
    """Salva a lista de livros no arquivo JSON."""

    try:
        # Abre o arquivo no modo de escrita.
        # "w" vem de write, que significa escrever.
        # Se o arquivo não existir, será criado.
        # Se existir, seu conteúdo será atualizado.
        with ARQUIVO_DADOS.open("w", encoding="utf-8") as arquivo:

            # Grava a lista em formato JSON.
            # ensure_ascii=False preserva os acentos.
            # indent=4 organiza o arquivo para facilitar a leitura.
            json.dump(
                livros,
                arquivo,
                ensure_ascii=False,
                indent=4
            )

        print("Dados salvos no computador!")

    except OSError as erro:
        print(f"Não foi possível salvar os livros: {erro}")


# except: significa "exceto" e serve para capturar e tratar um erro.
# OSError: tipo de erro relacionado ao sistema operacional,
# como problemas ao acessar arquivos ou diretórios.
# as erro: guarda as informações do erro em uma variável chamada erro.
# {erro}: mostra os detalhes do erro dentro de uma f-string.


# ==========================================================
# ETAPA 3 - CADASTRAR LIVROS
# ==========================================================

def cadastrar_livro():
    """Solicita os dados e cadastra um novo livro."""

    print("\n--- CADASTRO DE LIVRO ---")

    # input permite que a pessoa informe os dados.
    # strip() remove espaços em branco do início e do final do texto.
    titulo = input("Digite o título do livro: ").strip()
    autor = input("Digite o nome do autor: ").strip()
    ano_texto = input("Digite o ano de publicação: ").strip()

    # Impede o cadastro sem título ou autor.
    if not titulo or not autor:
        print("Erro: o título e o autor são obrigatórios.")
        return

    # Verifica se o ano foi informado como número inteiro.
    try:
        ano = int(ano_texto)

    except ValueError:
        print("Erro: o ano deve ser um número inteiro.")
        return

    if ano <= 0:
        print("Erro: digite um ano válido.")
        return

    # Cada livro é um dicionário com quatro informações.
    novo_livro = {
        "titulo": titulo,
        "autor": autor,
        "ano": ano,
        "disponivel": "Sim"
    }

    # Adiciona o dicionário à lista global de livros.
    livros.append(novo_livro)

    # Salva a alteração no arquivo JSON local.
    salvar_livros()

    print(f'Livro "{titulo}" cadastrado com sucesso!')


# if: significa "se". Permite verificar uma condição.
# not: inverte o valor lógico; nesse contexto, indica que o texto está vazio.
# or: significa "ou". Basta uma das condições ser verdadeira para entrar no bloco.
# return: encerra a execução da função naquele momento.


# ==========================================================
# ETAPA 4 - LISTAR TODOS OS LIVROS
# ==========================================================

def listar_livros():
    """Exibe todos os livros cadastrados."""

    print("\n--- LISTA DE LIVROS ---")

    # Se a lista estiver vazia, não há livros para exibir.
    if not livros:
        print("Nenhum livro cadastrado.")
        return

    # Percorre a lista e mostra as informações de cada livro.
    # enumerate() permite numerar os livros a partir de 1.
    for numero, livro in enumerate(livros, start=1):
        print(f"\nLivro {numero}")
        print(f"Título: {livro['titulo']}")
        print(f"Autor: {livro['autor']}")
        print(f"Ano: {livro['ano']}")
        print(f"Disponível: {livro['disponivel']}")


# ==========================================================
# ETAPA 5 - PESQUISAR LIVROS
# ==========================================================

def pesquisar_livros():
    """Pesquisa livros pelo título ou pelo autor."""

    print("\n--- PESQUISAR LIVROS ---")
    print("1 - Pesquisar por título")
    print("2 - Pesquisar por autor")

    opcao = input("Escolha uma opção: ").strip()

    if opcao == "1":
        campo = "titulo"
        termo = input("Digite o título ou parte dele: ").strip()

    elif opcao == "2":
        campo = "autor"
        termo = input("Digite o nome do autor ou parte dele: ").strip()

    else:
        print("Opção inválida.")
        return

    if not termo:
        print("Digite um termo para realizar a pesquisa.")
        return

    # Cria uma lista com os livros que correspondem à pesquisa.
    # casefold() permite comparar sem diferenciar maiúsculas e minúsculas.
    resultados = [
        livro for livro in livros
        if termo.casefold() in livro[campo].casefold()
    ]

    if not resultados:
        print("Nenhum livro encontrado.")
        return

    print(f"\nForam encontrados {len(resultados)} livro(s):")

    for livro in resultados:
        print(f"\nTítulo: {livro['titulo']}")
        print(f"Autor: {livro['autor']}")
        print(f"Ano: {livro['ano']}")
        print(f"Disponível: {livro['disponivel']}")


# ==========================================================
# ETAPA 6 - LOCALIZAR UM LIVRO PARA EMPRESTAR, DEVOLVER
# OU REMOVER
# ==========================================================

def selecionar_livro():
    """Localiza um livro pelo título e permite selecioná-lo."""

    if not livros:
        print("Não existem livros cadastrados.")
        return None

    termo = input("Digite o título ou parte do título: ").strip()

    if not termo:
        print("O título não pode ficar vazio.")
        return None

    # Busca os livros cujos títulos contêm o texto informado.
    resultados = [
        livro for livro in livros
        if termo.casefold() in livro["titulo"].casefold()
    ]

    if not resultados:
        print("Nenhum livro encontrado.")
        return None

    # Mostra os resultados numerados.
    print("\nLivros encontrados:")

    for numero, livro in enumerate(resultados, start=1):
        print(
            f"{numero} - {livro['titulo']} "
            f"({livro['autor']}) - "
            f"Disponível: {livro['disponivel']}"
        )

    # Solicita que a pessoa escolha um dos resultados.
    escolha = input("Digite o número do livro desejado: ").strip()

    try:
        indice = int(escolha) - 1

    except ValueError:
        print("Digite um número válido.")
        return None

    # Confere se o número corresponde a um resultado existente.
    if indice < 0 or indice >= len(resultados):
        print("Número fora da lista.")
        return None

    # Retorna o dicionário do livro selecionado.
    return resultados[indice]


# ==========================================================
# ETAPA 7 - EMPRESTAR LIVROS
# ==========================================================

def emprestar_livro():
    """Registra o empréstimo de um livro disponível."""

    print("\n--- EMPRESTAR LIVRO ---")

    livro = selecionar_livro()

    # Se a seleção falhou, não há nada para emprestar.
    if livro is None:
        return

    # Só permite empréstimo se o livro estiver disponível.
    if livro["disponivel"] == "Sim":

        livro["disponivel"] = "Não"

        # Salva o novo estado no arquivo local.
        salvar_livros()

        print(f'Livro "{livro["titulo"]}" emprestado com sucesso!')

    else:
        print("Este livro já está emprestado.")


# ==========================================================
# ETAPA 8 - DEVOLVER LIVROS
# ==========================================================

def devolver_livro():
    """Registra a devolução de um livro emprestado."""

    print("\n--- DEVOLVER LIVRO ---")

    livro = selecionar_livro()

    if livro is None:
        return

    # Só permite devolução se o livro estiver emprestado.
    if livro["disponivel"] == "Não":

        livro["disponivel"] = "Sim"

        # Salva a alteração no arquivo JSON local.
        salvar_livros()

        print(f'Livro "{livro["titulo"]}" devolvido com sucesso!')

    else:
        print("Este livro já está disponível na biblioteca.")


# ==========================================================
# ETAPA 9 - FUNCIONALIDADE EXTRA: ESTATÍSTICAS
# ==========================================================

def mostrar_estatisticas():
    """Mostra a quantidade total, disponível e emprestada."""

    total = len(livros)

    # Conta quantos livros estão disponíveis.
    disponiveis = sum(
        1 for livro in livros
        if livro["disponivel"] == "Sim"
    )

    # Calcula quantos livros estão emprestados.
    emprestados = total - disponiveis

    print("\n--- ESTATÍSTICAS DA BIBLIOTECA ---")
    print(f"Total de livros: {total}")
    print(f"Livros disponíveis: {disponiveis}")
    print(f"Livros emprestados: {emprestados}")


# ==========================================================
# ETAPA 10 - FUNCIONALIDADE EXTRA: ORDENAR LIVROS
# ==========================================================

def ordenar_livros():
    """Organiza os livros por título ou ano."""

    if not livros:
        print("Não existem livros para ordenar.")
        return

    print("\n--- ORDENAR LIVROS ---")
    print("1 - Ordenar por título")
    print("2 - Ordenar por ano de publicação")

    opcao = input("Escolha uma opção: ").strip()

    if opcao == "1":

        # Ordena alfabeticamente pelo título.
        livros.sort(key=lambda livro: livro["titulo"].casefold())

        print("Livros ordenados por título.")

    elif opcao == "2":

        # Ordena pelo ano de publicação.
        livros.sort(key=lambda livro: livro["ano"])

        print("Livros ordenados por ano de publicação.")

    else:
        print("Opção inválida.")
        return

    # Salva a ordem atual dos livros no arquivo local.
    salvar_livros()

    listar_livros()


# ==========================================================
# ETAPA 11 - FUNCIONALIDADE EXTRA: REMOVER LIVRO
# ==========================================================

def remover_livro():
    """Remove um livro que não esteja emprestado."""

    print("\n--- REMOVER LIVRO ---")

    livro = selecionar_livro()

    if livro is None:
        return

    # Evita remover um livro que ainda está emprestado.
    if livro["disponivel"] == "Não":
        print("Não é possível remover um livro emprestado.")
        return

    confirmacao = input(
        f'Deseja remover "{livro["titulo"]}"? (s/n): '
    ).strip().lower()

    if confirmacao == "s":

        # Remove o dicionário correspondente da lista.
        livros.remove(livro)

        # Salva a lista atualizada no arquivo local.
        salvar_livros()

        print("Livro removido com sucesso.")

    else:
        print("Remoção cancelada.")


# ==========================================================
# ETAPA 12 - MENU PRINCIPAL
# ==========================================================

def mostrar_menu():
    """Exibe as opções disponíveis no sistema."""

    print("\n===================================")
    print("   SISTEMA DE BIBLIOTECA")
    print("===================================")
    print("1 - Cadastrar livro")
    print("2 - Listar livros")
    print("3 - Pesquisar livros")
    print("4 - Emprestar livro")
    print("5 - Devolver livro")
    print("6 - Mostrar estatísticas")
    print("7 - Ordenar livros")
    print("8 - Remover livro")
    print("9 - Sair")


def main():
    """Controla o funcionamento principal do programa."""

    # Carrega os dados do arquivo JSON local antes de mostrar o menu.
    carregar_livros()

    # O laço mantém o menu em funcionamento até a opção de saída.
    while True:

        mostrar_menu()

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            cadastrar_livro()

        elif opcao == "2":
            listar_livros()

        elif opcao == "3":
            pesquisar_livros()

        elif opcao == "4":
            emprestar_livro()

        elif opcao == "5":
            devolver_livro()

        elif opcao == "6":
            mostrar_estatisticas()

        elif opcao == "7":
            ordenar_livros()

        elif opcao == "8":
            remover_livro()

        elif opcao == "9":
            print("Sistema encerrado. Até logo!")
            break

        else:
            print("Opção inválida. Escolha um número de 1 a 9.")


# ==========================================================
# ETAPA 13 - INICIAR O PROGRAMA
# ==========================================================

# Executa a função main() quando este arquivo é executado
# como programa principal no Visual Studio Code.
if __name__ == "__main__":
    main()
    