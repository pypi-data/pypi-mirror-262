## LIBRERIAS
# Librería para Crear y Verificar Tramas
Esta Librería proporciona funciones para rear tramas con checksum
y verificar la integridad de dichas tramas
#### FUNCIONES ####

## Calcular_cheksum (trama)
Esta funcion toma una trama en formato hexadecimal como entrada y calcula el checksum, sumando todos los valores de los bytes de la trama y tomando el modulo 256.
Si la suma es mayor o igual a 256, el checksum se calcula como 256 menos la diferencia entre la suma y 256. 

Ejemplo de uso:

checksum = calcular_checksum("02 00 01 FE")
print("Checksum:", checksum)

## crear_trama (direccion_origen, direccion_destino, numero_bits, comando, datos)
Esta función crea una trama según una estructura proporcionada y calcula su checksum. Los parámetros direccion_origen, direccion_destino, numero_bits y comando son valores hexadecimales que se utilizan para construir la trama. El parámetro datos es una lista de valores que se agregan a la trama en formato hexadecimal.

Ejemplo de uso:

trama = crear_trama(0x01, 0x02, 0x03, 0xFE, [0x41, 0x5A, 0x4B])
print("Trama creada:", trama)

# Licencia
Licencia MIT

Este README.md proporciona una descripción general de la librería, explica las funciones disponibles, muestra ejemplos de uso y proporciona información sobre cómo contribuir y la licencia del proyecto.
