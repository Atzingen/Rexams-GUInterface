import os, shutil, sys, time

def scrub_folders():
    for root, dirs, files in os.walk("../"):
        if not 'Geral' in root:     # do not walk over this folder
            for f in files:
                if '.Rnw' in f or '.jpg' in f:
                    shutil.copyfile(f'{root}/{f}', f)
                    print(f'{root}/{f}')

def delete_files_Geral():
    files = os.listdir()
    for f in files:
        if '.jpg' in f or '.Rnw' in f:
            os.remove(f)