**Explicação linha a linha do código**

### **Importação de Bibliotecas**
```python
import threading
```
O código utiliza a biblioteca `threading` para realizar a busca em um arquivo CSV de forma simultânea usando múltiplas threads, tornando a execução mais eficiente.

---
### **Função process_csv_part**
Esta função será executada por cada thread para buscar a placa no conjunto de linhas atribuídas a ela.

```python
def process_csv_part(lines, thread_id, target_plate, result, lock):
```
Define a função que recebe:
- `lines`: uma lista com as linhas do CSV atribuídas à thread.
- `thread_id`: o identificador da thread.
- `target_plate`: a placa que o usuário deseja buscar.
- `result`: uma lista compartilhada para armazenar o resultado encontrado.
- `lock`: um mecanismo para evitar conflitos de acesso simultâneo ao `result`.

```python
    print(f"Thread {thread_id} iniciou o processamento de {len(lines)} linhas.")
```
Exibe uma mensagem indicando quantas linhas a thread irá processar.

```python
    for line in lines:
        columns = line.strip().split(",")
```
Itera sobre as linhas recebidas, removendo espaços extras com `strip()` e separando os dados em colunas usando `split(",")`.

```python
        plate_in_csv = columns[0].replace("-", "")  # Remove o hífen da placa no CSV
```
Remove o hífen da placa armazenada no CSV para permitir a comparação com a entrada do usuário.

```python
        if plate_in_csv == target_plate:
```
Verifica se a placa (sem hífen) corresponde à buscada.

```python
            with lock:
                result.append((thread_id, columns))  # Armazena os dados encontrados
```
Se encontrada, a informação é adicionada à lista `result`, garantindo que o acesso seja seguro usando `lock`.

```python
            break  # Para a busca na thread
```
Uma vez que a placa foi encontrada, a busca pode ser interrompida para economizar recursos.

```python
    print(f"Thread {thread_id} terminou o processamento.")
```
Exibe uma mensagem quando a thread finaliza sua busca.

---
### **Função principal: main**
Esta é a função que inicia a execução do programa.

```python
def main():
```
Define a função principal do programa.

```python
    file_path = "dados.csv"
    num_threads = 7  
    threads = []
    result = []  
    lock = threading.Lock()  
```
Define:
- `file_path`: caminho do arquivo CSV.
- `num_threads`: número de threads a serem usadas.
- `threads`: lista para armazenar as threads criadas.
- `result`: lista compartilhada onde serão armazenados os resultados encontrados.
- `lock`: controle de acesso à lista `result`.

```python
    target_plate = input("Digite a placa do carro que deseja buscar: ").strip().upper().replace("-", "")
```
Solicita a placa ao usuário e a padroniza:
- `strip()` remove espaços extras.
- `upper()` coloca tudo em maiúsculas.
- `replace("-", "")` remove o hífen para padronizar.

```python
    with open(file_path, mode="r", encoding="utf-8") as file:
        lines = file.readlines()
```
Abre o arquivo CSV e lê todas as linhas.

```python
    header = lines[0].strip().split(",")
    data_lines = lines[1:]
```
Separa o cabeçalho dos dados.

```python
    chunk_size = len(data_lines) // num_threads
```
Divide os dados igualmente entre as threads.

```python
    for i in range(num_threads):
        start = i * chunk_size
        end = (i + 1) * chunk_size if i < num_threads - 1 else len(data_lines)
        chunk = data_lines[start:end]
```
Define os intervalos de linhas que cada thread irá processar.

```python
        thread = threading.Thread(target=process_csv_part, args=(chunk, i, target_plate, result, lock))
        threads.append(thread)
        thread.start()
```
Cria e inicia uma nova thread para processar o bloco de dados.

```python
    for thread in threads:
        thread.join()
```
Espera todas as threads terminarem antes de continuar.

---
### **Exibição dos resultados**
```python
    if result:
        thread_id, data = result[0]  
        print(f"\n\u2705 Thread {thread_id} encontrou a placa '{data[0]}':\n")
```
Se encontrou a placa, exibe a thread que a encontrou.

```python
        print("-" * 80)
        print(f"{header[0]:<10} {header[1]:<10} {header[2]:<10} {header[3]:<6} {header[4]:<15} {header[5]:<20} {header[6]:<5} {header[7]:<5}")
        print("-" * 80)
```
Imprime o cabeçalho formatado manualmente.

```python
        print(f"{data[0]:<10} {data[1]:<10} {data[2]:<10} {data[3]:<6} {data[4]:<15} {data[5]:<20} {data[6]:<5} {data[7]:<5}")
        print("-" * 80)
```
Exibe os dados encontrados formatados.

```python
    else:
        print(f"\n\u274c Nenhuma linha encontrada para a placa '{target_plate}'.")
```
Se a placa não for encontrada, exibe uma mensagem informando isso.

---
### **Execução do Programa**
```python
if __name__ == "__main__":
    main()
```
Garante que o script seja executado apenas quando rodado diretamente, chamando a função `main()`.

---
### **Resumo das Melhorias**
- **Threads** dividem a carga de trabalho, tornando a busca mais rápida.
- **Aceita placas com ou sem hífen**, melhorando a usabilidade.
- **Saída formatada** para melhor visualização dos resultados.

