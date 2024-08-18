import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk

# Variables globales para la rotación
angle_y = 0
rotating = False

# Función para rotar la pirámide
def rotate(vertices, angle_y):
    rotation_y = np.array([[np.cos(angle_y), 0, np.sin(angle_y)],
                           [0, 1, 0],
                           [-np.sin(angle_y), 0, np.cos(angle_y)]])
    
    rotated_vertices = np.dot(vertices, rotation_y)
    return rotated_vertices

# Configuración de la figura 3D
fig = plt.figure(figsize=(5, 5))
ax = fig.add_subplot(111, projection='3d')

# Dibujar el plano tridimensional sin puntos
ax.set_xlim([-2, 2])
ax.set_ylim([-2, 2])
ax.set_zlim([-2, 2])

# Configurar las etiquetas de los ejes
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# Definir los vértices de una pirámide
vertices = np.array([[0, 1, 0],   # Vértice superior
                     [-1, -1, -1],  # Base inferior izquierda
                     [1, -1, -1],   # Base inferior derecha
                     [1, -1, 1],    # Base superior derecha
                     [-1, -1, 1]])  # Base superior izquierda

# Definir las aristas de la pirámide
edges = [(0, 1), (0, 2), (0, 3), (0, 4),
         (1, 2), (2, 3), (3, 4), (4, 1)]

# Función para actualizar la visualización
def update_plot():
    ax.cla()  # Limpiar el eje
    ax.set_xlim([-2, 2])
    ax.set_ylim([-2, 2])
    ax.set_zlim([-2, 2])
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    # Rotar la figura según el ángulo en el eje Y
    rotated_vertices = rotate(vertices, np.radians(angle_y))

    # Dibujar la pirámide
    for edge in edges:
        start = rotated_vertices[edge[0]]
        end = rotated_vertices[edge[1]]
        ax.plot3D([start[0], end[0]], [start[1], end[1]], [start[2], end[2]], color='black')

    canvas.draw()

# Configuración de la interfaz de usuario con Tkinter
root = tk.Tk()
root.title("Interfaz de Usuario y Rotación 3D")

# Crear un Frame para el "HBox" (división izquierda y derecha)
main_frame = ttk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=True)

# Frame izquierdo (Ingreso de valores y botones)
left_frame = ttk.Frame(main_frame, width=200)
left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

# Frame derecho (Visualización 3D)
right_frame = ttk.Frame(main_frame, width=400)
right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

# Colocar la visualización de matplotlib en el frame derecho
canvas = FigureCanvasTkAgg(fig, master=right_frame)
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# Funciones de control para los botones
def start_rotation():
    global rotating, angle_y
    rotating = True
    rotate_continuously()

def rotate_continuously():
    global angle_y, rotating
    if rotating:
        angle_y += 1  # Incrementar el ángulo para la rotación continua
        update_plot()
        root.after(50, rotate_continuously)  # Llamar a la función cada 50ms para una rotación suave

def stop_rotation():
    global rotating
    rotating = False

def clear_rotation():
    global angle_y
    angle_y = 0
    update_plot()

# Ingresos de valores y botones en el frame izquierdo
btn_rotate = ttk.Button(left_frame, text="Rotar", command=start_rotation)
btn_rotate.pack(pady=10)

btn_stop = ttk.Button(left_frame, text="Detener", command=stop_rotation)
btn_stop.pack(pady=10)

btn_clear = ttk.Button(left_frame, text="Limpiar", command=clear_rotation)
btn_clear.pack(pady=10)

# Función para iniciar la interfaz de usuario
def start_interface():
    update_plot()  # Dibujar la figura inicial
    root.mainloop()

# Iniciar la interfaz
start_interface()


