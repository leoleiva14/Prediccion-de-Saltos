""" Tarea 1 Estructuras de Computadoras II    -    I Semestre 2024
    Codigo del predictor de saltos P-Shared
    Estudiantes: Melissa Rodriguez Jimenez C16634 y Leonardo Leiva Vasquez C14172
"""

import math

class pshared:
    """
    Clase que implementa un predictor de tipo P-Shared para predicción de ramas.

    Parámetros de entrada:
    - bits_to_index: Número de bits del PC para indexar la tabla de historia local.
    - local_history_size: Tamaño de los registros de historia local.

    Parámetros de salida: Ninguno.
    """
    def __init__(self, bits_to_index, local_history_size):
        '''
        Inicializa un objeto de la clase

        Parámetros de entrada:
        - bits_to_index: Número de bits del PC para indexar la tabla de historia local.
        - local_history_size: Tamaño de los registros de historia local.

        Parámetros de salida: Ninguno.
        '''
        #Para la tabla de historia local
        self.bits_to_index = bits_to_index #Del PC
        self.size_of_local_history_table = 2**bits_to_index

        #Para la tabla de patrones
        self.local_history_size = local_history_size #Tamano de los registros de la historia local
        self.size_of_patron_table = 2**self.local_history_size

        #Agregando valores default de 0 para ambas tablas
        self.local_history_table = [0 for i in range(self.size_of_local_history_table)]
        self.patron_table = [0 for i in range(self.size_of_patron_table)]

        #Inicializando estadisticas
        self.total_predictions = 0
        self.total_taken_pred_taken = 0
        self.total_taken_pred_not_taken = 0
        self.total_not_taken_pred_taken = 0
        self.total_not_taken_pred_not_taken = 0

    def print_info(self):
        """
        Imprime información sobre los parámetros del predictor P-Shared.

        Parámetros de entrada: Ninguno.
        Parámetros de salida: Ninguno.
        """
        print("Parámetros del predictor:")
        print("\tTipo de predictor:\t\t\tP-Shared")
        print("\tEntradas en el Predictor:\t\t\t"+str(2**self.bits_to_index))
        print("\tTamaño de los registros de historia local:\t"+str(self.local_history_size))

    def print_stats(self):
        """
        Imprime estadísticas sobre los resultados de la simulación.

        Parámetros de entrada: Ninguno.
        Parámetros de salida: Ninguno.
        """
        print("Resultados de la simulación")
        print("\t# branches:\t\t\t\t\t\t"+str(self.total_predictions))
        print("\t# branches tomados predichos correctamente:\t\t"+str(self.total_taken_pred_taken))
        print("\t# branches tomados predichos incorrectamente:\t\t"+str(self.total_taken_pred_not_taken))
        print("\t# branches no tomados predichos correctamente:\t\t"+str(self.total_not_taken_pred_not_taken))
        print("\t# branches no tomados predichos incorrectamente:\t"+str(self.total_not_taken_pred_taken))
        perc_correct = 100*(self.total_taken_pred_taken+self.total_not_taken_pred_not_taken)/self.total_predictions
        formatted_perc = "{:.3f}".format(perc_correct)
        print("\t% predicciones correctas:\t\t\t\t"+str(formatted_perc)+"%")

    def predict(self, PC):
        """
        Predice la toma o no toma de una rama utilizando el predictor P-Shared.

        Parámetros de entrada:
        - PC: Contador de Programa (Program Counter) para la rama a predecir.

        Parámetros de salida:
        - prediction: Predicción de la toma ("T") o no toma ("N") de la rama.
        """

        PC_index = int(PC) % self.size_of_local_history_table
        local_history_table_entry = self.local_history_table[PC_index]
        patron_table_entry = self.patron_table[local_history_table_entry]

        if patron_table_entry in [0,1]:
            return "N"
        else:
            return "T"
  

    def update(self, PC, result, prediction):
        """
        Actualiza los registros de historia y la tabla de patrones según el resultado de la predicción.

        Parámetros de entrada:
        - PC: Contador de Programa (Program Counter) para la rama a actualizar.
        - result: Resultado real de la toma ("T" para tomada, "N" para no tomada).
        - prediction: Predicción de la toma ("T" para tomada, "N" para no tomada).

        Parámetros de salida: Ninguno.
        """
        PC_index = int(PC) % self.size_of_local_history_table
        local_history_table_entry = self.local_history_table[PC_index]
        patron_table_entry = self.patron_table[local_history_table_entry]

        #Actualiza tabla de patrones siguiendo la forma de un contador con saturacion
        if patron_table_entry == 0 and result == "N":
            updated_patron_table_entry = patron_table_entry

        elif patron_table_entry != 0 and result == "N":
            updated_patron_table_entry = patron_table_entry - 1

        elif patron_table_entry == 3 and result == "T":
            updated_patron_table_entry = patron_table_entry

        else:
            updated_patron_table_entry = patron_table_entry + 1
 
        #Cambia valor en tabla
        self.patron_table[local_history_table_entry] = updated_patron_table_entry

        #Actualizacion de historia local
        if result == "T":
            #Se corre a la izquierda y agrega un cero
            updated_local_history_table_entry = local_history_table_entry * 2
            if updated_local_history_table_entry > self.size_of_patron_table - 1:
                # Se suma 1 para hacerlo impar y agregar efecto de branch tomado
                updated_local_history_table_entry = abs(self.size_of_patron_table - updated_local_history_table_entry) + 1
            else:
                # Se suma 1 para hacerlo impar y agregar efecto de branch tomado
                updated_local_history_table_entry = local_history_table_entry * 2 + 1
            
        else:
            #Se corre a la izquierda y agrega un cero
            updated_local_history_table_entry = local_history_table_entry * 2
            if updated_local_history_table_entry > self.size_of_patron_table - 1:
                updated_local_history_table_entry = abs(self.size_of_patron_table - updated_local_history_table_entry)

        self.local_history_table[PC_index] = updated_local_history_table_entry


        #Actualizacion de estadisticas de saltos
        if result == "T" and result == prediction:
            self.total_taken_pred_taken += 1
        elif result == "T" and result != prediction:
            self.total_taken_pred_not_taken += 1
        elif result == "N" and result == prediction:
            self.total_not_taken_pred_not_taken += 1
        else:
            self.total_not_taken_pred_taken += 1

        self.total_predictions += 1
