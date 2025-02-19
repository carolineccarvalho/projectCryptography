#redefine o tamanho da chave
def reshape(ipClass, round, key):
    keyCopy = key
    if(ipClass == 'A'):
        if(round % 2 == 0):
            while(len(keyCopy)!=24):
                keyCopy.insert(0,0)
                
        else:
            keyCopy = keyCopy[-8:]
            
    elif(ipClass == 'C'):
        if(round % 2 != 0):
            while(len(keyCopy)!=24):
                keyCopy.insert(0,0)
                
        else:
            keyCopy = keyCopy[-8:]
            
            
    return keyCopy

#Aumenta a chave para um valor definido
def expand(size, key):
    keyCopy = key.copy()
    i = 0
    while(len(keyCopy) < size):
                keyCopy.insert(0,key[i])
                i = i + 1
                if(i==len(key)):
                    i = 0

   
    while(len(keyCopy) > size):
        keyCopy.pop(0)

    return keyCopy

def int_to_binary_list(n):
  binary_list = []
  while n > 0:
    bit = n % 2
    binary_list.insert(0, bit)  # Insert at beginning to get correct order
    n //= 2

  if(len(binary_list) == 0):
    binary_list.append(0)
    binary_list.append(0)

  if(len(binary_list) == 1):
    binary_list.append(0)
    binary_list.reverse()

  return binary_list

