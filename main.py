import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# Variables globales para la rotación, el radio y la transformación
angle_y = 0
rotating = False
selected_figure = None  # Inicialmente, no se selecciona ninguna figura
radius = 1.0  # Valor predeterminado del radio
transformation_type = None  # Tipo de transformación seleccionada (reflejar o proyectar)
transformation_axis = None  # Eje seleccionado para la transformación

# Límites para el radio
MIN_RADIUS = 2
MAX_RADIUS = 50

# Función para rotación (transformación lineal)
def rotate(vertices, angle_y):
    rotation_y = np.array([[np.cos(angle_y), 0, np.sin(angle_y)],
                           [0, 1, 0],
                           [-np.sin(angle_y), 0, np.cos(angle_y)]])
    
    rotated_vertices = np.dot(vertices, rotation_y)
    return rotated_vertices

# Función para reflexión (transformación lineal)
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

# Función para proyección (sobre un eje)
def project(vertices, axis):
    if axis == 'X':
        projection_matrix = np.array([[1, 0, 0], [0, 0, 0], [0, 0, 0]])
    elif axis == 'Y':
        projection_matrix = np.array([[0, 0, 0], [0, 1, 0], [0, 0, 0]])
    elif axis == 'Z':
        projection_matrix = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 1]])
    else:
        return vertices  # No se aplica proyección si no se selecciona eje

    projected_vertices = np.dot(vertices, projection_matrix)
    return projected_vertices

# Función para calcular el complemento (diferencia entre el original y la proyección)
def compute_complement(vertices, projection):
    complement = vertices - projection
    return complement

# Configuración de la figura 3D
fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111, projection='3d')

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

# Función para actualizar la visualización de la gráfica
def update_plot():
    global transformation_axis, transformation_type
    ax.cla()  # Limpiar el eje

    # Establecer fondo personalizado en blanco
    ax.set_facecolor('white')  # Fondo blanco

    # Propiedades personalizadas de la cuadrícula y los ejes
    ax.grid(True, color='gray', linestyle='--', linewidth=0.5)
    ax.xaxis.pane.fill = False  # Ocultar los paneles para un mejor efecto visual
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False
    ax.xaxis.line.set_color("black")
    ax.yaxis.line.set_color("black")
    ax.zaxis.line.set_color("black")
    ax.set_xlabel('Eje X', fontsize=10, color='black')
    ax.set_ylabel('Eje Y', fontsize=10, color='black')
    ax.set_zlabel('Eje Z', fontsize=10, color='black')
    ax.set_xlim([-10, 10])
    ax.set_ylim([-10, 10])
    ax.set_zlim([-10, 10])

    # Definir colores únicos para cada tipo de reflexión y proyección
    colors = {
        'Reflect X': '#FF6347',  # Rojo tomate
        'Reflect Y': '#4682B4',  # Azul acero
        'Reflect Z': '#32CD32',  # Verde lima
        'Project X': '#FFD700',  # Oro
        'Project Y': '#8A2BE2',  # Violeta
        'Project Z': '#FF69B4'   # Rosa fuerte
    }

    if selected_figure == "Esfera":
        x, y, z = create_sphere(radius)
        vertices = np.array([x.flatten(), y.flatten(), z.flatten()]).T
        rotated_vertices = rotate(vertices, np.radians(angle_y))

        if transformation_type and transformation_axis:
            key = f"{transformation_type} {transformation_axis}"
            if "Reflect" in transformation_type:
                rotated_vertices = reflect(rotated_vertices, transformation_axis)
                ax.plot_surface(rotated_vertices[:, 0].reshape(x.shape), 
                                rotated_vertices[:, 1].reshape(y.shape), 
                                rotated_vertices[:, 2].reshape(z.shape), 
                                color=colors[key], alpha=0.8)
            elif "Project" in transformation_type:
                projected_vertices = project(rotated_vertices, transformation_axis)
                complement_vertices = compute_complement(rotated_vertices, projected_vertices)
                # Graficar la proyección
                ax.plot_surface(projected_vertices[:, 0].reshape(x.shape), 
                                projected_vertices[:, 1].reshape(y.shape), 
                                projected_vertices[:, 2].reshape(z.shape), 
                                color=colors[key], alpha=0.6)
                # Graficar el complemento
                ax.plot_surface(complement_vertices[:, 0].reshape(x.shape), 
                                complement_vertices[:, 1].reshape(y.shape), 
                                complement_vertices[:, 2].reshape(z.shape), 
                                color='#20B2AA', alpha=0.6)

        rotated_x, rotated_y, rotated_z = rotated_vertices.T
        ax.plot_surface(rotated_x.reshape(x.shape), rotated_y.reshape(y.shape), rotated_z.reshape(z.shape), color='#00BFFF')  # Azul agua

    elif selected_figure == "Cilindro":
        x, y, z = create_cylinder(radius)
        vertices = np.array([x.flatten(), y.flatten(), z.flatten()]).T
        rotated_vertices = rotate(vertices, np.radians(angle_y))

        if transformation_type and transformation_axis:
            key = f"{transformation_type} {transformation_axis}"
            if "Reflect" in transformation_type:
                rotated_vertices = reflect(rotated_vertices, transformation_axis)
                ax.plot_surface(rotated_vertices[:, 0].reshape(x.shape), 
                                rotated_vertices[:, 1].reshape(y.shape), 
                                rotated_vertices[:, 2].reshape(z.shape), 
                                color=colors[key], alpha=0.8)
            elif "Project" in transformation_type:
                projected_vertices = project(rotated_vertices, transformation_axis)
                complement_vertices = compute_complement(rotated_vertices, projected_vertices)
                # Graficar la proyección
                ax.plot_surface(projected_vertices[:, 0].reshape(x.shape), 
                                projected_vertices[:, 1].reshape(y.shape), 
                                proyectados[:, 2].reshape(z.shape), 
                                color=colors[key], alpha=0.6)
                # Graficar el complemento
                ax.plot_surface(complement_vertices[:, 0].reshape(x.shape), 
                                complement_vertices[:, 1].reshape(y.shape), 
                                complement_vertices[:, 2].reshape(z.shape), 
                                color='#20B2AA', alpha=0.6)

        rotated_x, rotated_y, rotated_z = rotated_vertices.T
        ax.plot_surface(rotated_x.reshape(x.shape), rotated_y.reshape(y.shape), rotated_z.reshape(z.shape), color='#00BFFF')  # Azul agua

    # Agregar anotaciones para indicar el eje y el tipo de transformación
    if transformation_axis:
        ax.text(0, 0, 0, f'{transformation_type} en {transformation_axis}', color=colors[key], fontsize=12)

    canvas.draw()

# Configuración de la interfaz de usuario de Tkinter
root = tk.Tk()
root.title("Interfaz de Transformaciones Lineales y Rotación 3D")

# Establecer el tamaño de la ventana para que sea más grande
root.geometry("1200x800")

# Caja horizontal principal (HBox) para contener los paneles izquierdo y derecho
main_hbox = tk.Frame(root, bg='white')
main_hbox.pack(fill=tk.BOTH, expand=True)

# VBox izquierda para los controles
left_vbox = tk.Frame(main_hbox, bg='white', width=200)
left_vbox.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

# VBox derecha para la gráfica 3D
right_vbox = tk.Frame(main_hbox, bg='white')
right_vbox.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

# Lienzo de Matplotlib en la VBox derecha
canvas = FigureCanvasTkAgg(fig, master=right_vbox)
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# Combobox para seleccionar la figura en la VBox izquierda
def on_select_figure(event):
    global selected_figure, angle_y
    selected_figure = combo_box_figure.get()
    angle_y = 0  # Restablecer la rotación al cambiar de figura
    combo_box_figure.config(state='disabled')  # Desactivar el combobox después de la selección

combo_box_figure = ttk.Combobox(left_vbox, values=["Esfera", "Cilindro"])
combo_box_figure.set("Seleccionar figura")
combo_box_figure.bind("<<ComboboxSelected>>", on_select_figure)
combo_box_figure.pack(pady=10)

# Combobox para seleccionar la transformación (reflejar o proyectar)
def on_select_transformation(event):
    global transformation_axis, transformation_type
    selected_option = combo_box_transformation.get()
    if "Reflect" in selected_option:
        transformation_type = "Reflect"
        transformation_axis = selected_option.split()[-1]
    elif "Project" in selected_option:
        transformation_type = "Project"
        transformation_axis = selected_option.split()[-1]
    combo_box_transformation.config(state='disabled')  # Desactivar el combobox después de la selección

combo_box_transformation = ttk.Combobox(left_vbox, values=[
    "Reflect X", "Reflect Y", "Reflect Z", 
    "Project X", "Project Y", "Project Z"
])
combo_box_transformation.set("Seleccionar transformación")
combo_box_transformation.bind("<<ComboboxSelected>>", on_select_transformation)
combo_box_transformation.pack(pady=10)

# Campo de entrada para el radio
tk.Label(left_vbox, text="Radio:", bg='white').pack(pady=5)
entry_radius = tk.Entry(left_vbox)
entry_radius.pack(pady=5)

# Funciones de control para los botones
def start_rotation():
    global rotating, angle_y, radius
    try:
        radius = float(entry_radius.get())
        if radius < MIN_RADIUS or radius > MAX_RADIUS:
            raise ValueError(f"El radio debe estar entre {MIN_RADIUS} y {MAX_RADIUS}")
        rotating = True
        rotate_continuously()
    except ValueError as e:
        messagebox.showwarning("Advertencia", str(e))

def rotate_continuously():
    global angle_y, rotating
    if rotating:
        angle_y += 1  # Incrementar ángulo para rotación continua
        update_plot()
        root.after(50, rotate_continuously)  # Llamar a la función cada 50ms para rotación suave

def stop_rotation():
    global rotating
    rotating = False

def clear_rotation():
    global rotating, selected_figure, transformation_axis, transformation_type
    rotating = False
    selected_figure = None  # No se selecciona ninguna figura
    transformation_axis = None  # No se selecciona ningún eje
    transformation_type = None  # No se selecciona ninguna transformación
    combo_box_figure.set("Seleccionar figura")  # Restablecer el combobox de la figura
    combo_box_figure.config(state='normal')  # Rehabilitar el combobox
    combo_box_transformation.set("Seleccionar transformación")  # Restablecer el combobox de la transformación
    combo_box_transformation.config(state='normal')  # Rehabilitar el combobox
    entry_radius.delete(0, tk.END)  # Borrar entrada del radio
    ax.cla()  # Limpiar gráfica
    ax.set_facecolor('white')  # Restablecer el color de fondo
    canvas.draw()

# Botones con colores específicos y tamaño consistente
button_width = 15  # Ancho consistente para los botones
btn_rotate = tk.Button(left_vbox, text="Rotar", command=start_rotation, bg='green', fg='white', width=button_width)
btn_rotate.pack(pady=10)

btn_stop = tk.Button(left_vbox, text="Detener", command=stop_rotation, bg='red', fg='white', width=button_width)
btn_stop.pack(pady=10)

btn_clear = tk.Button(left_vbox, text="Limpiar", command=clear_rotation, bg='purple', fg='white', width=button_width)
btn_clear.pack(pady=10)

# Función para iniciar la interfaz de usuario
def start_interface():
    canvas.draw()  # Iniciar sin ninguna figura
    root.mainloop()

# Iniciar la interfaz
start_interface()
