import tkinter as tk
from array import *

#taille du carré et nb de carré par côté
rect_size=10
nb = 50

root = tk.Tk()
root.title("grille")

#création du canevas
canvas = tk.Canvas(root, width=nb*rect_size, height=nb*rect_size, bg='white')

#création de tableau grid[] à deux dimensions
grid = []

#boucle de création des carrés pour remplir le canevas ->grille
#en plus on stoque chaque carré dans grid[] (grid[j,i] = carré à la coordonnée j,i)
for j in range(nb):
    column = []
    for i in range(nb):
        column.append(canvas.create_rectangle(j*rect_size, i*rect_size, (j+1)*rect_size, (i+1)*rect_size, fill='white'))
    grid.append(column)


#active le carré = couleur bleue
def cell_on(x,y):
    canvas.itemconfig(grid[x][y] , fill='blue')

#active si blanc - desactive si bleu
def cell_on_off(x,y):
    #test selon la propriété tk de couleur du rectangle
    couleur = canvas.itemcget(grid[x][y],'fill');
    if (couleur == 'blue'):
        cell_off(x,y)
    else:
        cell_on(x,y)   

#désactive le carré couleur blanche
def cell_off(x,y):
    canvas.itemconfig(grid[x][y] , fill='white')

#click dans la grille
def cell_click(event):
    widget = event.widget   
    # Convert screen coordinates to canvas coordinates
    xc = widget.canvasx(event.x) - rect_size
    yc = widget.canvasx(event.y) - rect_size
    # on calcule l'indice de la cellule à partir de la position de souris xc, yc
    # et on acticve le carré (cell)
    cell_on_off(int(xc/rect_size)+1, int(yc/rect_size)+1)

# liaison click soursi avec la fonction cell_click
canvas.bind("<Button-1>", cell_click)
canvas.pack()

# activation de certain carrés au départ  
cell_on(3,4)
cell_on(4,4)
cell_on(2,3)
cell_off(2,3)
cell_on(20,3)

root.mainloop()
