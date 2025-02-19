import functionF
import functionFlinha
import utilities
import keyGenerator
import ipaddress
import pandas as pd
firstFlinha = []
firstF = []
secondFlinha = []
secondF = []
result = []
dec_to_bin = lambda ip: bin(int(ipaddress.ip_address(ip)))  
original = []
anonimizado = []

def findClass(ip):
    aux = ip.split(".")
    if(int(aux[0]) >= 0 and int(aux[0]) <= 127):
        return "A"
    elif(int(aux[0]) >=128 and int(aux[0]) <= 191):
        return "B"
   
    elif(int(aux[0]) >= 192 and int(aux[0]) <= 223):
        return "C"
   
    elif(int(aux[0]) >= 224 and int(aux[0]) <= 239):
        return "D"
   
    else:
        return "E"
    
def split(lista, classe) -> tuple[str, str]:
    if(classe == 'A'):
        return (lista[:8], lista[8:])
    if(classe == 'C'):
        return (lista[:24], lista[24:])
    
    half = int(len(lista) / 2)
    return (lista[:half], lista[half:])

def size(classe) -> tuple[str, str]:
    if(classe == 'A'):
        return (8, 24)
    if(classe == 'C'):
        return (24, 8)
    
    return (16, 16)

def xor_vectors(vec1, vec2):
    assert len(vec1) == len(vec2), "Os vetores devem ter o mesmo tamanho."
    return [a ^ b for a, b in zip(vec1, vec2)]

def octetos(parts, classe):
    if(classe == 'A'):
        aux = 0 
        q1 = ""
        while aux<8:
            q1 = q1 + str(parts[0][aux])
            aux += 1
        
        aux = 0 
        q2 = ""
        while aux<8:
            q2 = q2 + str(parts[1][aux])
            aux += 1     
        
        q3 = ""
        while aux<16:
            q3 = q3 + str(parts[1][aux])
            aux += 1
        
        q4 = ""
        while aux<24:
            q4 = q4 + str(parts[1][aux])
            aux += 1  
    
    if(classe == 'C'):
        aux = 0 
        q1 = ""
        while aux<8:
            q1 = q1 + str(parts[0][aux])
            aux += 1
        
        q2 = ""
        while aux<16:
            q2 = q2 + str(parts[0][aux])
            aux += 1     
        
        q3 = ""
        while aux<24:
            q3 = q3 + str(parts[0][aux])
            aux += 1
        
        aux = 0 
        q4 = ""
        while aux<8:
            q4 = q4 + str(parts[1][aux])
            aux += 1   
    
    
    if(classe == 'B' or classe == 'D' or classe == 'E'):
        aux = 0 
        q1 = ""
        while aux<8:
            q1 = q1 + str(parts[0][aux])
            aux += 1
            
        q2 = ""
        while aux<16:
            q2 = q2 + str(parts[0][aux])
            aux += 1     
            
        aux = 0 
        q3 = ""
        while aux<8:
            q3 = q3 + str(parts[1][aux])
            aux += 1
            
        q4 = ""
        while aux<16:
            q4 = q4 + str(parts[1][aux])
            aux += 1 
            
    
    return(q1,q2,q3,q4)



def encrypt(ip, round):
    classe = findClass(ip)
    listKey = keyGenerator.keyGenerator('key_strengh_nbits', round) 
    binary = dec_to_bin(ip)[2:]
    
    while(len(binary)!=32):
            binary = '0' + binary

    list_binary = keyGenerator.bin_to_list(binary)
    original.append(list(list_binary))
    parts = split(list_binary, classe)
    
    
    i = 0
    
    while(i!=round):
        if(i%2==0):
                esquerda = parts[0]
                direita = parts[1]
                anom = functionFlinha.encryption(listKey[i], esquerda)
                firstFlinha.append(anom[1])
                secondFlinha.append(anom[2])
                result.append(anom[0])
                aux = xor_vectors(anom[0], esquerda)
                
                parts = [direita, aux]
           
        else:
                direita = parts[0]
                esquerda = parts[1]
                
                anom = functionF.encryption(listKey[i], direita)
                firstF.append(anom[1])
                secondF.append(anom[2])
                result.append(anom[0])
                aux = xor_vectors(anom[0], utilities.expand(len(direita),parts[1]))
                parts = [esquerda, aux]
          
         
        if(i==round-1):
            lis = []
            for k in range(0, len(parts[0])):
                lis.append(parts[0][k])
                
            for k in range(0, len(parts[1])):
                lis.append(parts[1][k])
                
            anonimizado.append(list(lis))
            
        i = i + 1
       
    value = size(classe)
    
    
   
    ans = octetos(parts, classe)
    
    return(str(int(ans[0],2)) + "." + str(int(ans[1],2)) + "." + str(int(ans[2],2)) + "." + str(int(ans[3],2)))

def decrypt(ip, classe, key, round):
    listKey = keyGenerator.keyGenerator('key_strengh_nbits', round) 
    binary = dec_to_bin(ip)[2:]
    
    while(len(binary)!=32):
            binary = '0' + binary

    list_binary = keyGenerator.bin_to_list(binary)
    listKey.reverse()
    firstF.reverse()
    firstFlinha.reverse()
    secondF.reverse()
    secondFlinha.reverse()
    
    parts = split(list_binary, classe)
    
    i = 0
    l = 0
    r = 0
    while(i!=round):
        if(i%2==0):
                extendido = utilities.expand(len(parts[1]), parts[0])
                xored = xor_vectors(extendido, parts[1])
                anom = functionF.decryption(xored,firstF[l], secondF[l], listKey[i])
                parts = [parts[1], anom]
                l = l+1

        else:   
                xored = xor_vectors(parts[0], result[i])
                anom = functionFlinha.decryption(xored,firstFlinha[r], secondFlinha[r], listKey[i])
                parts = [parts[1], anom]
                r = r+1
                            
        i = i + 1
       
    ans = octetos(parts, classe)
    
    return(str(int(ans[0],2)) + "." + str(int(ans[1],2)) + "." + str(int(ans[2],2)) + "." + str(int(ans[3],2)))

    
