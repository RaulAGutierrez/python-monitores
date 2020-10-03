import threading
import time
import logging
import random

logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(threadName)s] - %(message)s', datefmt='%H:%M:%S', level=logging.INFO)


def productor(monitor):
    print("Voy a producir")
    for i in range(30):
 
        with monitor:          # hace el acquire y al final un release
            logging.info(f'Lista de items {items}')
            items.append(i)    # agrega un ítem
            logging.info(f'Produje item {i}')
            monitor.notify()   # Notifica que ya se puede hacer acquire
        time.sleep(2) # simula un tiempo de producción


class Consumidor(threading.Thread):
    def __init__(self, monitor,itemPermitidos,itemsConsumidos = 0):
        super().__init__()
        self.monitor = monitor
        self.itemPermitidos = itemPermitidos
        self.itemsConsumidos = itemsConsumidos

    def contarUnItemConsumido(self):
        self.itemsConsumidos += 1
    
    def totalItemsConsumidos(self):
        return self.itemsConsumidos
    
    def run(self):
        while (True):
            
            with self.monitor:          # Hace el acquire y al final un release    
                while len(items) < self.itemPermitidos:     # si no hay ítems para consumir
                    self.monitor.wait()  # espera la señal, es decir el notify
                x = items.pop(0)     # saca (consume) el primer ítem
                self.contarUnItemConsumido()
            
            logging.info(f'Consumí {x}')
            time.sleep(1)
          


# la lista de ítems a consumir
items = []

# El monitor
items_monit = threading.Condition()

# un thread que consume
cons1 = Consumidor(items_monit,1)
cons1.start()
cons2 = Consumidor(items_monit,1)
cons2.start()
cons3 = Consumidor(items_monit,1)
cons3.start()

# El productor
productor(items_monit)


print("total items del consumidor1 ",cons1.totalItemsConsumidos())
print("total items del consumidor2 ",cons2.totalItemsConsumidos())
print("total items del consumidor3 ",cons3.totalItemsConsumidos())

        
