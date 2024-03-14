import os
import time
import threading
import multiprocessing


def fibonacci(n):
    if n <= 1:
        return n
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)


def run_synchronously(n):
    start_time = time.time()
    for _ in range(10):
        fibonacci(n)
    return time.time() - start_time


def run_with_threads(n):
    start_time = time.time()
    threads = []
    for _ in range(10):
        thread = threading.Thread(target=fibonacci, args=(n,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    return time.time() - start_time


def run_with_processes(n):
    start_time = time.time()
    processes = []
    for _ in range(10):
        process = multiprocessing.Process(target=fibonacci, args=(n,))
        process.start()
        processes.append(process)

    for process in processes:
        process.join()

    return time.time() - start_time


if __name__ == "__main__":
    script_directory = os.path.dirname(os.path.abspath(__file__))
    artifacts_directory = os.path.join(script_directory, "artifacts")
    os.makedirs(artifacts_directory, exist_ok=True)

    n = 35

    results = []

    # Синхронный запуск
    sync_time = run_synchronously(n)
    results.append(f"Synchronous Execution: {sync_time:.6f} seconds")

    # Запуск с использованием потоков
    thread_time = run_with_threads(n)
    results.append(f"Threaded Execution: {thread_time:.6f} seconds")

    # Запуск с использованием процессов
    process_time = run_with_processes(n)
    results.append(f"Multiprocessing Execution: {process_time:.6f} seconds")

    # Запись результатов в текстовый файл
    with open(os.path.join(artifacts_directory, "execution_times.txt"), 'w') as file:
        for result in results:
            file.write(result + "\n")