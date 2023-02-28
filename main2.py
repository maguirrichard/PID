import tkinter as tk
from tkinter import *
from tkinter import filedialog as dlg
import cv2
import glob
import numpy as np
import PIL
from PIL import Image, ImageTk
import skimage as sk
from skimage.feature import greycomatrix, greycoprops #funcao do pacote skimage para calcular a matriz GLCM e os atributos da matriz
from skimage.io import imread #importando a funcao imread para leitura da imagem
from random import sample
import time
from skimage.color import rgb2gray #importando funcao rgb2grey que converte a imagem para cinza
from sklearn.metrics.cluster import entropy
from skimage import img_as_uint
import os.path

#Inicialização do programa
root = Tk()
my_menu = Menu(root)

#Configurações da tela
root.config(menu=my_menu)
root.title('Trabalho Prático - PID')
root.geometry('1366x1024') 

#Inicialização do frame1
frame1 = Frame(root, width=1124, height=1024, background='white')
frame1.pack_propagate(0)    
frame1.pack(side="left")

#Inicialização do frame
frame = Frame(root, width=35, height=400)
frame.pack_propagate(0)
frame.pack(side="left")

#Inicialização do frame2
frame2 = Frame(root, width=130, height=130, background='white')
frame2.pack_propagate(0)    
frame2.pack(side="left")

#Declarações e inicialização de variáveis globais
img = 0
fname = ''
canvas = tk.Canvas(frame1, borderwidth=0, highlightthickness=0)
canvas2 = tk.Canvas(frame2, borderwidth=0, highlightthickness=0)
topx, topy= 0, 0
rect_id = None
lista_imagensB1=[]  #lista BIRADS I.
lista_imagensB2=[]  #lista BIRADS II.
lista_imagensB3=[]  #lista BIRADS III.
lista_imagensB4=[]  #lista BIRADS IV.

def our_command():
   pass

def lerDiretorio():
   global lista_imagensB1, lista_imagensB2, lista_imagensB3, lista_imagensB4

   cont = 0

   path1 = "./imagens/1/*.*" #caminho pras pastas 
   path2 = "./imagens/2/*.*" #caminho pras pastas 
   path3 = "./imagens/3/*.*" #caminho pras pastas
   path4 = "./imagens/4/*.*" #caminho pras pastas 

   for arq in glob.glob(path1):   
       print('[' + str(cont) + '] ' + arq)     #printa os caminhos
       b1 = cv2.imread(arq)  #lê cada imagem
       lista_imagensB1.append(b1)  #Cria a lista com as imagens
       cont = cont + 1

   for arq in glob.glob(path2):   
       print('[' + str(cont) + '] ' + arq)     #printa os caminhos
       b2 = cv2.imread(arq)  #le cada imagem
       lista_imagensB2.append(b2)  #Cria a lista com as imagens
       cont = cont + 1

   for arq in glob.glob(path3):   
       print('[' + str(cont) + '] ' + arq)     #printa os caminhos
       b3 = cv2.imread(arq)  #le cada imagem
       lista_imagensB3.append(b3)  #Cria a lista com as imagens
       cont = cont + 1

   for arq in glob.glob(path4):   
       print('[' + str(cont) + '] ' + arq)     #printa os caminhos
       b4 = cv2.imread(arq)  #le cada imagem
       lista_imagensB4.append(b4)  #Cria a lista com as imagens
       cont = cont + 1
        
   #print(lista_imagensB1[99])
   #Visualizar imagens lidas dos diretorios
   c = Canvas(root, height=25, width=190, background="gray")
   c.pack()
   c.create_text(97,15,fill="black",font="Arial 12 bold", text= str(cont) + " imagens foram lidas")
   c.after(7000, lambda: c.destroy())
    
def selecionar():
   #Abre qualquer uma das imagens
   from matplotlib import pyplot as plt
   plt.imshow(lista_imagensB1[99])  
   plt.show()

def abrirImagem():
   global img, fname
   filename = dlg.askopenfilename() #selecionar um arquivo
   fname=filename;
   img = Image.open(filename)
   load = ImageTk.PhotoImage(img)
   canvas.config(width=load.width(), height=load.height())
   canvas.pack(expand=True)
   canvas.img = load
   canvas.create_image(0, 0, image=load, anchor=tk.NW)
   canvas.place(x=0,y=0)
   
def zoom_in():
   global img
   load = ImageTk.PhotoImage(img)
   width = load.width()*1.25
   height = load.height()*1.25
   img = img.resize((int(width), int(height)), Image.ANTIALIAS)
   load = ImageTk.PhotoImage(img)
   canvas.config(width=load.width(), height=load.height())
   canvas.pack(expand=True)
   canvas.img = load
   canvas.create_image(0, 0, image=load, anchor=tk.NW)
   canvas.place(x=0,y=0)

def zoom_out():
   global img
   load = ImageTk.PhotoImage(img)
   width = load.width()*0.75
   height = load.height()*0.75
   img = img.resize((int(width), int(height)), Image.ANTIALIAS)
   load = ImageTk.PhotoImage(img)
   canvas.config(width=load.width(), height=load.height())
   canvas.pack(expand=True)
   canvas.img = load
   canvas.create_image(0, 0, image=load, anchor=tk.NW)
   canvas.place(x=0,y=0)

def redefinir():
   global img, fname
   img = Image.open(fname)
   load = ImageTk.PhotoImage(img)
   canvas.config(width=load.width(), height=load.height())
   canvas.pack(expand=True)
   canvas.img = load
   canvas.create_image(0, 0, image=load, anchor=tk.NW)
   canvas.place(x=0,y=0)

def marcarRegiao():
   global rect_id
   #Cria o retangualo
   rect_id = canvas.create_rectangle(topx, topy, topx, topy, dash=(2,2), fill='', outline='green')
   canvas.bind('<Button-1>', get_mouse_posn)

def get_mouse_posn(event):
   global topy, topx, img
   topx, topy = event.x, event.y
   canvas.coords(rect_id, topx-64, topy-64, topx+64, topy+64)
   crop_rectangle = (topx-64, topy-64, topx+64, topy+64)
   crop_img = img.crop(crop_rectangle)
   load = ImageTk.PhotoImage(crop_img)
   canvas2.config(width=load.width(), height=load.height())
   canvas2.pack(expand=True)
   canvas2.img = load
   canvas2.create_image(0, 0, image=load, anchor=tk.NW)
   canvas2.place(x=1,y=1)
   crop_img = crop_img.save("save.png")
      

def calcular1():
   global fname
   print("Calcular e exibir as características")

   #inicia tempo de exec
   start_time = time.time()

   #image_path = "./imagens/1/p_d_left_cc(108).png" #endereco da imagem
   image = imread(fname) #leitura da imagem
   image_gray = rgb2gray(image) #transformar de RGB para nivel de cinza
   #distancia escolhida entre os pixels para fazer a relação da GLCM é 1
   #print(image_gray)
   props = np.zeros((7)) # vetor para armazenar atributos (no caso o vetor que identifica os dados do usuario)

   
   # Toplevel object which will  
   # be treated as a new window 
   newWindow = Toplevel(root) 
  
   # sets the title of the 
   # Toplevel widget 
   newWindow.title("Características") 
   newWindow.geometry("250x650") 

   for i in range(5):
      matrix = greycomatrix(image_gray,[2**i],[0]) #calculo da matriz em 0 graus
      props[0] = greycoprops(matrix, 'contrast') #calcula constraste
      #print( "Contraste: " + str(props[0]))
      props[1] = greycoprops(matrix, 'dissimilarity') #calcula a dissimilaridade
      #print("Dissimilaridade: " + str(props[1]))
      props[2] = greycoprops(matrix, 'homogeneity') #calcula homogeneidade
      #print("Homogeneidade: " + str(props[2]))
      props[3] = greycoprops(matrix, 'energy') #calcula energia
      #print("Energia: " + str(props[3]))
      props[4] = greycoprops(matrix, 'correlation') #calcula correlacao
      #print( "Correlacao: " + str(props[4]))
      props[5] = greycoprops(matrix, 'ASM') #calcula o segundo momento angular
      #print( "ASM: " + str(props[5]))
      props[6] = entropy(image_gray) #calcula entropia
      #print("Entropia: " + str(props[6]))
      Label(newWindow, 
         text = "Matriz de ocorrência: " + str(2**i) +
         "\nHomogeneidade: " + str("{:.4f}".format(props[2])) +
         "\nEntropia: " + str("{:.4f}".format(props[6])) +
         "\nEnergia: " + str("{:.4f}".format(props[3])) +
         "\nContraste: " + str("{:.4f}".format(props[0]))
         ).pack()

   # Calculate Moments
   moments = cv2.moments(image_gray)

   # Calculate Hu Moments
   huMoments = cv2.HuMoments(moments)
 
   # Log scale hu moments
   for i in range(0,7):
    huMoments[i] = -1* np.copysign(1.0, huMoments[i]) * np.log10(abs(huMoments[i]))

   print("Momentos invariantes de Hu:")
   print(huMoments)
   tempo = time.time() - start_time
   print("--- %s seconds ---" % (tempo))

   Label(newWindow, text = "\nMomentos invariantes Hu\n" + str(huMoments)).pack()
   Label(newWindow,text ="Tempo = "  + str("--- %s segundos ---" % "{:.4f}".format(tempo))).pack()

def calcular2():
   print("Calcular e exibir as características")

   #inicia tempo de exec
   start_time = time.time()

   #image_path = "./imagens/1/p_d_left_cc(108).png" #endereco da imagem
   image = imread("save.png") #leitura da imagem
   image_gray = rgb2gray(image) #transformar de RGB para nivel de cinza
   #distancia escolhida entre os pixels para fazer a relação da GLCM é 1
   #print(image_gray)
   props = np.zeros((7)) # vetor para armazenar atributos (no caso o vetor que identifica os dados do usuario)

   
   # Toplevel object which will  
   # be treated as a new window 
   newWindow = Toplevel(root) 
  
   # sets the title of the 
   # Toplevel widget 
   newWindow.title("Características") 
   newWindow.geometry("250x650") 

   for i in range(5):
      matrix = greycomatrix(image_gray,[2**i],[0]) #calculo da matriz em 0 graus
      props[0] = greycoprops(matrix, 'contrast') #calcula constraste
      #print( "Contraste: " + str(props[0]))
      props[1] = greycoprops(matrix, 'dissimilarity') #calcula a dissimilaridade
      #print("Dissimilaridade: " + str(props[1]))
      props[2] = greycoprops(matrix, 'homogeneity') #calcula homogeneidade
      #print("Homogeneidade: " + str(props[2]))
      props[3] = greycoprops(matrix, 'energy') #calcula energia
      #print("Energia: " + str(props[3]))
      props[4] = greycoprops(matrix, 'correlation') #calcula correlacao
      #print( "Correlacao: " + str(props[4]))
      props[5] = greycoprops(matrix, 'ASM') #calcula o segundo momento angular
      #print( "ASM: " + str(props[5]))
      props[6] = entropy(image_gray) #calcula entropia
      #print("Entropia: " + str(props[6]))
      Label(newWindow, 
         text = "Matriz de ocorrência: " + str(2**i) +
         "\nHomogeneidade: " + str("{:.4f}".format(props[2])) +
         "\nEntropia: " + str("{:.4f}".format(props[6])) +
         "\nEnergia: " + str("{:.4f}".format(props[3])) +
         "\nContraste: " + str("{:.4f}".format(props[0]))
         ).pack()

   # Calculate Moments
   moments = cv2.moments(image_gray)

   # Calculate Hu Moments
   huMoments = cv2.HuMoments(moments)
 
   # Log scale hu moments
   for i in range(0,7):
    huMoments[i] = -1* np.copysign(1.0, huMoments[i]) * np.log10(abs(huMoments[i]))

   print("Momentos invariantes de Hu:")
   print(huMoments)
   tempo = time.time() - start_time
   print("--- %s seconds ---" % (tempo))

   Label(newWindow, text = "\nMomentos invariantes Hu\n" + str(huMoments)).pack()
   Label(newWindow,text ="Tempo = "  + str("--- %s segundos ---" % "{:.4f}".format(tempo))).pack()

def treinar():
   print('calcular')

def classificar():
   print('calcular')

#Menu
arquivo_menu = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label="Arquivo", menu=arquivo_menu)
arquivo_menu.add_command(label="Adicionar Imagem", command=abrirImagem)
arquivo_menu.add_separator()
arquivo_menu.add_command(label="Sair", command=root.quit)

#Visualizacao
visualizacao_menu = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label="Visualização", menu=visualizacao_menu)
visualizacao_menu.add_command(label="Zoom In (25%)", command=zoom_in)
visualizacao_menu.add_command(label="Zoom Out (25%)", command=zoom_out)
visualizacao_menu.add_separator()
visualizacao_menu.add_command(label="Redefinir", command=redefinir)


#Opcoes
opcoes_menu = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label="Opções", menu=opcoes_menu)
opcoes_menu.add_command(label="Ler diretório de imagens", command=lerDiretorio)
opcoes_menu.add_command(label="Treinar 75%", command=treinar)
opcoes_menu.add_command(label="Classificar 25%", command=our_command)
opcoes_menu.add_command(label="Marcar a região de interesse", command=marcarRegiao)
opcoes_menu.add_command(label="Caracterizar imagem completa", command=calcular1)
opcoes_menu.add_command(label="Caracterizar área selecionada", command=calcular2)
opcoes_menu.add_command(label="Calcular e exibir as características", command=our_command)

root.mainloop()
