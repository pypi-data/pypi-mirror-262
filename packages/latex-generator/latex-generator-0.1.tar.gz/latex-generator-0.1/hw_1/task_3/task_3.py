import os


def wc(file_path):
    try:
        with open(file_path, 'r') as file:
            # Считаем строки, слова и байты в файле
            lines = file.readlines()
            num_lines = len(lines)
            num_words = sum(len(line.split()) for line in lines)
            num_bytes = os.path.getsize(file_path)
            return num_lines, num_words, num_bytes
    except FileNotFoundError:
        return 0, 0, 0


def process_files(file_paths, output_file):
    if len(file_paths) == 1:
        # Если передан только один файл, выводим его статистику без суммарной статистики
        file_path = file_paths[0]
        num_lines, num_words, num_bytes = wc(file_path)

        # Выводим статистику и имя файла
        print(f"\n==> {file_path} <==")
        print(f"\nLines\tWords\tBytes\tFile")
        print(f"{num_lines}\t{num_words}\t{num_bytes}\t{file_path}")
        output_file.write(f"\n==> {file_path} <==")
        output_file.write(f"\nLines\tWords\tBytes\tFile\n")
        output_file.write(f"{num_lines}\t{num_words}\t{num_bytes}\t{file_path}\n")
    else:
        # Если передано больше одного файла, обрабатываем каждый файл и выводим суммарную статистику
        total_lines, total_words, total_bytes = 0, 0, 0

        for file_path in file_paths:
            # Получаем статистику для каждого файла
            num_lines, num_words, num_bytes = wc(file_path)

            # Выводим статистику и имя файла
            print(f"\n==> {file_path} <==")
            print(f"\nLines\tWords\tBytes\tFile")
            print(f"{num_lines}\t{num_words}\t{num_bytes}\t{file_path}")
            output_file.write(f"\n==> {file_path} <==")
            output_file.write(f"\nLines\tWords\tBytes\tFile\n")
            output_file.write(f"{num_lines}\t{num_words}\t{num_bytes}\t{file_path}\n")

            # Обновляем суммарную статистику
            total_lines += num_lines
            total_words += num_words
            total_bytes += num_bytes

        # Выводим суммарную статистику в конце, если передано больше одного файла
        print(f"\n==> Total <==")
        print(f"\nLines\tWords\tBytes\t")
        print(f"{total_lines}\t{total_words}\t{total_bytes}\t")
        output_file.write(f"\n==> Total <==")
        output_file.write(f"\nLines\tWords\tBytes\t\n")
        output_file.write(f"{total_lines}\t{total_words}\t{total_bytes}\n")


def user_input(output_file):
    print("Enter 5 lines:")
    user_lines = [input().strip() for _ in range(5)]

    # Считаем статистику для введенных строк
    num_lines = len(user_lines)
    num_words = sum(len(line.split()) for line in user_lines)
    num_bytes = sum(len(line.encode()) for line in user_lines)

    print(f"\nLines\tWords\tBytes\t")
    print(f"{num_lines}\t{num_words}\t{num_bytes}\t")
    output_file.write(f"\nLines\tWords\tBytes\t\n")
    output_file.write(f"{num_lines}\t{num_words}\t{num_bytes}\t\n")


def main():
    file_paths = ["task_3", "task_3_1"]

    # Проверяем существование файлов по их именам
    existing_files = [file_path for file_path in file_paths if os.path.exists(file_path)]

    if existing_files:
        # Если хотя бы один файл существует, обрабатываем его
        with open("artifacts/artifact_3.txt", 'w') as output_file:
            process_files(existing_files, output_file)
    else:
        # Если ни одного существующего файла нет, переходим к пользовательскому вводу
        with open("artifacts/artifact_3.txt", 'w') as output_file:
            user_input(output_file)


if __name__ == "__main__":
    main()
