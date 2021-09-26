import numpy as np

def row_cases(vector, size, padding):
    # Se coge el primer término para generar la recursividad.
    # Se genera el total de casos posibles.
    first = vector[0]
    cases = np.array([0] * size)
    re_size = size - first

    # Caso base.
    if(len(vector) == 1):
        for i in range(re_size + 1):
            current_case = np.pad(np.array([1]*first), (i, re_size - i))
            comparison = current_case - padding

            if(1 not in comparison and -1 not in comparison):
                cases += current_case

    # Caso general.
    else:
        vector_iterator = np.delete(vector, 0)
        occupied_size = sum(vector) + len(vector) - first - 2
        for i in range(1, re_size - occupied_size + 1):
            row_first_ones = np.pad([1] * first, (i - 1, 0))
            comparison = row_first_ones - padding[0 : i + first - 1]

            # Se compara que que todos los primeros elementos corresponden
            # con el vector fila de 1 de tamaño "primera componente del
            # vector", y que el relleno en la posición "primera componente"
            # +1 sea diferente de 0 (Luego del vector fila debe haber un 0).
            if(1 not in comparison and -1 not in comparison
               and padding[i + first - 1] != 1 and padding[i + first - 1] != -1):
                iterator = row_cases(vector_iterator, re_size - i, padding[i + first : size])
                cases += np.pad(iterator, (size - len(iterator), 0))
                row_first = row_first_ones * sum(iterator) / sum(vector_iterator)
                cases += np.pad(row_first.astype(int), (0, re_size - i + 1))

    return cases

def row_comprobation(vector, padding, size):
    # Generando el vector que se obtiene con ese rellenado.
    comparison_vector = np.zeros(len(vector), dtype = int)
    number_of_ones = 0
    index = 0

    # Se mira cuántos unos hay entre los ceros y se pone en un array.
    for i in range(size):
        if(padding[i] == 0 and number_of_ones != 0):
            comparison_vector[index] = number_of_ones
            number_of_ones = 0
            index += 1
        elif(padding[i] == 1):
            number_of_ones += 1

    # Si al final hay un uno, no habrá cero que genere la cantidad de
    # unos que había entre el último cero y la última parte del rellenado.
    if(padding[size - 1] == 1):
        comparison_vector[len(comparison_vector) - 1] = number_of_ones
    
    return np.all(comparison_vector == vector)

def new_row(vector, size, padding):
    # Si el rellenado ya está completo (Lleno de unos y ceros), no hay
    # modificaciones por hacer.
    if(3 not in padding):
        if(row_comprobation(vector, padding, size)):
            return padding
        
        # Por si el rellenado no es el adecuado para la configuración.
        else:
            return "No concuerda el rellenado con lo especificado."
    else:
        cases = row_cases(vector, size, padding)
        row_probabilities = cases * sum(vector) / sum(cases)
        for i in range(0, size):
            if(row_probabilities[i] != 1 and row_probabilities[i] != 0):
                row_probabilities[i] = 3
        return row_probabilities

def solve_nonogram_matrix(vectors_row, vectors_column, size):
    nonogram_matrix = np.full((size[0], size[1]), fill_value = 3, dtype = int)

    # Se va a cambiar cada fila y colmuna según el relleno que tenga
    # y cómo debe estar rellenado.
    count = 0
    while(np.any(nonogram_matrix == 3)):
        matrix_rectifier = np.copy(nonogram_matrix)
        try:
            for i in range(max(size)):
                if(i < min(size)):
                    nonogram_matrix[i, :] = new_row(vectors_row[i], size[0], nonogram_matrix[i, :])
                    nonogram_matrix[:, i] = new_row(vectors_column[i], size[1], nonogram_matrix[:, i])
                elif(min(size) == size[1]):
                    nonogram_matrix[:, i] = new_row(vectors_column[i], size[1], nonogram_matrix[:, i])
                else:
                    nonogram_matrix[i, :] = new_row(vectors_row[i], size[0], nonogram_matrix[i, :])
        except:
            break

        if(np.all(matrix_rectifier == nonogram_matrix)):
            if(count < 2):
                count += 1
            else:
                break
        else:
            count = 0
    return nonogram_matrix

def rows_columns_creator(size):
    vectors_row = []
    vectors_column = []
    
    # Esto pedirá cada fila y columna.
    for i in range(max(size)):
        if(i < size[0]):
            vector = [int(j) for j in input("Inserte el array correspondiente a la fila " + str(i + 1) + " ").split()]
            occupied_size = sum(vector) + len(vector) - 1
            
            # Esto verifica que sea posible el rellenado de la fila i.
            if(occupied_size > size[0]):
                print("No es posible esa combinación en la fila " + str(i + 1))
            else:
                vectors_row.append(vector)
        
        if(i < size[1]):
            vector = [int(j) for j in input("Inserte el array correspondiente a la columna " + str(i + 1) + " ").split()]
            occupied_size = sum(vector) + len(vector) - 1
            
            # Esto verifica que sea posible el rellenado de la columna i.
            if(occupied_size > size[1]):
                print("No es posible esa combinación en la columna " + str(i + 1))
            else:
                vectors_column.append(vector)

    return (vectors_row, vectors_column)

# Activar lo siguiente si no tienes ya escritas los vectores filas y columnas.
n_rows = int(input("Inserte el número de filas "))
n_columns = int(input("Inserte el número de columnas "))
size = np.array([n_rows, n_columns])

(vectors_row, vectors_column) = rows_columns_creator(size)

matrix = solve_nonogram_matrix(vectors_row, vectors_column, size)

# Rectificador.
#matrix[i, :] = new_row(vectors_row[i], 15, matrix[i,:])