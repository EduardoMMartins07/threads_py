import threading

# Função que cada thread executará
def process_csv_part(lines, thread_id, target_id, result, lock):
    print(f"Thread {thread_id} iniciou o processamento de {len(lines)} linhas.")
    for line in lines:
        # Divide a linha em colunas usando a vírgula como separador
        columns = line.strip().split(",")
        # Verifica se o ID da linha corresponde ao ID procurado
        if columns[0] == target_id:
            with lock:
                result.append((thread_id, line))  # Armazena o ID da thread e a linha encontrada
            break  # Encerra a busca, pois o ID foi encontrado
    print(f"Thread {thread_id} terminou o processamento.")

# Função principal
def main():
    file_path = "dados.csv"
    num_threads = 7  # Número de threads que você deseja utilizar
    threads = []
    result = []  # Lista para armazenar o resultado da busca
    lock = threading.Lock()  # Lock para sincronizar o acesso à lista de resultados

    # Solicita o ID como entrada do usuário
    target_id = input("Digite o ID que deseja buscar: ")

    # Abre o arquivo e lê todas as linhas
    with open(file_path, mode="r", encoding="utf-8") as file:
        lines = file.readlines()  # Lê todas as linhas do arquivo

    # Remove o cabeçalho (primeira linha) e divide as linhas restantes
    header = lines[0]  # Guarda o cabeçalho
    data_lines = lines[1:]  # Restante das linhas (dados)

    # Divide as linhas do CSV em partes iguais para cada thread
    chunk_size = len(data_lines) // num_threads
    for i in range(num_threads):
        start = i * chunk_size
        end = (i + 1) * chunk_size if i < num_threads - 1 else len(data_lines)
        chunk = data_lines[start:end]

        # Cria e inicia uma nova thread para processar o chunk
        thread = threading.Thread(
            target=process_csv_part, args=(chunk, i, target_id, result, lock)
        )
        threads.append(thread)
        thread.start()

    # Aguarda todas as threads terminarem
    for thread in threads:
        thread.join()

    # Exibe o resultado da busca
    if result:
        thread_id, line = result[0]  # Pega o ID da thread e a linha encontrada
        print(f"Thread {thread_id} encontrou a linha para o ID {target_id}: {line}")
    else:
        print(f"Nenhuma linha encontrada para o ID {target_id}.")

if __name__ == "__main__":
    main()