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
            logging.info(f'Lista de items {items}')
            #monitor.notify()   # Notifica que ya se puede hacer acquire
            monitor.notifyAll() # dar señal a todos los threads que están esperando
        time.sleep(2) # simula un tiempo de producción


class Consumidor(threading.Thread):
    def __init__(self, monitor,itemPermitidos,totalItemsConsumidos = 0):
        super().__init__()
        self.monitor = monitor
        self.itemPermitidos = itemPermitidos
        self.totalItemsConsumidos = totalItemsConsumidos

    def contarUnItemConsumido(self):
        self.totalItemsConsumidos += 1
        
    def totalItems(self):
        return str(self.totalItemsConsumidos)
    
    def consumeItems(self,listaItems):
        itemsQueSeConsumieron = []
        while self.itemPermitidos > len(itemsQueSeConsumieron):
            x = listaItems.pop(0)
            logging.info(f'consumir: {x}')
            itemsQueSeConsumieron.append(x)
            logging.info(f'Item que se consumieron: {x}')
            self.contarUnItemConsumido()
        itemsQueSeConsumieron = []
    
    
    def run(self):
        #while (True):
            
            with self.monitor:          # Hace el acquire y al final un release    
                
                while len(items) < self.itemPermitidos :     # si no hay ítems para consumir
                    self.monitor.wait()  # espera la señal, es decir el notify
                
                logging.info(f'Hay estos items para consumir: {items}')
                self.consumeItems(items)     # saca (consume) el primer ítem

            logging.info(f'Quedan estos Items {items}')
            time.sleep(1)
          


# la lista de ítems a consumir
items = []

# El monitor
items_monit = threading.Condition()

# un thread que consume
cons1 = Consumidor(items_monit,8)
cons1.start()
cons2 = Consumidor(items_monit,12)
cons2.start()
cons3 = Consumidor(items_monit,9)
cons3.start()

# El productor
productor(items_monit)


print("total items del consumidor1 ",cons1.totalItems())
print("total items del consumidor2 ",cons2.totalItems())
print("total items del consumidor3 ",cons3.totalItems())

        
