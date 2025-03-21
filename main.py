import threading

# Função que cada thread executará
def process_csv_part(lines, thread_id, target_plate, result, lock):
    print(f"Thread {thread_id} iniciou o processamento de {len(lines)} linhas.")
    for line in lines:
        columns = line.strip().split(",")
        plate_in_csv = columns[0].replace("-", "")  # Remove o hífen da placa no CSV
        if plate_in_csv == target_plate:  # Compara sem o hífen
            with lock:
                result.append((thread_id, columns))  # Armazena os dados encontrados
            break  # Para a busca na thread
    print(f"Thread {thread_id} terminou o processamento.")

# Função principal
def main():
    file_path = "dados.csv"
    num_threads = 4 
    threads = []
    result = []  
    lock = threading.Lock()  

    # Solicita a placa do carro como entrada do usuário
    target_plate = input("Digite a placa do carro que deseja buscar: ").strip().upper().replace("-", "")

    # Abre o arquivo e lê todas as linhas
    with open(file_path, mode="r", encoding="utf-8") as file:
        lines = file.readlines()  

    # Captura o cabeçalho e as linhas de dados
    header = lines[0].strip().split(",")
    data_lines = lines[1:]  

    # Divide as linhas do CSV em partes iguais para cada thread
    chunk_size = len(data_lines) // num_threads
    for i in range(num_threads):
        start = i * chunk_size
        end = (i + 1) * chunk_size if i < num_threads - 1 else len(data_lines)
        chunk = data_lines[start:end]

        # Cria e inicia uma nova thread para processar o chunk
        thread = threading.Thread(target=process_csv_part, args=(chunk, i, target_plate, result, lock))
        threads.append(thread)
        thread.start()

    # Aguarda todas as threads terminarem
    for thread in threads:
        thread.join()

    # Exibe o resultado da busca formatado manualmente
    if result:
        thread_id, data = result[0]  
        print(f"\n✅ Thread {thread_id} encontrou a placa '{data[0]}':\n")
        
        # Exibir cabeçalho
        print("-" * 80)
        print(f"{header[0]:<10} {header[1]:<10} {header[2]:<10} {header[3]:<6} {header[4]:<15} {header[5]:<20} {header[6]:<5} {header[7]:<5}")
        print("-" * 80)
        
        # Exibir os dados encontrados
        print(f"{data[0]:<10} {data[1]:<10} {data[2]:<10} {data[3]:<6} {data[4]:<15} {data[5]:<20} {data[6]:<5} {data[7]:<5}")
        print("-" * 80)
    else:
        print(f"\n❌ Nenhuma linha encontrada para a placa '{target_plate}'.")

if __name__ == "__main__":
    main()
