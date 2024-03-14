input_file = "download_info.txt"
output_file = "download_info_new.txt"
with open(input_file, "r") as file:
    lines = file.readlines()

# Фильтруем строки, чтобы оставить только те, которые содержат слово "qwerty"
filtered_lines = [line for line in lines if not ".zip" in line]

# Записываем отфильтрованные строки в новый файл
with open(output_file, "w") as file:
    file.writelines(filtered_lines)
