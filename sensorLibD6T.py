import time
import smbus
import math
import os

i2c_ch = 1


# TMP102 address on the I2C bus
i2c_address = 0x0A

# Register addresses
reg_temp = 0x4C
reg_config = 0x01


# Read temperature registers and calculate Celsius
def read_temp( bus, arreglo):

    for i in range(9):
        arreglo[i]=arreglo[i+1]
    # Read temperature registers
    val = bus.read_i2c_block_data(i2c_address, reg_temp, 5)

    print (val)

    tPTAT = (256 * val[1]) + val[0]
    tp= ((256 * val[3] )+ val[2])
    #tp= ((256 * val[3] )+ val[2]+110)/10

    os.system("clear")
    print ('tpTAT = ', tPTAT, ' tp = ', tp )

    arreglo[9]=tp
    suma=0
    print(arreglo)
    for i in arreglo:
        suma+=i
    #vari=round (((float(suma)*0.007898)+14.8) , 1)
    vari=round(-(0.0027 * pow(float(suma/10),2)) + 2.089*float(suma/10) - 0.3891,0)/10

    #print ('tpTAT = ', tPTAT, ' tp = '  )
    print(vari)

    if max(arreglo) == arreglo[0]:

        if vari>31 and vari<38.5:
            return vari
    return 0

def  rBus():
    return smbus.SMBus(i2c_ch)

def temp ():
    bus = rBus()
    arreglo =[0]*10
    var=0
    while var==0:

        var=read_temp(bus, arreglo)



        #print(round(temperature, 2), "C")
        time.sleep(0.05)
        if var >31 and var<34:
            return var + 2
    return var