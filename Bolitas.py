# -*- coding: utf-8 -*-
"""
Created on Thu Oct  1 17:48:35 2020

@author: Raul A. Gutierrez - Prog. Concurrente
"""

import threading
import time
import logging

logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(threadName)s] - %(message)s', datefmt='%H:%M:%S', level=logging.INFO)

def juego(monitorDeParticipantes,listaElementos):
    print(f'Arranquemos a jugar')
    while True:
        
        with monitorDeParticipantes:   # hace el acquire y al final un release por cada turno de cada participante
            logging.info(f'La cantidad de BOLITAS en el frasco es {len(listaElementos)}')
            monitorDeParticipantes.notify()  # notifica a los participantes
            logging.info(f'Proximo participante')
            time.sleep(2)
        
        time.sleep(3)  # espera para ejecutar el proximo turno.

class Participante(threading.Thread):
    def __init__(self, nombre,listaElementos,cantidadBolitasQuePone,cantidadBolitasQueSaca,monitor):
        super().__init__()
        self.nombre = nombre
        self.listaElementos = listaElementos
        self.cantidadBolitasQuePone = cantidadBolitasQuePone
        self.cantidadBolitasQueSaca = cantidadBolitasQueSaca
        self.monitor = monitor
        
    def run (self):
        contador = 0
        while True:
            contador += 1
            
            logging.info(f'RONDA {contador}')
            with self.monitor:   # hace un acquiere y al final un release, cuando el participante es notificado
            
                self.monitor.wait()
                logging.info(f'{self.nombre} va a ingresar {self.cantidadBolitasQuePone} BOLITAS')
                for i in range (int(self.cantidadBolitasQuePone)):
                    logging.info(f'{self.nombre} ingresa {i + 1} BOLITA,  de la RONDA {contador}')
                    self.listaElementos.append(i)
                    time.sleep(1)
                logging.info(f'{self.nombre} debe poder sacar {self.cantidadBolitasQueSaca} BOLITAS')
                time.sleep(2)
                logging.info(f'Hay {len(self.listaElementos)} para sacar: ALCANZA?')
                time.sleep(2)
                while len(self.listaElementos) < self.cantidadBolitasQueSaca:
                    self.monitor.wait()
                for i in range (int(self.cantidadBolitasQueSaca)):
                    logging.info(f'{self.nombre} sanca {i + 1} BOLITA, de la RONDA {contador}')
                    self.listaElementos.pop(0)
                    time.sleep(1)
                logging.info(f'Hay {len(self.listaElementos)} BOLITAS para el siguiente participante')    
                
            time.sleep(3)

# Frasco de bolitas
frasco = []

# monitor
mmonitorParticipantes = threading.Condition()

# un thread por cada participante
participante1 = Participante("MARTIN",frasco,3,2,mmonitorParticipantes)
participante1.start()
participante2 = Participante("SEBASTIAN",frasco,2,2,mmonitorParticipantes)
participante2.start()
participante3 = Participante("RAUL",frasco,5,8,mmonitorParticipantes)
participante3.start()

#The game is beginning....
juego(mmonitorParticipantes,frasco)

