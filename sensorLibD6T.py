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

    #print (val)

    tPTAT = (256 * val[1]) + val[0]
    tp= ((256 * val[3] )+ val[2])
    #tp= ((256 * val[3] )+ val[2]+110)/10

    #os.system("clear")
    print ('tpTAT = ', tPTAT, ' tp = ', tp )

    arreglo[9]=tp
    suma=0
    #print(arreglo)
    for i in arreglo:
        suma+=i
    #vari=round (((float(suma)*0.007898)+14.8) , 1)
    #vari=round(-(0.0027 * pow(float(suma/10),2)) + 2.089*float(suma/10) - 0.3891,0)/10
    vari=0
    if tp>= tPTAT:
        vari=round(tp * 0.5508)
        if tPTAT < 200:
            vari +=200.8
        elif tPTAT < 251:
            vari +=185.8
        elif tPTAT < 280:
            vari +=195.8
        elif tPTAT < 305:
            vari +=189.8
        elif tPTAT < 335:
            vari +=193.8
        else:
            vari+= 191.8
        vari=round(vari/10, 1)
    print(vari)
    if vari>33 and vari<38.5:
        return vari
    return 0
    
def  rBus():
    return smbus.SMBus(i2c_ch)

def temp ():
    # return 36.6
    bus = rBus()
    arreglo =[0]*10
    var=0
    while var==0:

        var=read_temp(bus, arreglo)
        #print(round(temperature, 2), "C")
        time.sleep(0.05)
        if var >33 and var<=34:
            return var + 2
        elif var>37.7 and 38.5:
            return var-1
        if var >35 and var < 37.7: 
            return var
        var = 0
        
        

