import re

with open("download_info_new.txt", "r") as fp:
    lines = fp.readlines()
    for line in lines:
        if "file_path" in line:
            match = re.search(r"Ссылка: (.*)", line)
            if match:
                link_text = match.group(1)
                print(link_text)
