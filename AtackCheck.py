from random import randint

def check_atack(guardar, ler, mome):
    if guardar == 1:
        nome = str(mome)
        escrever = open(f'txts/{nome}.txt', 'w')
        escrever.write('1')
        escrever.close()
    if ler == 1:
        nome1 = str(mome)
        escrever = open(f'txts/{nome1}.txt', 'r')
        var = escrever.readline()
        escrever.close()
        return var
    

def create_archive(nome):
    arquivo = str(nome)
    escrever = open(f'txts/{arquivo}.txt', 'w')
    escrever.write('0')
    escrever.close()