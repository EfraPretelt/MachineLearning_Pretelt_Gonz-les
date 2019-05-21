#!/usr/bin/env python
# coding: utf-8

# In[13]:


import serial #Libreria que permite la comunicacion del robot
import pygame#Libreria que se usara para el uso de un mouse como "control"
import smbus#Libreria que emplearemos para el guardado de informacion del sensor
import time#Libreria implementada como temporadizadores
 
ser = serial.Serial('/dev/rfcomm0', 9600)#La antena que le otorgara comunicacion del robot con un controlador.
 
pygame.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption('Robot')
pygame.mouse.set_visible(1)
 
val = '-'#Estado de inicio del control remoto

robot = smbus.SMBus(1)
#Se comenzaran a escribir informacion en bytes para guardarla
robot.write_byte_data(0x39, 0x00 | 0x80, 0x0D)
robot.write_byte_data(0x39, 0x02 | 0x80, 0xFF)
robot.write_byte_data(0x39, 0x03 | 0x80, 0xFF)
robot.write_byte_data(0x39, 0x0E | 0x80, 0x20)
robot.write_byte_data(0x39, 0x0F | 0x80, 0x20)
#Luego de tomar los registros, este tomara un tiempo de 0,8 sg para comenzar el proceso.
time.sleep(0.8)
#I2C es un protocolo de comunicación serial, donde envia informacion a traves de una sola via de comunicacion, la informacion que manda es de bit en bit de forma cordinada.
data = robot.read_i2c_block_data(0x39, 0x18 | 0x80, 2)#Lee un bloque de hasta 32 bytes de un registro dado.
proximity = data[1] * 256 + data[0] #Se realiza el calculo de la proximidad(Se multiplica *256 por que cada Byte puede almacenar hasta 256,por que incluye hasta 8bits.)

print ("Distancia del robot : %d" %proximity)#Se mostrara la distancia entre el robot y el dispositivo
 
while val != 'stop': #Aqui se muestra como funcionara en el caso de uso manual 
    events = pygame.event.get()
    for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                        ser.write('a')
                elif event.key == pygame.K_LEFT:
                        ser.write('i')
            elif event.key == pygame.K_RIGHT:
                ser.write('d')
            elif event.key == pygame.K_DOWN:
                ser.write('r')
            elif event.key == pygame.K_ESCAPE:
                    val = 'stop'
            if event.type == pygame.KEYUP:
                ser.write('s')


# In[ ]:




