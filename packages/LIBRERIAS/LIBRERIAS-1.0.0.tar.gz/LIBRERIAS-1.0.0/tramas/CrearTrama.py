def calcular_checksum(trama):
    # Convierto trama en hexadecimal a trama en bytes para sumarla
    trama_byte = bytes.fromhex(trama)
    # Suma todos los valores ASCII de los caracteres en la trama convertida
    check = sum(trama_byte)
    # Devuelve el checksum módulo 256, comprobando que si check > 256 , el cheksum es 256 menos la diferencia que hay entre ambos
    if check >= 256:
        checksum = 256 - (abs(256-check))
    else:
        checksum = abs(256-check)
    return checksum # valor absoluto por si cheksum es mayor que 256


def crear_trama(direccion_origen, direccion_destino, numero_bits, comando, datos):
    # Construye la trama según la estructura proporcionada
    trama = f"{direccion_destino:02X} {numero_bits:02X} {direccion_origen:02X} {comando:02X} "
    # Agregar cada elemento de la lista datos a la trama en formato hexadecimal
    for dato in datos:
        trama += f"{dato:02X} "
    # Calcula el checksum de la trama
    checksum = calcular_checksum(trama)
    # Agrega el checksum a la trama
    trama += f"{checksum:02X}\n"  # Asegura que el checksum esté representado por dos caracteres hexadecimales
    return trama