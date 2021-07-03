import os, shutil, sys, time, subprocess

def scrub_folders():
    for root, dirs, files in os.walk("BancoQuestoes/"):
        if not 'All' in root:     # do not walk over this folder
            for f in files:
                if '.Rnw' in f or '.jpg' in f:
                    shutil.copyfile(f'{root}/{f}', f'BancoQuestoes/All/{f}')
                    tags_full = root.strip('BancoQuestoes/')
                    if '\\' in tags_full:
                        tags_split = tags_full.split('\\')
                        tag1 = tags_split[0]
                        tag2 = ''.join(tags_split[1:])  # descobrir pq come a ultima letra (?)
                        # print(f'{tag1} | {tag2} \t {root}/{f}') 
                    else:
                        tag1 = tags_full
                        tag2 = ""
                    if '.Rnw' in f:
                        add_tags(f'BancoQuestoes/All/{f}', f'#TAGS - TEMA:{tag1} \n#TAGS - SUBTEMA:{tag2} \n')

def add_tags(file_name, text):
    with open(file_name, 'r', encoding='utf-8') as original: 
        data = original.read()
    with open(file_name, 'w', encoding='utf-8') as modified:
        modified.write(text + '\n' + data)
    

def delete_files_Geral():
    files = os.listdir('BancoQuestoes/All/')
    for f in files:
        if '.jpg' in f or '.Rnw' in f or '.html' in f:
            os.remove(f'BancoQuestoes/All/{f}')

def create_html():
    files = os.listdir('BancoQuestoes/All/')
    for f in files:
        if '.Rnw' in f:
            command = f'Rscript.exe make_html.R {f} {42}'
            subprocess.call(command, cwd="BancoQuestoes/All/")
            # ret = subprocess.run(command, capture_output=True, shell=True, cwd="BancoQuestoes/All")  
            # print(f, ret)

if __name__ == '__main__':
    delete_files_Geral()
    scrub_folders()
    create_html()