import numpy as np
import utilities

Matriz = []


#guardar a linha que usou da SBox da primeira vez para decriptografar
lineSBoxFirst = []

#guardar a linha que usou da SBox da segunda vez para decriptografar
lineSBoxSecond = []

#SBox que eu defini para a substituição
SBox = np.array([[0, 1],
                 [2, 3],
                 [0, 1],
                 [2, 3]
                 ])

# TABELA DE EXPANSÃO E PERMUTAÇÃO PARA 24 BITS
EP = np.array([[1, 0, 0, 0, 0, 0],
               [0, 1, 0, 0, 0, 0],
               [0, 0, 1, 0, 1, 0],
               [0, 0, 0, 1, 0, 1],
               ])

#função de substituição utilizando a SBox
def substituition(matrix):
  new_matrix = []
  for row in matrix:
    result = int(row[0] * 2 + row[2])
    lineSBoxFirst.append(result)
    value = SBox[result][int(row[1])]
    value1, value2 = utilities.int_to_binary_list(value)
    new_row = [value1, value2,int(row[3]),int(row[4]),int(row[5])]
    new_matrix.append(new_row)

  matrix = new_matrix
  new_matrix = []
  for row in matrix:
    result = int(row[0] * 2 + row[2])
    lineSBoxSecond.append(result)
    value = SBox[result][int(row[1])]
    value1, value2 = utilities.int_to_binary_list(value)
    new_row = [value1, value2,int(row[3]),int(row[4])]
    new_matrix.append(new_row)

  return new_matrix


#matriz de permutação
Permutation = np.array([[0, 1, 0, 0],
                        [0, 0, 1, 0],
                        [0, 0, 0, 1],
                        [1, 0, 0, 0],
                      ])



#função de criptografia

def encryption(key, part):
    line = int(len(part)/4)
    
    Matriz = np.array(part).reshape(line,4)
    result = np.dot(Matriz, EP).astype(int)
    newKey = utilities.expand(result.size, key)
    Key = np.array(newKey).reshape(result.shape)
    result_matrix = np.bitwise_xor(result, Key).astype(int)
    aux = substituition(result_matrix)
    aux = np.array(aux).astype(int)
    new = np.dot(aux,Permutation)
    
    return (new.flatten().tolist(), lineSBoxFirst, lineSBoxSecond) 



#função de decriptografia
def decryption(IPanom, first, second, Key):
    line = int(len(IPanom)/4)
    
    IPanom = np.array(IPanom).reshape(line,4)
    original_matrix = np.dot(IPanom, np.linalg.inv(Permutation)).astype(int)

    newMatrix = []
    i=0
    for row in original_matrix:
        value = SBox[second[i]]
        if(value[0] == 2*row[0] + row[1]):
            new_row = []
            new_row.append(int(second[i]/2))
            new_row.append(0)
            new_row.append(int(second[i]%2))
            new_row.append(row[2])
            new_row.append(row[3])

            newMatrix.append(new_row)
        else:
            new_row = []
            new_row.append(int(second[i]/2))
            new_row.append(int(1))
            new_row.append(second[i]%2)
            new_row.append(row[2])
            new_row.append(row[3])
            newMatrix.append(new_row)
        i = i+1

    i=0

    recupera = []
    for row in newMatrix:
        value = SBox[first[i]]
        if(value[0] == 2*row[0] + row[1]):
            new_row = []
            new_row.append(int(first[i]/2))
            new_row.append(0)
            new_row.append(int(first[i]%2))
            new_row.append(row[2])
            new_row.append(row[3])
            new_row.append(row[4])
            recupera.append(new_row)
        else:
            new_row = []
            new_row.append(int(first[i]/2))
            new_row.append(int(1))
            new_row.append(first[i]%2)
            new_row.append(row[2])
            new_row.append(row[3])
            new_row.append(row[4])
            recupera.append(new_row)
        i = i+1

    recupera = np.array(recupera)
    newKey = utilities.expand(recupera.size, Key)
    newKey = np.array(newKey).reshape(recupera.shape)
    result_matrix = np.bitwise_xor(recupera, newKey)
    linhas_de_zeros = np.zeros((2, EP.shape[1]))
    matriz_expan = np.vstack((EP, linhas_de_zeros)).astype(int)

    result = np.dot(result_matrix, matriz_expan).astype(int)
    return result[:, :4].flatten().tolist()
    

part = [0,1,1,0,1,1,1,1]
key = [0,0,0,1,1,0,0,1]

