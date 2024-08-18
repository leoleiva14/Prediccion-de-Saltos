""" Tarea 1 Estructuras de Computadoras II    -    I Semestre 2024
    Codigo del predictor de saltos basado en perceptrones
    Estudiantes: Melissa Rodriguez Jimenez C16634 y Leonardo Leiva Vasquez C14172
"""
from math import floor
class perceptron:
    """
    Clase que implementa un predictor de tipo Perceptrón para predicción de ramas.

    Parámetros de entrada:
    - bits_to_index: Número de bits utilizados para indexar la tabla de pesos.
    - global_history_size: Tamaño de los registros de historia global.

    Parámetros de salida: Ninguno.
    """
    def __init__(self, bits_to_index, global_history_size):
        """
        Inicializa un objeto Perceptrón con los pesos, sesgo y variables estadísticas.

        Parámetros de entrada:
        - bits_to_index: Número de bits utilizados para indexar la tabla de pesos.
        - global_history_size: Tamaño de los registros de historia global.

        Parámetros de salida: Ninguno.
        """
        # Cantidad de bits definidos para el PC y la Historia Global
        self.bits_to_index = bits_to_index
        self.global_history_size = global_history_size

        # Se define matriz de pesos
        self.weights_list = [[1 if j == global_history_size else 0 for j in range(global_history_size + 1)] for _ in range(2 ** bits_to_index)]
        
        # Se define vector de entradas
        self.GHR = [-1] * global_history_size

        # Se define umbral que limita cantidad de entrenamiento
        self.threshold = 1.93 * global_history_size + 10

        #Inicializando estadisticas
        self.total_predictions = 0
        self.total_taken_pred_taken = 0
        self.total_taken_pred_not_taken = 0
        self.total_not_taken_pred_taken = 0
        self.total_not_taken_pred_not_taken = 0

    def print_info(self):
        """
        Imprime información sobre los parámetros del predictor Perceptrón.

        Parámetros de entrada: Ninguno.
        Parámetros de salida: Ninguno.
        """
        print("Parámetros del predictor:")
        print("\tTipo de predictor:\t\t\tPerceptron")
        print("\tEntradas en el Predictor:\t\t\t" + str(2**self.bits_to_index))
        print("\tTamaño de los registros de historia global:\t" + str(self.global_history_size))

    def print_stats(self):
        """
        Imprime estadísticas sobre los resultados de la simulación.

        Parámetros de entrada: Ninguno.
        Parámetros de salida: Ninguno.
        """
        print("Resultados de la simulación")
        print("\t# branches:\t\t\t\t\t\t" + str(self.total_predictions))
        print("\t# branches tomados predichos correctamente:\t\t" + str(self.total_taken_pred_taken))
        print("\t# branches tomados predichos incorrectamente:\t\t" + str(self.total_taken_pred_not_taken))
        print("\t# branches no tomados predichos correctamente:\t\t" + str(self.total_not_taken_pred_not_taken))
        print("\t# branches no tomados predichos incorrectamente:\t" + str(self.total_not_taken_pred_taken))
        perc_correct = 100 * (self.total_taken_pred_taken + self.total_not_taken_pred_not_taken) / self.total_predictions
        formatted_perc = "{:.2f}".format(perc_correct)
        print("\t% predicciones correctas:\t\t\t\t" + str(formatted_perc) + "%")

    def predict(self, PC):
        """
        Predice la toma o no toma de una rama utilizando el predictor Perceptrón.

        Parámetros de entrada:
        - PC: Contador de Programa (Program Counter) para la rama a predecir.

        Parámetros de salida:
        - prediction: Predicción de la toma ("T") o no toma ("N") de la rama.
        """
        PC_index = int(PC) % len(self.weights_list)

        # Obteniendo la prediccion a partir de las entradas y de la matriz de pesos
        y = self.weights_list[PC_index][-1] + sum(w * g for w, g in zip(self.weights_list[PC_index][:-1], self.GHR))
        prediction = "T" if y >= 0 else "N"
        return prediction

    def update(self, PC, result, prediction):
        """
        Actualiza los pesos y registros de historia según el resultado de la predicción.

        Parámetros de entrada:
        - PC: Contador de Programa (Program Counter) para la rama a actualizar.
        - result: Resultado real de la toma ("T" para tomada, "N" para no tomada).
        - prediction: Predicción de la toma ("T" para tomada, "N" para no tomada).

        Parámetros de salida: Ninguno.
        """
        PC_index = int(PC) % len(self.weights_list)
        t = 1 if result == "T" else -1

        # Obteniendo la prediccion a partir de las entradas y de la matriz de pesos
        y = self.weights_list[PC_index][-1] + sum(w * g for w, g in zip(self.weights_list[PC_index][:-1], self.GHR))
        m = 1 if y >= 0 else -1

        # Algoritmo de entrenamiento
        if m != t or abs(y) <= self.threshold:
            for i in range(len(self.GHR)):
                self.weights_list[PC_index][i] += t * self.GHR[i]
            self.weights_list[PC_index][-1] -= t * self.GHR[i]
            self.weights_list[PC_index][-1] += t

        # Se actualiza el vector de entradas
        if result == "T":
            self.GHR = self.GHR[1:] + [1]
        else:
            self.GHR = self.GHR[1:] + [0]
        self.update_statistics(result, prediction)

    def update_statistics(self, result, prediction):
        """
        Actualiza las estadísticas del predictor basado en el resultado y la predicción.

        Parámetros de entrada:
        - result: Resultado real de la toma ("T" para tomada, "N" para no tomada).
        - prediction: Predicción de la toma ("T" para tomada, "N" para no tomada).

        Parámetros de salida: Ninguno.
        """
        if result == "T" and result == prediction:
            self.total_taken_pred_taken += 1
        elif result == "T" and result != prediction:
            self.total_taken_pred_not_taken += 1
        elif result == "N" and result == prediction:
            self.total_not_taken_pred_not_taken += 1
        else:
            self.total_not_taken_pred_taken += 1
        self.total_predictions += 1
