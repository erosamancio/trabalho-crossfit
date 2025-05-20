import os 
os.system("cls")
import random

# menu principal
def menu():
    # garante que os arquivos necessários existem
    checar_arquivo_wods()
    checar_arquivo_metas()
    while True:
        print("\n~~~ MENU DE WODs CROSSFIT ~~~")
        print("1) Adicionar WOD")
        print("2) Visualizar WODs")
        print("3) Editar WOD")
        print("4) Excluir WOD")
        print("5) Filtrar WODs")
        print("6) Adicionar Meta")
        print("7) Ver Metas")
        print("8) Editar Meta")
        print("9) Apagar Meta")
        print("10) Sugestão Aleatória de WOD")
        print("11) Conquistas")
        print("0) Sair\n")
        try:
            opcao = int(input("Digite um número: "))
        except:
            print("Digite apenas números!")
            continue
        # chame a função correspondente a opção selecionada
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
        elif opcao == 6:
            add_meta()
        elif opcao == 7:
            ver_metas()
        elif opcao == 8:
            edit_meta()
        elif opcao == 9:
            apagar_meta()
        elif opcao == 10:
            sugerir_wod()
        elif opcao == 11:
            conquistas()
        elif opcao == 0:
            print("Programa encerrado!")
            break
        else:
            print("Opção inválida")

# mista de WODs pré-definidos para sugestões rápidas
WODS_PRE_DEFINIDOS = [
    {
        "Tipo": "AMRAP",
        "Séries": "5",
        "Repetições": "máximo de rounds",
        "Movimentos": "5 Pull-ups, 10 Push-ups, 15 Air Squats",
        "Tempo": "20"
    },
    {
        "Tipo": "EMOM",
        "Séries": "4",
        "Repetições": "cada minuto",
        "Movimentos": "10 Burpees",
        "Tempo": "10"
    },
    {
        "Tipo": "FOR TIME",
        "Séries": "3",
        "Repetições": "21-15-9",
        "Movimentos": "Thrusters, Pull-ups",
        "Tempo": "6"
    }
]

# garante que o arquivo dos WODs existe
def checar_arquivo_wods():
    if not os.path.exists("wods.txt"):
        with open("wods.txt", "w"):
            pass

# garante que o arquivo das metas existe
def checar_arquivo_metas():
    if not os.path.exists("metas.txt"):
        with open("metas.txt", "w"):
            pass

# remove espaços, acentos e deixe em minúsculo
def normaliza_string(s):
    return s.strip().lower().replace("-", " ").replace("_", " ")

# verifica se todos os movimentos estão no WOD
def movimentos_contidos(alvo, movimentos):
    alvo_set = set([normaliza_string(x) for x in alvo.split(",")])
    movimentos_set = set([normaliza_string(x) for x in movimentos.split(",")])
    return alvo_set.issubset(movimentos_set)

# converte datas para padrão dia/mes/ano
def formatar_data(data):
    partes = data.replace("-", "/").replace(".", "/").split("/")
    if len(partes) == 3:
        if len(partes[0]) == 4:  # AAAA/MM/DD
            return f"{partes[2]}/{partes[1]}/{partes[0]}"
        else:  # DD/MM/AAAA
            return f"{partes[0]}/{partes[1]}/{partes[2]}"
    return data

# atualiza metas automaticamente ao registrar WOD, verificando se foram atingidas
def checar_wod_para_metas(wod_tipo, wod_movimentos, wod_tempo, wod_reps, wod_data):
    checar_arquivo_metas()
    try:
        with open("metas.txt", "r") as f:
            linhas = f.readlines()
    except:
        print("Erro ao ler metas.")
        return
    novas_linhas = []
    for l in linhas:
        partes = l.strip().split(";")
        if len(partes) < 9:
            novas_linhas.append(l)
            continue
        data_cad, desc, tipo, alvo, valor_alvo, unidade, prazo, progresso, status = partes
        if status != "ABERTA":
            novas_linhas.append(l)
            continue
        alvo_norm = normaliza_string(alvo)
        wod_tipo_norm = normaliza_string(wod_tipo)
        wod_mov_norm = normaliza_string(wod_movimentos)
        meta_atingida = False

        # caso especial para benchmark Fran
        if alvo_norm == "fran":
            if wod_tipo_norm == "for time" and "thrusters" in wod_mov_norm and "pull-ups" in wod_mov_norm:
                try:
                    wod_tempo_num = float(wod_tempo)
                    valor_alvo_num = float(valor_alvo)
                    if wod_tempo_num <= valor_alvo_num:
                        status = "CONCLUÍDA"
                        progresso = "%s min (atingido em %s)" % (wod_tempo, formatar_data(wod_data))
                        meta_atingida = True
                    else:
                        progresso = "%s min (melhor até agora)" % wod_tempo
                except:
                    progresso = progresso
        # verifica por qualquer outro movimento/meta
        elif alvo_norm in wod_mov_norm or movimentos_contidos(alvo, wod_movimentos):
            if tipo == "tempo" and unidade == "min":
                try:
                    wod_tempo_num = float(wod_tempo)
                    valor_alvo_num = float(valor_alvo)
                    if wod_tempo_num <= valor_alvo_num:
                        status = "CONCLUÍDA"
                        progresso = "%s min (atingido em %s)" % (wod_tempo, formatar_data(wod_data))
                        meta_atingida = True
                    else:
                        progresso = "%s min (melhor até agora)" % wod_tempo
                except:
                    progresso = progresso
            elif tipo == "rep":
                try:
                    wod_reps_num = int(wod_reps)
                    valor_alvo_num = int(valor_alvo)
                    if wod_reps_num >= valor_alvo_num:
                        status = "CONCLUÍDA"
                        progresso = "%s rep (atingido em %s)" % (wod_reps, formatar_data(wod_data))
                        meta_atingida = True
                    else:
                        progresso = "%s rep (melhor até agora)" % wod_reps
                except:
                    progresso = progresso
            elif tipo == "weight":
                try:
                    wod_reps_num = float(wod_reps)
                    valor_alvo_num = float(valor_alvo)
                    if wod_reps_num >= valor_alvo_num:
                        status = "CONCLUÍDA"
                        progresso = "%s kg (atingido em %s)" % (wod_reps, formatar_data(wod_data))
                        meta_atingida = True
                    else:
                        progresso = "%s kg (melhor até agora)" % wod_reps
                except:
                    progresso = progresso
        nova = ";".join([data_cad, desc, tipo, alvo, str(valor_alvo), unidade, prazo, progresso, status]) + "\n"
        novas_linhas.append(nova)
        if meta_atingida:
            print("Parabéns! Você atingiu a meta: '%s'" % desc)
    with open("metas.txt", "w") as f:
        f.writelines(novas_linhas)

# adicionar um novo WOD
def add():
    checar_arquivo_wods()
    print("\n--- Novo WOD ---")
    d = input("Data (dia/mes/ano): ")
    t = input("Tipo (AMRAP, EMOM, FOR TIME): ").upper()
    s = input("Séries: ")
    r = input("Repetições (ou peso, se aplicável): ")
    m = input("Movimentos (vírgula): ")
    tempo = input("Tempo (em minutos): ")
    try:
        tempo_int = float(tempo)
    except:
        print("Tempo deve ser um número (minutos).")
        return
    try:
        with open("wods.txt", "a") as f:
            f.write("%s;%s;%s;%s;%s;%s\n" % (formatar_data(d), t, s, r, m, tempo_int))
        print("Salvo!\n")
    except:
        print("Erro ao salvar.")
    checar_wod_para_metas(t, m, tempo, r, d)

# Visualize todos os WODs cadastrados
def ver():
    checar_arquivo_wods()
    print("\n-- WODs --")
    try:
        with open("wods.txt") as f:
            dados = f.readlines()
    except:
        print("Erro abrindo o arquivo")
        return
    if not dados:
        print("Não tem nada ainda")
        return
    for l in dados:
        campos = l.strip().split(";")
        if len(campos) < 6:
            continue
        print("Data:", campos[0])
        print("Tipo:", campos[1])
        print("Séries:", campos[2])
        print("Repetições/Peso:", campos[3])
        print("Movimentos:", campos[4])
        print("Tempo: %s minutos" % campos[5])
        print("------------------")

# permite editar um WOD selecionando o campo desejado
def edit():
    checar_arquivo_wods()
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
    alvo = input("Data do WOD que quer mudar (dia/mes/ano): ")
    novo = ""
    achei = False
    for l in todos:
        c = l.strip().split(";")
        if c[0] == formatar_data(alvo):
            achei = True
            print("1) Tipo\n2) Séries\n3) Repetições/Peso\n4) Movimentos\n5) Tempo")
            esc = input("Qual quer mudar: ")
            if esc == "1":
                c[1] = input("Novo tipo: ").upper()
            elif esc == "2":
                c[2] = input("Nova série: ")
            elif esc == "3":
                c[3] = input("Nova repetição/peso: ")
            elif esc == "4":
                c[4] = input("Novos movimentos: ")
            elif esc == "5":
                c[5] = input("Novo tempo (em minutos): ")
            else:
                print("Número errado")
                return
            linha_nova = ";".join(c) + "\n"
            novo += linha_nova
        else:
            novo += l
    try:
        with open("wods.txt", "w") as a:
            a.write(novo)
        if achei:
            print("Editado com sucesso")
        else:
            print("Nada encontrado com essa data")
    except:
        print("Erro ao escrever")
        return

# apague um WOD a partir da data
def apagar():
    checar_arquivo_wods()
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
    data = input("Digite a data pra apagar (dia/mes/ano): ")
    novo = ""
    achou = False
    for l in linhas:
        pedacos = l.strip().split(";")
        if pedacos[0] != formatar_data(data):
            novo += l
        else:
            achou = True
    try:
        with open("wods.txt", "w") as f:
            f.write(novo)
        if achou:
            print("Apagado com sucesso")
        else:
            print("Não achei esse WOD")
    except:
        print("Erro ao salvar novo arquivo")
        return

# permite filtrar WODs por tipo ou movimento
def filtrar():
    checar_arquivo_wods()
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
    encontrou_algum = False
    for linha in dados:
        linha = linha.strip()
        campos = linha.split(";")
        if len(campos) < 6:
            continue
        tipo = campos[1].upper()
        movimentos = campos[4].upper()
        if (esc == "1" and filtro in tipo) or (esc == "2" and filtro in movimentos):
            print("\nData:", campos[0])
            print("Tipo:", campos[1])
            print("Séries:", campos[2])
            print("Repetições/Peso:", campos[3])
            print("Movimentos:", campos[4])
            print("Tempo: %s minutos" % campos[5])
            print("------------------")
            encontrou_algum = True
    if not encontrou_algum:
        print("Nenhum resultado foi encontrado com esse filtro.")

# adicione uma nova meta de desempenho
def add_meta():
    checar_arquivo_metas()
    print("\n--- Nova Meta de Desempenho ---")
    desc = input("Descrição da meta (ex: Baixar tempo Fran para 6min): ")
    tipo = input("Tipo de meta (tempo/rep/weight): ").lower()
    alvo = input("Movimento ou WOD alvo (ex: Fran, Pull-up): ").strip().upper()
    valor_alvo = input("Valor alvo (ex: 6, 50, 100): ")
    unidade = input("Unidade (min, rep, kg): ").lower()
    prazo = input("Prazo final (dia/mes/ano): ")
    status = "ABERTA"
    progresso = ""
    data_cadastro = input("Data de cadastro (dia/mes/ano): ")
    linha = f"{formatar_data(data_cadastro)};{desc};{tipo};{alvo};{valor_alvo};{unidade};{formatar_data(prazo)};{progresso};{status}\n"
    try:
        with open("metas.txt", "a") as f:
            f.write(linha)
        print("Meta salva!\n")
    except:
        print("Erro ao salvar a meta")

# visualize todas as metas cadastradas e seus progressos
def ver_metas():
    checar_arquivo_metas()
    print("\n-- METAS DE DESEMPENHO --")
    try:
        with open("metas.txt") as f:
            linhas = f.readlines()
    except:
        print("Erro abrindo o arquivo de metas")
        return
    if not linhas:
        print("Nenhuma meta cadastrada")
        return
    for l in linhas:
        partes = l.strip().split(";")
        if len(partes) < 9:
            continue
        print(f"Data de Cadastro: {partes[0]}")
        print(f"Descrição: {partes[1]}")
        print(f"Tipo: {partes[2]}")
        print(f"Movimento/WOD alvo: {partes[3]}")
        print(f"Valor alvo: {partes[4]} {partes[5]}")
        print(f"Prazo final: {partes[6]}")
        print(f"Progresso: {partes[7]}")
        print(f"Status: {partes[8]}")
        print("------------------")

# permite editar uma meta manualmente, inclusive progresso
def edit_meta():
    checar_arquivo_metas()
    print("\n--- Editar Meta ---")
    try:
        with open("metas.txt", "r") as f:
            todas = f.readlines()
    except:
        print("Erro ao abrir o arquivo")
        return
    if not todas:
        print("Nenhuma meta para editar")
        return
    ver_metas()
    data_alvo = input("Data de cadastro da meta que quer editar (dia/mes/ano): ")
    desc_alvo = input("Descrição da meta que quer editar: ")
    novo = ""
    achei = False
    for l in todas:
        c = l.strip().split(";")
        if len(c) < 9:
            novo += l
            continue
        if c[0] == formatar_data(data_alvo) and c[1].strip().lower() == desc_alvo.strip().lower():
            achei = True
            print("1) Descrição\n2) Tipo\n3) Movimento/WOD alvo\n4) Valor alvo\n5) Unidade\n6) Prazo\n7) Progresso\n8) Status")
            escolha = input("Qual campo deseja editar: ")
            if escolha == "1":
                c[1] = input("Nova descrição: ")
            elif escolha == "2":
                c[2] = input("Novo tipo: ")
            elif escolha == "3":
                c[3] = input("Novo movimento/WOD alvo: ").upper()
            elif escolha == "4":
                c[4] = input("Novo valor alvo: ")
            elif escolha == "5":
                c[5] = input("Nova unidade: ")
            elif escolha == "6":
                c[6] = formatar_data(input("Novo prazo final (dia/mes/ano): "))
            elif escolha == "7":
                c[7] = input("Novo progresso: ")
            elif escolha == "8":
                c[8] = input("Novo status (ABERTA/CONCLUÍDA/ATRASADA): ").upper()
            else:
                print("Opção inválida")
                return
            nova_linha = ";".join(c) + "\n"
            novo += nova_linha
        else:
            novo += l
    try:
        with open("metas.txt", "w") as f:
            f.write(novo)
        if achei:
            print("Meta editada com sucesso")
        else:
            print("Nenhuma meta encontrada com essa data e descrição")
    except:
        print("Erro ao salvar a meta editada")

# apague uma meta pelo data e descrição
def apagar_meta():
    checar_arquivo_metas()
    print("\n--- Apagar Meta ---")
    try:
        with open("metas.txt", "r") as f:
            linhas = f.readlines()
    except:
        print("Erro ao abrir o arquivo")
        return
    if not linhas:
        print("Não tem nada pra apagar")
        return
    ver_metas()
    data_alvo = input("Data de cadastro da meta para apagar (dia/mes/ano): ")
    desc_alvo = input("Descrição da meta para apagar: ")
    novo = ""
    achou = False
    for l in linhas:
        partes = l.strip().split(";")
        if len(partes) < 9:
            novo += l
            continue
        if partes[0] == formatar_data(data_alvo) and partes[1].strip().lower() == desc_alvo.strip().lower():
            achou = True
        else:
            novo += l
    try:
        with open("metas.txt", "w") as f:
            f.write(novo)
        if achou:
            print("Apagado com sucesso")
        else:
            print("Não achei essa meta")
    except:
        print("Erro ao salvar novo arquivo de metas")
        return

# sugire um WOD aleatório, usando também os WODs do usuário
def sugerir_wod():
    checar_arquivo_wods()
    print("\n--- Sugestão Aleatória de WOD ---")
    user_wods = []
    try:
        with open("wods.txt", "r") as f:
            linhas = f.readlines()
            for l in linhas:
                campos = l.strip().split(";")
                if len(campos) >= 6:
                    user_wods.append({
                        "Tipo": campos[1],
                        "Séries": campos[2],
                        "Repetições": campos[3],
                        "Movimentos": campos[4],
                        "Tempo": campos[5]
                    })
    except:
        pass
    opcoes = user_wods + WODS_PRE_DEFINIDOS
    if not opcoes:
        print("Nenhum WOD disponível para sugestão.")
        return
    escolhido = random.choice(opcoes)
    print("Aqui vai um WOD aleatório pra você tentar repetir ou se inspirar:\n")
    print("Tipo:", escolhido["Tipo"])
    print("Séries:", escolhido["Séries"])
    print("Repetições:", escolhido["Repetições"])
    print("Movimentos:", escolhido["Movimentos"])
    print("Tempo: %s minutos" % escolhido["Tempo"])

# mostra conquistas baseadas nos WODs cadastrados
def conquistas():
    checar_arquivo_wods()
    print("\n--- Conquistas ---")
    try:
        with open("wods.txt", "r") as f:
            linhas = f.readlines()
    except:
        print("Erro ao acessar os WODs")
        return
    if not linhas:
        print("Nenhum WOD cadastrado ainda.")
        return
    total_wods = len(linhas)
    tipos = set()
    movimentos = []
    contagem_movimentos = {}
    for l in linhas:
        c = l.strip().split(";")
        if len(c) < 6:
            continue
        tipos.add(c[1].strip().upper())
        for m in c[4].split(","):
            mov = m.strip().upper()
            movimentos.append(mov)
            contagem_movimentos[mov] = contagem_movimentos.get(mov, 0) + 1
    print("\nVocê já cadastrou %s WOD(s)" % total_wods)
    if total_wods >= 1:
        print("✅ Primeiro treino registrado!")
    if total_wods >= 10:
        print("🏅 Medalha de Consistência: 10 ou mais WODs registrados!")
    if total_wods >= 20:
        print("🏅🏅 Medalha de Foco: 20 ou mais WODs registrados!")
    tipos_necessarios = {"AMRAP", "EMOM", "FOR TIME"}
    if tipos_necessarios.issubset(tipos):
        print("🧠 Usou todos os tipos de treino! (AMRAP, EMOM e FOR TIME)")
    elif len(tipos) >= 2:
        print("🤸‍♂ Medalha de Versatilidade: 2 ou mais tipos diferentes!")
    if len(set(movimentos)) >= 10:
        print("🤸‍♀🤸‍♀ Medalha de Diversidade: 10 ou mais movimentos diferentes usados!")
    if contagem_movimentos:
        favorito = max(contagem_movimentos, key=contagem_movimentos.get)
        qtd = contagem_movimentos[favorito]
        if qtd >= 5:
            print("⭐ Movimento favorito: %s apareceu %d vezes!" % (favorito, qtd))
    print("\nContinue se desafiando para conquistar mais medalhas 💪")

if __name__ == "__main__":
    menu()
