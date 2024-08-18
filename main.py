import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# Variables globales para la rotación, radio, y reflejo
angle_y = 0
rotating = False
selected_figure = None  # Inicialmente ninguna figura está seleccionada
radius = 1.0  # Valor por defecto del radio
reflection_axis = None  # Eje de reflexión seleccionado

# Límites para el radio
MIN_RADIUS = 0.1
MAX_RADIUS = 1.5

# Función para rotar la figura
def rotate(vertices, angle_y):
    rotation_y = np.array([[np.cos(angle_y), 0, np.sin(angle_y)],
                           [0, 1, 0],
                           [-np.sin(angle_y), 0, np.cos(angle_y)]])
    
    rotated_vertices = np.dot(vertices, rotation_y)
    return rotated_vertices

# Función para reflejar la figura
def reflect(vertices, axis):
    reflection_matrix = {
        'X': np.array([[-1, 0, 0], [0, 1, 0], [0, 0, 1]]),
        'Y': np.array([[1, 0, 0], [0, -1, 0], [0, 0, 1]]),
        'Z': np.array([[1, 0, 0], [0, 1, 0], [0, 0, -1]])
    }
    if axis in reflection_matrix:
        reflected_vertices = np.dot(vertices, reflection_matrix[axis])
        return reflected_vertices
    return vertices

# Configuración de la figura 3D
fig = plt.figure(figsize=(5, 5))
ax = fig.add_subplot(111, projection='3d')
ax.set_facecolor('white')  # Amarillo pastel para todo el fondo

# Función para crear una esfera
def create_sphere(radius):
    u = np.linspace(0, 2 * np.pi, 100)
    v = np.linspace(0, np.pi, 100)
    x = radius * np.outer(np.cos(u), np.sin(v))
    y = radius * np.outer(np.sin(u), np.sin(v))
    z = radius * np.outer(np.ones(np.size(u)), np.cos(v))
    return np.array([x, y, z])

# Función para crear un cilindro
def create_cylinder(radius, height=2):
    z = np.linspace(-height/2, height/2, 100)
    theta = np.linspace(0, 2. * np.pi, 100)
    theta_grid, z_grid = np.meshgrid(theta, z)
    x_grid = radius * np.cos(theta_grid)
    y_grid = radius * np.sin(theta_grid)
    return np.array([x_grid, y_grid, z_grid])

# Función para actualizar la visualización
def update_plot():
    ax.cla()  # Limpiar el eje
    ax.set_xlim([-2, 2])
    ax.set_ylim([-2, 2])
    ax.set_zlim([-2, 2])
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_facecolor('white')  

    if selected_figure == "Esfera":
        x, y, z = create_sphere(radius)
        vertices = np.array([x.flatten(), y.flatten(), z.flatten()]).T
        rotated_vertices = rotate(vertices, np.radians(angle_y))
        if reflection_axis:
            rotated_vertices = reflect(rotated_vertices, reflection_axis)
        rotated_x, rotated_y, rotated_z = rotated_vertices.T
        ax.plot_surface(rotated_x.reshape(x.shape), rotated_y.reshape(y.shape), rotated_z.reshape(z.shape), color='#00BFFF')  # Azul agua
    elif selected_figure == "Cilindro":
        x, y, z = create_cylinder(radius)
        vertices = np.array([x.flatten(), y.flatten(), z.flatten()]).T
        rotated_vertices = rotate(vertices, np.radians(angle_y))
        if reflection_axis:
            rotated_vertices = reflect(rotated_vertices, reflection_axis)
        rotated_x, rotated_y, rotated_z = rotated_vertices.T
        ax.plot_surface(rotated_x.reshape(x.shape), rotated_y.reshape(y.shape), rotated_z.reshape(z.shape), color='#00BFFF')  # Azul agua

    canvas.draw()

# Configuración de la interfaz de usuario con Tkinter
root = tk.Tk()
root.title("Interfaz de Usuario y Rotación 3D")

# Crear un Frame principal para todos los elementos
main_frame = tk.Frame(root, bg='white')
main_frame.pack(fill=tk.BOTH, expand=True)

# Frame izquierdo (Ingreso de valores y botones)
left_frame = tk.Frame(main_frame, width=200, bg='white')
left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

# Frame derecho (Visualización 3D)
right_frame = tk.Frame(main_frame, width=400, bg='white')  
right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

# Colocar la visualización de matplotlib en el frame derecho
canvas = FigureCanvasTkAgg(fig, master=right_frame)
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# Combobox para seleccionar la figura
def on_select_figure(event):
    global selected_figure, angle_y
    selected_figure = combo_box_figure.get()
    angle_y = 0  # Reiniciar la rotación al cambiar de figura

combo_box_figure = ttk.Combobox(left_frame, values=["Esfera", "Cilindro"])
combo_box_figure.set("Selecciona una figura")
combo_box_figure.bind("<<ComboboxSelected>>", on_select_figure)
combo_box_figure.pack(pady=10)

# Combobox para seleccionar el eje de reflexión
def on_select_reflection(event):
    global reflection_axis
    reflection_axis = combo_box_reflection.get()

combo_box_reflection = ttk.Combobox(left_frame, values=["X", "Y", "Z"])
combo_box_reflection.set("Reflejar en eje")
combo_box_reflection.bind("<<ComboboxSelected>>", on_select_reflection)
combo_box_reflection.pack(pady=10)

# Campo de texto para el radio
tk.Label(left_frame, text="Radio:", bg='white').pack(pady=5)
entry_radius = tk.Entry(left_frame)
entry_radius.pack(pady=5)

# Funciones de control para los botones
def start_rotation():
    global rotating, angle_y, radius
    try:
        radius = float(entry_radius.get())
        if radius < MIN_RADIUS or radius > MAX_RADIUS:
            raise ValueError("Valor muy grande")
        rotating = True
        rotate_continuously()
    except ValueError as e:
        messagebox.showwarning("Advertencia", f"Valor de radio no válido: {e}")

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
    global rotating, selected_figure, reflection_axis
    rotating = False
    selected_figure = None  # Ninguna figura seleccionada
    reflection_axis = None  # Ningún eje seleccionado
    combo_box_figure.set("Selecciona una figura")  # Resetear el ComboBox de figuras
    combo_box_reflection.set("Reflejar en eje")  # Resetear el ComboBox de reflexión
    entry_radius.delete(0, tk.END)  # Limpiar el campo de texto del radio
    ax.cla()  # Limpiar el plano
    ax.set_facecolor('#FFFACD')  # Mantener el fondo amarillo pastel
    canvas.draw()

# Botones con colores específicos y tamaño consistente
button_width = 15  # Ancho consistente para todos los botones
btn_rotate = tk.Button(left_frame, text="Rotar", command=start_rotation, bg='green', fg='white', width=button_width)
btn_rotate.pack(pady=10)

btn_stop = tk.Button(left_frame, text="Detener", command=stop_rotation, bg='red', fg='white', width=button_width)
btn_stop.pack(pady=10)

btn_clear = tk.Button(left_frame, text="Limpiar", command=clear_rotation, bg='purple', fg='white', width=button_width)
btn_clear.pack(pady=10)

# Función para iniciar la interfaz de usuario
def start_interface():
    canvas.draw()  # Iniciar sin ninguna figura
    root.mainloop()

# Iniciar la interfaz
start_interface()
