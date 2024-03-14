import os


def tail(file_path):
    # Получаем последние 10 строк файла
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            last_lines = lines[-10:]
            return last_lines
    except FileNotFoundError:
        return []


def process_files(file_paths, output_file):
    for file_path in file_paths:
        if len(file_paths) > 1:
            # Выводим разделитель перед каждым файлом, если передано больше одного файла
            print(f"\n\n==> {file_path} <==\n")
            output_file.write(f"\n\n==> {file_path} <==\n")

        last_lines = tail(file_path)

        for line in last_lines:
            # Выводим каждую строку в консоль и записываем в файл
            print(line, end='')
            output_file.write(line)


def user_input(output_file):
    print("Enter 20 lines:")
    user_lines = []
    for _ in range(20):
        line = input()
        user_lines.append(line.strip())

    # Выводим последние 17 строк из введенных пользователем строк
    for line in user_lines[-17:]:
        print(line)
        output_file.write(line + '\n')


def main():
    file_paths = ["task_2", "task_2_1"]

    # Проверяем существование файлов по их именам
    existing_files = [file_path for file_path in file_paths if os.path.exists(file_path)]

    if existing_files:
        # Если хотя бы один файл существует, обрабатываем его
        with open("artifacts/artifact_2.txt", 'w') as output_file:
            process_files(existing_files, output_file)
    else:
        # Если ни одного существующего файла нет, переходим к пользовательскому вводу
        with open("artifacts/artifact_2.txt", 'w') as output_file:
            user_input(output_file)

if __name__ == "__main__":
    main()
