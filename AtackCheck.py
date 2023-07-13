def check_atack(guardar, ler):
    if guardar == 1:
        escrever = open('switch.txt', 'w')
        escrever.write('1')
        escrever.close()
    if ler == 1:
        escrever = open('switch.txt', 'r')
        var = escrever.readline()
        escrever.close()
        return var