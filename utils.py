import docx2txt
import glob
import os

def convert_docx_2_txt():
    directory = glob.glob('/home/charslib/Documents/hakathon/RussiaBank/*.docx')

    for file_name in directory:
        with open(file_name, 'rb') as infile:
            with open(file_name[:-5]+'.txt', 'w', encoding='utf-8') as outfile:
                doc = docx2txt.process(infile)
                outfile.write(doc)

    print("=========")
    print("All done!")


def get_text_files(directory = "docs/."):
    txt_files = []

    for file in os.listdir(directory):
        if file[-4:] == ".txt":
            txt_files.append(file)
    return txt_files
