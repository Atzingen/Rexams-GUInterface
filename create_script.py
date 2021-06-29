import subprocess, random, time, sys, os, shutil, pathlib

def create_R_sample(var_name, min, max, step):
    return f'{var_name} <- sample(seq(from={min},to={max},by={step}),1)'

def vardom_2_varsol(data):
    variables, solutions = [], []
    for i in range(int(len(data)/2)):
        variables.append(data[2*i])
        solutions.append(data[2*i+1])
    return [variables, solutions]

def get_file(path, file_name):  
    try:
        with open(f'{path}/{file_name}', encoding='utf-8') as f:
            html_text = f.read()
        return html_text    
    except IOError as exc: ## TODO - Não retornar erro para o html - log e retun de erros para usuário
        return str(exc)

def del_file(path, file_name):
    try:
        os.remove(f'{path}/{file_name}')
        return True
    except Exception as e:
        print('Exception', e)
    return False

def move_Rnw(path, file_name):
    shutil.move('./CriaRnw/Rnw_question.Rnw', f'{path}/{file_name}')

def parse_solucoes_dom(solucoes_dom):
    var, texto, solucao = [], [], []
    for i in range(int(len(solucoes_dom)/3)):
        var.append(solucoes_dom[3*i])
        texto.append(solucoes_dom[3*i+1])
        solucao.append(solucoes_dom[3*i+2])
    return [var, texto, solucao]

def variable_formater(variables, solutions):
    data = []
    for variable, solution in zip(variables, solutions):
        data.append(f'{variable} <- {solution}')
    return data

def answerlist_formater(answerlist):
    data = []
    for answer in answerlist:
        data.append(f'\item {answer}')
    return data

def meta_formater(information):
    data = []
    data.append(f'%% META-INFORMATION')

    data.append(f'%% \extype{{{information[0]}}}')

    exsolution = '%% \exsolution{\Sexpr{'
    exclozetype = '%% \exclozetype{'
    respostas = information[1]
    last = respostas.pop(-1)
    for resposta in respostas:
        exsolution += resposta
        exsolution += '}|\Sexpr{'
        exclozetype += 'num|'
    exsolution += last
    exsolution += '}}'
    exclozetype += 'num}'
    data.append(exsolution)
    data.append(exclozetype)
    data.append(f'%% \exname{{{information[2]}}}')
    data.append(f'%% \extol{{{information[3]}}}')
    return data

def create_Rnw(data):
    fixed_txts = ['CriaRnw/Rnw_01_header.txt', 'CriaRnw/Rnw_02_questionStart.txt',
                  'CriaRnw/Rnw_03_answerlistStart.txt', 'CriaRnw/Rnw_04_answerlistEnd.txt', 
                  'CriaRnw/Rnw_05_closeAnserlist.txt']
    with open('CriaRnw/Rnw_question.Rnw', 'wb') as f:
        for i, file_name in enumerate(fixed_txts):
            with open(file_name, 'rb') as fd:
                shutil.copyfileobj(fd, f)    
            texto = ''
            for linha in data[i]:
                texto += linha
                texto += '\n'
            f.write(str.encode(texto))           

def create_xml(list_Rnw, n, subject):
    for i, file in enumerate(list_Rnw):
        shutil.copyfile(file, f'CriaAtividade/Q{i}.Rnw')
    t = int(time.time())
    output = subprocess.check_output(f'Rscript.exe ./CriaAtividade/make_moodle.R {subject} {t} {n}')
    
    list_all_files = os.listdir('CriaAtividade/')
    for file in list_all_files:
        if '.Rnw' in file:
            os.remove(f'CriaAtividade/{file}')

def create_html(filename_Rnw):
    print(filename_Rnw)
    t = int(time.time())
    output = subprocess.check_output(f'Rscript.exe CriaRnw/make_html.R {filename_Rnw} {t}')
    return output
       
def test_R_singleline(inline_data):
    t = int(time.time())
    path2script = f'tempFile_{t}.R'
    with open(path2script, 'w') as f:
        f.write(f'set.seed({t})\n')
        f.write(f'var_temp <- {inline_data}\n')
        f.write(f'print(var_temp)\n')
    command ='Rscript'
    cmd = [command, path2script]
    x = subprocess.check_output(cmd, universal_newlines=True)
    os.remove(path2script)
    return x

def list_all_Rnw():
    '''
    List all Rnw files in the folder BancoQuestoes.
    Used for sorting and search files by name.
    TODO: Tags for information inside question.
    '''
    all_Rnw = []
    for dirpath, dirs, files in os.walk("./BancoQuestoes"):
        for filename in files:
            if '.Rnw' in filename:
                all_Rnw.append(f'{dirpath}/{filename}')
    return all_Rnw

def list_all_images(Rnw_file):
    '''
    list all images related to the Rnw file and return it along with
    the full path to the folder.
    '''
    full_Rnw_path = pathlib.Path(Rnw_file)
    Rnw_name = full_Rnw_path.stem
    path_folder = full_Rnw_path.parent
    files = os.listdir(path_folder)
    images = [x for x in files if '.jpg' in x and Rnw_name in x]
    return images, path_folder