import os

def checar_arquivo():
    if not os.path.exists("wods.txt"):
        with open("wods.txt", "w") as f:
            pass  # só cria o arquivo vazio

def add():
    print("\n--- Novo WOD ---")
    d = input("Data: ")
    t = input("Tipo: ").upper()
    s = input("Séries: ")
    r = input("Repetições: ")
    m = input("Movimentos (vírgula): ")

    try:
        with open("wods.txt", "a") as f:
            f.write(f"{d};{t};{s};{r};{m}\n")
        print("Salvo!\n")
    except:
        print("Erro ao salvar")

def ver():
    print("\n-- WODs --")
    try:
        with open("wods.txt") as f:
            dados = f.readlines()
    except:
        print("Erro ao abrir o arquivo")
        return

    if not dados:
        print("Não tem nada ainda")
        return

    for l in dados:
        campos = l.strip().split(";")
        print("Data:", campos[0])
        print("Tipo:", campos[1])
        print("Séries:", campos[2])
        print("Repetições:", campos[3])
        print("Movimentos:", campos[4])
        print("------------------")

def edit():
    print("\n--- Editar WOD ---")
    try:
        with open("wods.txt", "r") as arq:
            todos = arq.readlines()
    except:
        print("Erro abrindo o arquivo")
        return

    if not todos:
        print("Nada para editar")
        return

    ver()
    alvo = input("Data do WOD que quer mudar: ")

    novo = ""
    achei = False

    for l in todos:
        c = l.strip().split(";")
        if c[0] == alvo:
            achei = True
            print("1) Tipo\n2) Séries\n3) Repetições\n4) Movimentos")
            esc = input("Qual quer mudar: ")

            if esc == "1":
                c[1] = input("Novo tipo: ").upper()
            elif esc == "2":
                c[2] = input("Nova série: ")
            elif esc == "3":
                c[3] = input("Nova repetição: ")
            elif esc == "4":
                c[4] = input("Novos movimentos:")
            else:
                print("Número inválido")
                return

            novo += ";".join(c) + "\n"
        else:
            novo += l

    try:
        with open("wods.txt", "w") as a:
            a.write(novo)
    except:
        print("Erro ao escrever")
        return

    if achei:
        print("Editado com sucesso")
    else:
        print("Nada encontrado com essa data")

def apagar():
    print("\n--- Apagar WOD ---")
    try:
        with open("wods.txt", "r") as f:
            linhas = f.readlines()
    except:
        print("Erro no arquivo")
        return

    if not linhas:
        print("Não tem nada pra apagar")
        return

    ver()
    data = input("Digite a data pra apagar: ")

    novo = ""
    achou = False

    for l in linhas:
        pedacos = l.strip().split(";")
        if pedacos[0] != data:
            novo += l
        else:
            achou = True

    try:
        with open("wods.txt", "w") as f:
            f.write(novo)
    except:
        print("Erro ao salvar novo arquivo")
        return

    if achou:
        print("Apagado com sucesso")
    else:
        print("Não achei esse WOD")

def filtrar():
    print("\n--- Filtrar WODs ---")
    print("1) Por tipo")
    print("2) Por movimento")
    esc = input("Selecione uma opção: ")

    try:
        with open("wods.txt", "r") as f:
            dados = f.readlines()
    except:
        print("Falha na tentativa de abrir o arquivo")
        return

    if not dados:
        print("Nenhum WOD cadastrado")
        return

    filtro = input("Digite o que deseja buscar: ").upper()
    encontrou = False

    for l in dados:
        c = l.strip().split(";")
        if esc == "1" and filtro in c[1].upper():
            encontrou = True
        elif esc == "2" and filtro in c[4].upper():
            encontrou = True
        else:
            continue

        if encontrou:
            print("\nData:", c[0])
            print("Tipo:", c[1])
            print("Séries:", c[2])
            print("Repetições:", c[3])
            print("Movimentos:", c[4])
            print("------------------")
            encontrou = False

    if not encontrou:
        print("Nenhum resultado foi encontrado com esse filtro.")

def menu():
    checar_arquivo()
    while True:
        print("\n~~ MENU DE WODs CROSSFIT ~~")
        print("1) Adicionar WOD")
        print("2) Visualizar WODs")
        print("3) Editar WOD")
        print("4) Excluir WOD")
        print("5) Filtrar WODs")
        print("0) Sair\n")

        try:
            opcao = int(input("Digite um número: "))
        except:
            print("Digite apenas números!")
            continue

        if opcao == 1:
            add()
        elif opcao == 2:
            ver()
        elif opcao == 3:
            edit()
        elif opcao == 4:
            apagar()
        elif opcao == 5:
            filtrar()
        elif opcao == 0:
            print("Programa encerrado!")
            break
        else:
            print("Opção inválida")

menu()
