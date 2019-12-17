import launchpad_py as lp 
import os
import threading
import time
import numpy as np
import math


eixoX = [0,1,2,3,4,5,6,7]
eixoY = [1,2,3,4,5,6,7,8]
cor = [ 0, 7, 121, 5, 9, 13, 109, 3]
pixel_array = []
color_array = np.arange(128).tolist()
temp_color_list=[]
altura = 8
largura = 8

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
    while True:
        event = eventUpdate()
        colorChanger(event)
        atualizaPixel(event)
        print("temp_color_list: ",temp_color_list)
        time.sleep(0.01)
    # set_interval(atualizaPixel(),1)

# def set_interval(func, sec):
#     e = threading.Event()
#     while not e.wait(sec):
#         func()
def eventUpdate():
    event = lp.ButtonStateXY()
    print("Event:",end=" ")
    if event:
        print(event)
        return event
    else:
        print(event)
        event=[-1,-1,-1]
        return event
        # if pixel_array[0]+1 > 127:
        #     pixel_array[0]=0
        # else: 

        #     pixel_array[0]+=1

def printaDados():
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
    print("\n\n Array: ",pixel_array)

def render():

    # lp.LedAllOn(0)
    for linha in range(0,altura):
        for coluna in range(0,largura):
            pixel_index = (linha*altura)+coluna
            # print("eixoX[coluna]: %d" % (eixoX[coluna]))
            # print("eixoY[linha]: %d" % (eixoY[linha]))
            # print("pixel_array[pixel_index]: %d" % (pixel_array[pixel_index]))
            lp.LedCtrlXYByCode(eixoX[coluna],eixoY[linha],pixel_array[pixel_index])

def criaEstruturaDadosPixels():
    quantidade_pixels = altura * largura
    for i in range(quantidade_pixels):
        pixel_array.insert(i,1)

def criaFogo():
    for coluna in range(0,largura):
        OverflowPixel = altura * largura
        pixel_index = (OverflowPixel - largura) + coluna

        pixel_array[pixel_index] = 7

def atualizaPixel(event):
    offset = colorShifter(event)

    if not offset:
        offset=0

    for coluna in range(0,largura):
        for linha in range(0,altura):
            pixel_index = coluna + (linha * largura)
            
            # pixel_array[pixel_index] = color_array[pixel_index+offset]
            # criaPropagacao(pixel_index)
    printaDados()
    render()

recolorMode = False
def colorChanger(event):
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
            print("TRUE")
            
            pixel_array[temp_color_list[0][0]] = temp_color_list[1][1]
            pixel_array[temp_color_list[1][0]] = temp_color_list[0][1]

            recolorMode = False
            temp_color_list.clear()
        else:
            recolorMode = True

def colorShifter(event):
    ##### REFAZER ####
    """


    """
    if event == [3,0,127]:
        lp.LedCtrlXYByCode(3,0,72)
        lp.LedCtrlXYByCode(3,0,0)
        #Se o ultimo led ta dentro do limite de cor
        if pixel_array[63] < 127:
            return 1
        else:
            return 0

    if event == [2,0,127]:
        lp.LedCtrlXYByCode(2,0,72)
        lp.LedCtrlXYByCode(2,0,0)
        #Se o primeiro led ta dentro do limite de cor
        if pixel_array[0] > 0:
            return -1
        else:
            return 0

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

def criaGridColor():
    for coluna in range(0,largura):
        for linha in range(0,altura):
            pixel_index = coluna + (linha * largura)
            
            pixel_array[pixel_index] = color_array[pixel_index]
            

lp = lp.LaunchpadMk2()
# lp.ListAll()
lp.Open(0,"Mk2")
start()
print('\n\nLaunchpad conectado')
# except Exception as exc:
#     print('Launchpad não conectado')
#     print(exc)
# position = []
# for x in range()