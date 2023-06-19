import random
import time
from threading import Thread, Lock

class Filosofo():

    def __init__(self, id, name, esq, dir, pegouEsq, pegouDir,faz):
        self.id = id
        self.name = name
        self.esq = esq
        self.dir = dir
        self.pegouEsq = pegouEsq
        self.pegouDir = pegouDir
        self.faz = faz
    
    def inicia(self, hashis):
        if self.id != len(hashis) - 1:
            hashis[self.esq].acquire(True)
            self.pegouEsq = self.esq
    
    def jantar(self, hashis):
        Thread(target=self.run, args=(hashis,)).start()

    def run(self, hashis):
        while True:
            if self.faz == 'pensando':
                tempo = random.uniform(0, 3)
                print(f"{self.name} vai pensar por {tempo} segundos.")
                time.sleep(tempo)
                self.faz = 'esperando'
            elif self.faz == 'esperando':
                self.comer(hashis)

    def comer(self, hashis):
        if self.pegouEsq == -1:
            self.pegouEsq = self.tentaPegar(hashis, 'esq')

        if self.pegouDir == -1:
            self.pegouDir = self.tentaPegar(hashis, 'dir')
        
        if self.pegouEsq != -1 and self.pegouDir != -1:
            print(f"{self.name} COMECOU a comer.")
            time.sleep(random.uniform(0,3))
            print(f"{self.name} TERMINOU de comer.")
            hashis[self.pegouEsq].release()
            hashis[self.pegouDir].release()
            self.pegouEsq = -1
            self.pegouDir = -1
            self.faz = 'pensando'
        else:
            if self.pegouEsq != -1:
                hashis[self.pegouEsq].release()
                self.pegouEsq = -1
            
            if self.pegouDir != -1:
                hashis[self.pegouDir].release()
                self.pegouDir = -1
            
            tempo = random.uniform(1, 3)
            time.sleep(tempo)
        
    def tentaPegar(self, hashis, lado):
        r = -1
        if lado == 'esq':
            if not hashis[self.esq].locked():
                hashis[self.esq].acquire(True)
                r = self.esq
        elif lado == 'dir':
            if not hashis[self.dir].locked():
                hashis[self.dir].acquire(True)
                r = self.dir
        return r

if __name__ == '__main__':
    nomes = ['Aristóteles', 'Platão', 'Sócrates', 'Pitágoras', 'Demócrito'] 
    filosofos = [Filosofo(id=x, name=nomes[x], esq=x%5, dir=(x+1)%5,pegouEsq=-1,pegouDir=-1,faz='pensando') for x in range(5)]
    hashis = [Lock() for _ in range(5)]
    for i in filosofos: i.inicia(hashis)
    for i in filosofos: i.jantar(hashis); time.sleep(0.1)




