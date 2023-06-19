import random
import time
from threading import Thread, Lock


def tentaPegar(filosofo, hashis, lado):
    r = -1
    if lado == 'esq':
        if not hashis[filosofo['esq']].locked():
            hashis[filosofo['esq']].acquire(True)
            r = filosofo['esq']
    elif lado == 'dir':
        if not hashis[filosofo['dir']].locked():
            hashis[filosofo['dir']].acquire(True)
            r = filosofo['dir']
    return r
    
def comer(filosofo, hashis):
    if filosofo['pegouEsq'] == -1:
        filosofo['pegouEsq'] = tentaPegar(filosofo, hashis, 'esq')
    
    if filosofo['pegouDir'] == -1:
        filosofo['pegouDir'] = tentaPegar(filosofo, hashis, 'dir')

    if filosofo['pegouEsq'] != -1 and filosofo['pegouDir'] != -1:
        print(f"{filosofo['nome']} COMEÇOU a comer.")
        time.sleep(random.uniform(1, 3))
        print(f"{filosofo['nome']} PAROU de comer.")
        hashis[filosofo['pegouEsq']].release()
        hashis[filosofo['pegouDir']].release()
        filosofo['faz'] = 'pensando'
        filosofo['pegouEsq'] = -1
        filosofo['pegouDir'] = -1
    else:
        # Caso o filósofo não consiga pegar os dois hashis, ele libera o que pegou
        if filosofo['pegouEsq'] != -1:
            hashis[filosofo['pegouEsq']].release()
            filosofo['pegouEsq'] = -1
        
        if filosofo['pegouDir'] != -1:
            hashis[filosofo['pegouDir']].release()
            filosofo['pegouDir'] = -1

        tempo = random.uniform(1, 3)
        time.sleep(tempo)
        
def run(filosofo, hashis):
    while True:
        if filosofo['faz'] == 'pensando':
            tempo = random.uniform(0, 3)
            print(f"{filosofo['nome']} vai pensar por {tempo} segundos.")
            time.sleep(tempo)
            filosofo['faz'] = 'esperando'

        elif filosofo['faz'] == 'esperando':
            comer(filosofo, hashis)
        
def inicia(filosofos, hashis, i):
    if i < len(filosofos):
        if i != len(filosofos) - 1:
            hashis[filosofos[i]['esq']].acquire(True)
            filosofos[i]['pegouEsq'] = filosofos[i]['esq']  # Correção aqui
        inicia(filosofos, hashis, i+1)

if __name__ == "__main__":
    nomes = ['Aristóteles', 'Platão', 'Sócrates', 'Pitágoras', 'Demócrito']  # Nomes dos filósofos
    filosofos = [{"id": x,"nome": nomes[x],"esq": x%5,"dir":(x+1)%5,"pegouEsq": -1,"pegouDir": -1,"faz": "pensando"} for x in range(5)]
    hashis = [Lock() for _ in range(5)]
    inicia(filosofos, hashis, 0)
    print([i.locked() for i in hashis])

    for i in filosofos:
        Thread(target=run, args=(i, hashis)).start()