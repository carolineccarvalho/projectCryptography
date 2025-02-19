import hashlib
import ipaddress
import numpy as np


#transformar decimal para binário
dec_to_bin = lambda ip: bin(int(ipaddress.ip_address(ip)))  

#transformar binario do tipo 0b0000 para uma lista de binários
bin_to_list = lambda x: [int(d) for d in str(x)]

#cria a lista de chaves que serão utilizadas ao longo dos rounds
key_list = []

#importa a chave e retorna seu valor em uma lista de binários
def importKey(key):
    key40bits = hashlib.pbkdf2_hmac('sha256', key.encode('utf-8'),b'',100000, dklen=5)
    key_int = int.from_bytes(key40bits, byteorder='big')
    binary_key = bin(key_int)[2:]
    while(len(binary_key)!=40):
        binary_key = '0' + binary_key
    list_binary_key_menor = bin_to_list(binary_key)
    return list_binary_key_menor

#Realiza o shift para a esquerda
def left_shift(row):
    return np.roll(row, -1)


#gera todas as chaves
def keyGeneratorList(key, round):
    lista = np.array(key)
    for i in range(0, round):
        aux = left_shift(lista)
        value = aux.tolist()
        key_list.append(value)
        
    
def keyGenerator(key, round):
    binaryKey = importKey(key)
    keyGeneratorList(binaryKey, round)
    return key_list
