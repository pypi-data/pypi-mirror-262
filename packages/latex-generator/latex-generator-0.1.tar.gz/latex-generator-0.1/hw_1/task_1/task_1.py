import argparse
import os


def nl(line, line_number, output_file_path=None):
    # Выводим пронумерованную строку в консоль
    print(f"{line_number}\t{line.strip()}")

    # Если указан путь к файлу для записи, записываем туда вывод
    if output_file_path:
        with open(output_file_path, 'a') as out_file:
            out_file.write(f"{line_number}\t{line.strip()}\n")


def process_files(file_paths, output_file_path):
    for file_path in file_paths:
        # Проверяем, существует ли файл
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                for i, line in enumerate(file, start=1):
                    nl(line, i, output_file_path)


def user_input(output_file_path, num_lines):
    # Читаем строки из stdin
    for i in range(1, num_lines + 1):
        line = input()
        nl(line, i, output_file_path)  # Выводим после каждого ввода

if __name__ == "__main__":
    # Парсинг аргументов командной строки
    file_paths = ["task_1"]
    output_file_path = "artifacts/artifact_1.txt"
    num_lines = 5  # Пример: количество строк для пользовательского ввода

    # Проверяем существование файлов по их именам
    existing_files = [file_path for file_path in file_paths if os.path.exists(file_path)]

    if existing_files:
        # Если хотя бы один файл существует, обрабатываем его
        process_files(existing_files, output_file_path)
    else:
        # Если ни одного существующего файла нет, переходим к пользовательскому вводу
        user_input(output_file_path, num_lines)
