import launchpad_py as lp 
import os
import threading
import time
import numpy as np
import math


altura = 8
largura = 8

eixoX = [0,1,2,3,4,5,6,7]
eixoY = [1,2,3,4,5,6,7,8]

#Color Pallete
pallete = [ 0, 7, 121, 5, 9, 13, 109, 3]

# Array que mapeia cada led (grid interno, sem contar os botoes de controle) a uma cor naquele instante mapeado através da posição do array
#  [  0,  1,  2,  3,  4,  5,  6,  7, 
#     8,  9, 10, 11, 12, 13, 14, 15,
#               ...
pixel_array = []

#Main color Pallete
color_array = np.arange(128).tolist()

#For recolor mode
temp_color_list=[]
# class led:
#     def __init__(self,position,color=0,mode="on"):
#         self.position = position
#         self.color = color
#         self.mode = mode


def start():
    criaEstruturaDadosPixels()
    criaGridColor()
    # criaFogo()
    # printaDados()
    # render()
    event = []
    while True and event!=[8,8,127]:
        event = eventUpdate()
        recolor(event)
        eventChecker(event)
        printaDados(event)
        render()
        # atualizaPixel(event)
        time.sleep(0.01)
    lp.LedAllOn(0)
    # set_interval(atualizaPixel(),1)

# def set_interval(func, sec):
#     e = threading.Event()
#     while not e.wait(sec):
#         func()
lastEvent = []
def eventUpdate():
    global lastEvent
    event = lp.ButtonStateXY()
    if event:
        lastEvent = event
        return event
    else:
        event=[-1,-1,-1]
        return event
        # if pixel_array[0]+1 > 127:
        #     pixel_array[0]=0
        # else: 

        #     pixel_array[0]+=1

def printaDados(event):

    os.system('cls')
    for linha in range(0,altura):
        print("\t")
        for coluna in range(0,largura):
            pixel_index = (linha*altura)+coluna
            if len(str(pixel_array[pixel_index])) == 1:
                print("  " + str(pixel_array[pixel_index]),end=' ')
            elif len(str(pixel_array[pixel_index])) == 2:
                print(" " + str(pixel_array[pixel_index]),end=' ')
            else: 
                print(pixel_array[pixel_index],end=' ')
    
    print("\n\n Pixel Array: [",end="")
    for i in range(0,len(pixel_array)):
        if len(str(pixel_array[i]))==1:
            comp = "  "
        elif len(str(pixel_array[i]))==2:
            comp = " "
        else:
            comp=""

        if i == int(len(pixel_array)/2):
            print("\n               ",end="")
        print(comp,pixel_array[i],sep="",end="")
    print("]")
    print("Event:",event)
    print("lastEvent: ",lastEvent)

def render():
    for linha in range(1,altura+1):
        for coluna in range(0,largura):
            pixel_index = ((linha-1)*altura)+coluna

            lp.LedCtrlXYByCode(coluna, linha, pixel_array[pixel_index])

def criaEstruturaDadosPixels(): 
    quantidade_pixels = altura * largura
    for i in range(quantidade_pixels):
        pixel_array.insert(i,1)

def atualizaPixel(event):
    for coluna in range(0,largura):
        for linha in range(1,altura+1):
            pixel_index = coluna + ((linha -1)* largura)
            pass
            # criaPropagacao(pixel_index)

recolorMode = False
def recolor(event):
    global recolorMode
    if event[2] == 127 \
        and event[0] >= 0 and event[0] <= 7\
        and event[1] >= 1 and event[1] <= 8:
        
        x = event[0]
        y = event[1] - 1

        position = x + (y * 8)
        color =  pixel_array[position]

        temp_color_list.append([position,color])
        
        if recolorMode == True:
            
            pixel_array[temp_color_list[0][0]] = temp_color_list[1][1]
            pixel_array[temp_color_list[1][0]] = temp_color_list[0][1]

            recolorMode = False
            temp_color_list.clear()
        else:
            recolorMode = True

def eventChecker(event):
    if lastEvent == [2,0,127] or lastEvent == [3,0,127]:
        lp.LedCtrlXYByCode(lastEvent[0],lastEvent[1],72)
        lp.LedCtrlXYByCode(lastEvent[0],lastEvent[1],0)
        if lastEvent[0] == 2:
            shiftColor(lastEvent,-1)
        else:
            shiftColor(lastEvent,1)



offset = 0
def shiftColor(event,direction):
    global pixel_array,offset
    
    limMin = 0 + offset + direction
    limMax = len(pixel_array) + offset + direction

    if limMin < 0 or limMax > len(color_array):
        limMin = 0 + offset
        limMax = len(pixel_array) + offset
    else:
        pixel_array = color_array[limMin:limMax]
        offset += direction

def criaGridColor():
    for coluna in range(0,largura):
        for linha in range(0,altura):
            pixel_index = coluna + (linha * largura)
            
            pixel_array[pixel_index] = color_array[pixel_index]

def criaFogo():
    for coluna in range(0,largura):
        OverflowPixel = altura * largura
        pixel_index = (OverflowPixel - largura) + coluna

        pixel_array[pixel_index] = 7

def criaPropagacao(pixel_index_atual):
    pixel_de_baixo = pixel_index_atual + largura
    
    if pixel_de_baixo >= largura * altura:
        return
    decay = math.floor(np.random.random()*3)
    fogo_de_baixo = pixel_array[pixel_de_baixo]
    if fogo_de_baixo - decay >=0:
        novo_fogo = fogo_de_baixo - decay
    else:
        novo_fogo = 0

    pixel_array[pixel_index_atual - math.floor(decay*0.3)] = novo_fogo


if __name__ == "__main__":
    lp = lp.LaunchpadMk2()
    # lp.ListAll()
    lp.Open(0,"Mk2")
    start()
    print('\n\nLaunchpad conectado')
