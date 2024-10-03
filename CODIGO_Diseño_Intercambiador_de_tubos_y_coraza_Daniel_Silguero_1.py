#Codigo para el Diseño de un intercambiador de Calor de tubos y coraza:
#PROPIETARIO: Daniel Silguero Iregui / Transferencia de calor II / 7mo Semestre/ Ing. Química / Universidad del Atlantico

#-------------------------------------------------------------------------------------------------------------------------------------------------

#Sistema de unidades a utilizar: Sistema Ingles:

#-------------------------------------------------------------------------------------------------------------------------------------------------

#Importación de librerías a utilizar:

import math
import tkinter as tk
from tkinter import ttk
from tabulate import tabulate
from colorama import Fore, Style, init
from sympy import symbols, Eq, nsolve, log, re
import itertools
import flet as ft
#-------------------------------------------------------------------------------------------------------------------------------------------------

""" 
    DATOS PROBLEMA DANIEL SILGUERO: SISTEMA TETRACLORURO DE CARBONO - AGUA:
    
    SUSTANCIA CALIENTE: CCl4

    mCCl4= 53837.504   lb/h
    T_entrada= 196.61  °F
    T_salida= 173.21   °F

    SUSTANCIA FRIA: H2O

    T_entrada= 78.71   °F
    T_salida= 106.25   °F

"""

#-------------------------------------------------------------------------------------------------------------------------------------------------



def main(page: ft.Page):

    # Variable para almacenar el nombre
    nombre_usuario = ""
    # Variables para almacenar las sustancias seleccionadas
    Sustancia_Caliente_Seleccionada = ""
    Sustancia_Fria_Seleccionada = ""
    Flujo_másico_Caliente= None
    Flujo_másico_Frio= None
    Temp_Entrada_Caliente= None
    Temp_Salida_Caliente= None
    Temp_Entrada_Frio= None
    Temp_Salida_Frio=None
    siguiente_button = None  # Inicializamos el botón como None
    IniciarCodigo_Botón= None
    IniciarCodigo_Botón2= None
    progress_ring = ft.ProgressRing(visible=False)
    P_input_Coraza_1=0
    P_input_Coraza_2=0
    P_input_Tubos_1=0
    P_input_Tubos_2=0
    Min_efectividad=0

    def Actualización_sustancia_caliente(value):
        nonlocal Sustancia_Caliente_Seleccionada
        Sustancia_Caliente_Seleccionada = value
        Actualizar_boton_siguiente()  # Verificar si debe mostrarse el botón

    def Actualización_sustancia_fria(value):
        nonlocal Sustancia_Fria_Seleccionada
        Sustancia_Fria_Seleccionada = value
        Actualizar_boton_siguiente()  # Verificar si debe mostrarse el botón

    def Actualizar_boton_siguiente():
        nonlocal siguiente_button
        if Sustancia_Caliente_Seleccionada and Sustancia_Fria_Seleccionada:
            # Si ya hay selección de ambas sustancias, mostramos el botón
            if siguiente_button is None:
                siguiente_button = ft.ElevatedButton(text="Siguiente", on_click=cambiar_interfaz_3)
                page.add(siguiente_button)
                page.update()
        else:
            # Si no hay selección, ocultamos el botón
            if siguiente_button is not None:
                page.controls.remove(siguiente_button)
                siguiente_button = None

    # Configuramos la página principal
    page.title = "Bienvenid@ a la App de diseño de intercambiadores de calor de tubo y coraza"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER  # Centrar contenido verticalmente
    
    # Creamos un texto de bienvenida
    welcome_text = ft.Text(
        "¡Bienvenido a la aplicación de diseño de intercambiadores de calor de tubo y coraza!",
        size=30,
        weight=ft.FontWeight.BOLD,
        color=ft.colors.BLUE,
    )
    
    def cambiar_interfaz_1(e):
        # Limpiar la pantalla
        page.controls.clear()
        Nombre_Usuario= ft.TextField(label="Introduce tu nombre ingeniero:", autofocus=True)

        # Crear nuevos elementos para la nueva pantalla
        page.add(
            ft.Text("DISEÑO DE INTERCAMBIADOR DE CALOR DE TUBO Y CORAZA", size=30),
            Nombre_Usuario,
            ft.ElevatedButton(text="Enviar", on_click=lambda e: (enviar_nombre(Nombre_Usuario.value), cambiar_interfaz_2(e)))
        )

        # Actualizar la página para reflejar los cambios
        page.update()


    def enviar_nombre(Nombre):
        nonlocal nombre_usuario  # Permite modificar la variable externa
        nombre_usuario = Nombre
        page.update()

    def cambiar_interfaz_2(e):
        # Limpiar la pantalla
        page.controls.clear()

        nonlocal nombre_usuario
        nonlocal Sustancia_Caliente_Seleccionada
        nonlocal Sustancia_Fria_Seleccionada
        nonlocal siguiente_button
        siguiente_button =None

        # Listas de sustancias (ejemplo)
        Lista_Sustancias_1 = ["Agua", "Tetracloruro de Carbono","Kerosene","Acido acético 5%","Etilenglicol","Acido nitrico 70%"]
        Lista_Sustancias_2 = ["Agua", "Tetracloruro de Carbono","Kerosene","Acido acético 5%","Etilenglicol","Acido nitrico 70%"]

        page.add(
            ft.Text("DISEÑO DE INTERCAMBIADOR DE CALOR DE TUBO Y CORAZA", size=30),
            ft.Text(f"Hola, {nombre_usuario}!", size=30),
            ft.Text("Selecciona las sustancias a utilizar", size=24),

            # Selector para la sustancia caliente
            ft.Text("Selecciona la sustancia caliente:"),
            ft.Dropdown(
            options=[ft.dropdown.Option(sustancia) for sustancia in Lista_Sustancias_1],
            on_change=lambda e: Actualización_sustancia_caliente(e.control.value)
            ),

        # Selector para la sustancia fría
            ft.Text("Selecciona la sustancia fría:"),
            ft.Dropdown(
            options=[ft.dropdown.Option(sustancia) for sustancia in Lista_Sustancias_2],
            on_change=lambda e: Actualización_sustancia_fria(e.control.value)
            ),
        )
        page.update()

    def cambiar_interfaz_3(e):
         # Limpiar la pantalla
        page.controls.clear()

        nonlocal Flujo_másico_Caliente,Temp_Entrada_Caliente,Temp_Salida_Caliente,Temp_Entrada_Frio,Temp_Salida_Frio, IniciarCodigo_Botón
        IniciarCodigo_Botón =None
        sustancia_caliente_container = ft.Container(
            content=ft.Column([
                ft.Text("SUSTANCIA CALIENTE", size=28, color="black"),
                Flujo_másico_Caliente := ft.TextField(label="Flujo másico en lb/h",text_style=ft.TextStyle(color="black"),border_color="black",label_style=ft.TextStyle(color="black"), on_change=lambda e: actualizar_boton_iniciar()),
                Temp_Entrada_Caliente := ft.TextField(label="Temperatura de entrada en Fahrenheit",text_style=ft.TextStyle(color="black"),border_color="black",label_style=ft.TextStyle(color="black"), on_change=lambda e: actualizar_boton_iniciar()),
                Temp_Salida_Caliente := ft.TextField(label="Temperatura de salida en Fahrenheit",text_style=ft.TextStyle(color="black"),border_color="black",label_style=ft.TextStyle(color="black"), on_change=lambda e: actualizar_boton_iniciar()),
            ]),
            alignment=ft.alignment.center_left, # Alineado a la izquierda
            padding=ft.padding.all(10), # Espaciado interno (padding)
            bgcolor=ft.colors.ORANGE_300, # Color de fondo
            border_radius=10, # Bordes redondeados
            width=400  # Ancho del contenedor
        )

    # Contenedor de sustancia fría
        sustancia_fria_container = ft.Container(
            content=ft.Column([
                ft.Text("SUSTANCIA FRIA", size=28, color="black"),
                Temp_Entrada_Frio := ft.TextField(label="Temperatura de entrada en Fahrenheit",text_style=ft.TextStyle(color="black"),border_color="black",label_style=ft.TextStyle(color="black"), on_change=lambda e: actualizar_boton_iniciar()),
                Temp_Salida_Frio := ft.TextField(label="Temperatura de salida en Fahrenheit",text_style=ft.TextStyle(color="black"),border_color="black",label_style=ft.TextStyle(color="black"), on_change=lambda e: actualizar_boton_iniciar()),
            ]),
            alignment=ft.alignment.center_right, # Alineado a la derecha
            padding=ft.padding.all(10), # Espaciado interno
            bgcolor=ft.colors.CYAN_300, # Color de fondo
            border_radius=10, # Bordes redondeados
            width=400  # Ancho del contenedor
        )

    # Fila que contiene ambos contenedores
        fila = ft.Row(
            controls=[sustancia_caliente_container, sustancia_fria_container],
            alignment=ft.MainAxisAlignment.SPACE_AROUND,  # Alinea ambos contenedores con espacio alrededor
        )
        # Mostrar los campos de entrada para el fluido caliente y frío
        page.add(fila)
        page.update()

        def actualizar_boton_iniciar():
            nonlocal IniciarCodigo_Botón
            if (Flujo_másico_Caliente.value and Temp_Entrada_Caliente.value and Temp_Salida_Caliente.value
                    and Temp_Entrada_Frio.value and Temp_Salida_Frio.value):
                if IniciarCodigo_Botón is None:
                    IniciarCodigo_Botón = ft.ElevatedButton(text="Iniciar", on_click=lambda e: iniciar_calculos_1())
                    page.add(IniciarCodigo_Botón)
            else:
                if IniciarCodigo_Botón is not None:
                    page.controls.remove(IniciarCodigo_Botón)
                    IniciarCodigo_Botón = None
            page.update()

        def iniciar_calculos_1():

            # Aquí puedes agregar la lógica para iniciar los cálculos
            print("Iniciando cálculos con los valores ingresados...")

            interfaz_de_espera()


    def interfaz_de_espera ():
        page.controls.clear()
        nonlocal P_input_Coraza_1, P_input_Coraza_2,P_input_Tubos_1,P_input_Tubos_2, Min_efectividad, IniciarCodigo_Botón2
        IniciarCodigo_Botón2 = None

        Caida_requerida_Coraza = ft.Container(
            content=ft.Column([
                ft.Text("Caidas de presión permitida en la Coraza", size=28, color="black"),
                P_input_Coraza_1 := ft.TextField(label="Minimo caida de presión en psi",text_style=ft.TextStyle(color="black"),border_color="black",label_style=ft.TextStyle(color="black"), on_change=lambda e: actualizar_boton_intermedio()),
                P_input_Coraza_2 := ft.TextField(label="Máxima caida de presión en psi",text_style=ft.TextStyle(color="black"),border_color="black",label_style=ft.TextStyle(color="black"), on_change=lambda e: actualizar_boton_intermedio()),
            ]),
            alignment=ft.alignment.center_right, # Alineado a la izquierda
            padding=ft.padding.all(10), # Espaciado interno (padding)
            bgcolor=ft.colors.CYAN_300, # Color de fondo
            border_radius=10, # Bordes redondeados
            width=400  # Ancho del contenedor
        )

        Caida_requerida_Tubos = ft.Container(
            content=ft.Column([
                ft.Text("Caidas de presión permitida en los tubos", size=28, color="black"),
                P_input_Tubos_1 := ft.TextField(label="Minimo caida de presión en psi",text_style=ft.TextStyle(color="black"),border_color="black",label_style=ft.TextStyle(color="black"), on_change=lambda e: actualizar_boton_intermedio()),
                P_input_Tubos_2 := ft.TextField(label="Máxima caida de presión en psi",text_style=ft.TextStyle(color="black"),border_color="black",label_style=ft.TextStyle(color="black"), on_change=lambda e: actualizar_boton_intermedio()),
            ]),
            alignment=ft.alignment.center_left, # Alineado a la izquierda
            padding=ft.padding.all(10), # Espaciado interno (padding)
            bgcolor=ft.colors.ORANGE_300, # Color de fondo
            border_radius=10, # Bordes redondeados
            width=400  # Ancho del contenedor
        )

        Minimo_efectividad = ft.Container(
            content=ft.Column([
                ft.Text("Selección de efectividad:", size=28, color="black"),
                Min_efectividad := ft.TextField(label="Mínima efectividad del intercambiador de calor:",text_style=ft.TextStyle(color="black"),border_color="black",label_style=ft.TextStyle(color="black"), on_change=lambda e: actualizar_boton_intermedio()),
            ]),
            alignment=ft.alignment.center_left, # Alineado a la izquierda
            padding=ft.padding.all(10), # Espaciado interno (padding)
            bgcolor=ft.colors.BLUE_400, # Color de fondo
            border_radius=10, # Bordes redondeados
            width=400  # Ancho del contenedor
        )

        # Fila que contiene ambos contenedores
        fila = ft.Row(
            controls=[Caida_requerida_Tubos, Caida_requerida_Coraza, Minimo_efectividad],
            alignment=ft.MainAxisAlignment.SPACE_AROUND,  # Alinea ambos contenedores con espacio alrededor
        )
        # Mostrar los campos de entrada para el fluido caliente y frío
        page.add(fila)
        page.update()

        def actualizar_boton_intermedio():
            nonlocal IniciarCodigo_Botón2
            if (P_input_Coraza_1.value and P_input_Coraza_2.value and P_input_Tubos_1.value
                    and P_input_Tubos_2.value and Min_efectividad.value):
                if IniciarCodigo_Botón2 is None:
                    IniciarCodigo_Botón2 = ft.ElevatedButton(text="Iniciar Calculos", on_click=lambda e: cambiar_interfaz_4())
                    page.add(IniciarCodigo_Botón2)
            else:
                if IniciarCodigo_Botón2 is not None:
                    page.controls.remove(IniciarCodigo_Botón2)
                    IniciarCodigo_Botón2 = None
            page.update()

    def cambiar_interfaz_4():
        # Limpiar la pantalla:
        page.controls.clear()
        progress_ring.visible = True
        page.update()
        page.add(
            ft.Column(
                [
                    progress_ring
                ],
                alignment=ft.MainAxisAlignment.CENTER,  # Alinea verticalmente al centro
                horizontal_alignment=ft.CrossAxisAlignment.CENTER  # Alinea horizontalmente al centro
            )
        )

        nonlocal Flujo_másico_Caliente,Temp_Entrada_Caliente,Temp_Salida_Caliente,Temp_Entrada_Frio,Temp_Salida_Frio, P_input_Coraza_1, P_input_Coraza_2, P_input_Tubos_1, P_input_Tubos_2, Min_efectividad, Sustancia_Caliente_Seleccionada, Sustancia_Fria_Seleccionada
        #Variables dadas por el usuario:

        T_entr_C= float(Temp_Entrada_Caliente.value)         #Unidades: °F
        T_sal_C= float(Temp_Salida_Caliente.value)           #Unidades: °F
        m_C=float(Flujo_másico_Caliente.value)               #Unidades: lb/h
        T_entr_F= float(Temp_Entrada_Frio.value)             #Unidades: °F
        T_sal_F= float(Temp_Salida_Frio.value)               #Unidades: °F
        T_prom_C= (T_entr_C+T_sal_C)/2
        T_prom_F= (T_entr_F+T_sal_F)/2
        #Selección de propiedades para sustancias Caliente y Fria:

        #SUSTANCIAS CALIENTES:

        if Sustancia_Caliente_Seleccionada == "Tetracloruro de Carbono":
            R_C= 0.0005
            
            #Función Propieades: Estado liquido:
            if T_prom_C <= 169:
                Dens_C= (-0.0653*T_prom_C)+103.61       #Unidades: lb/ft3
                Cp_C= (0.0001*T_prom_C)+0.176           #Unidades: lb/h*ft
                Visc_C= (-0.0098*T_prom_C)+2.8045       #Unidades: Btu/h*°F
                Condc_C= ((-7*10**(-5))*T_prom_C)+0.0631  #Unidades: Btu/lb*°F
            
            #Función Propieades: Estado Gaseoso:
            if T_prom_C > 169:
                Dens_C= (7*(10**(-7))*(T_prom_C**2))-(0.0008*T_prom_C)+0.4621       #Unidades: lb/ft3
                Cp_C= ((5*(10**(-5)))*T_prom_C)+0.1301                              #Unidades: lb/h*ft
                Visc_C= ((5*(10**(-5)))*T_prom_C)+0.0196                            #Unidades: Btu/h*°F
                Condc_C= (1*(10**(-5))*T_prom_C)+0.0031                             #Unidades: Btu/lb*°F

            Pr_C=(Visc_C*Cp_C)/(Condc_C)
            s_C= Dens_C/62.24879

        if Sustancia_Caliente_Seleccionada == "Agua":
            R_C= 0.001

            #Función Propiedades: Estado Liquido:
            if T_prom_C <= 212:
                Dens_C= (-0.0272*T_prom_C)+64.984                                   #Unidades: lb/ft3
                Cp_C= (1*(10**(-6))*(T_prom_C**2))-(0.0002*T_prom_C)+1.0383         #Unidades: lb/h*ft
                Visc_C= (0.0001*(T_prom_C**2))-(0.0409*T_prom_C)+4.7526             #Unidades: Btu/h*°F
                Condc_C= (-1*(10**(-6))*(T_prom_C**2))+(0.0007*T_prom_C)+0.3088     #Unidades: Btu/lb*°F
                
            #Función Propiedades: Estado Gas:
            if T_prom_C > 212:
                Dens_C= (-5*(10**(-5))*(T_prom_C))+0.0466                                #Unidades: lb/ft3
                Cp_C= (7*(10**(-8))*(T_prom_C**2))+(2*(10**(-5))*T_prom_C)+0.4483        #Unidades: lb/h*ft
                Visc_C= (6*(10**(-5))*T_prom_C)+0.0174                                   #Unidades: Btu/h*°F
                Condc_C= (-3*(10**(-8))*(T_prom_C**2))+(1*(10**(-5))*T_prom_C)+0.0107    #Unidades: Btu/lb*°F

            Pr_C=(Visc_C*Cp_C)/(Condc_C)
            s_C= Dens_C/62.2487

        if Sustancia_Caliente_Seleccionada == "Kerosene":
            R_C= 0.001

            #Función Propiedades: Estado Liquido:
            if T_prom_C <= 350:
                Dens_C= (-8*(10**(-6))*(T_prom_C**2))(-0.0242*T_prom_C)+52.284                                  #Unidades: lb/ft3
                Cp_C= (0.0006*T_prom_C)+0.3934                                      #Unidades: lb/h*ft
                Visc_C= (5*(10**(-5))*(T_prom_C**2))-(0.0304*T_prom_C)+5.3733       #Unidades: Btu/h*°F
                Condc_C= (-4*(10**(-5))*T_prom_C)+0.0707                            #Unidades: Btu/lb*°F
                
            Pr_C=(Visc_C*Cp_C)/(Condc_C)
            s_C= Dens_C/62.2487

        if Sustancia_Caliente_Seleccionada == "Etilenglicol":
            R_C= 0.001

            #Función Propiedades: Estado Liquido:
            if T_prom_C <= 350:
                Dens_C= (-0.0276*T_prom_C)+71.544                                                                                      #Unidades: lb/ft3
                Cp_C= (0.0007*T_prom_C)+0.5105                                                                                          #Unidades: lb/h*ft
                Visc_C= (2.04*(10**(-8))*(T_prom_C**4))-(2.15*(10**(-5))*(T_prom_C**3))+(0.008557*(T_prom_C**2))-(1.555*T_prom_C)+113.57       #Unidades: Btu/h*°F
                Condc_C= (-2*(10**(-7))*(T_prom_C**2))+(9*(10**(-5))*T_prom_C)+0.1412                                                   #Unidades: Btu/lb*°F
                
            Pr_C=(Visc_C*Cp_C)/(Condc_C)
            s_C= Dens_C/62.2487

        if Sustancia_Caliente_Seleccionada == "Acido acético 5%":
            R_C= 0.001

            #Función Propiedades: Estado Liquido:
            if T_prom_C <= 210:
                Dens_C= (-1*10**(-5)*(T_prom_C**2))-(0.0269*T_prom_C)+65.414                                   #Unidades: lb/ft3
                Cp_C= (1*(10**(-6))*(T_prom_C**2))-(0.0001*T_prom_C)+ 0.9528                                   #Unidades: lb/h*ft
                Visc_C= (0.0001*(T_prom_C**2))-(0.0516*T_prom_C)+ 6.0902                                       #Unidades: Btu/h*°F
                Condc_C= (-7*(10**(-7))*(T_prom_C**2))+(0.0005*T_prom_C)+0.2713                                #Unidades: Btu/lb*°F
                
            #Función Propiedades: Estado Gas:
            if T_prom_C > 210:
                Dens_C= (7*10**(-8)*(T_prom_C**2))-(9*10**(-5)*(T_prom_C))+0.0578                              #Unidades: lb/ft3
                Cp_C= (9*10**(-5)*T_prom_C)+0.4144                                                             #Unidades: lb/h*ft
                Visc_C= (4*(10**(-5))*T_prom_C)+0.0144                                                         #Unidades: Btu/h*°F
                Condc_C= (1*(10**(-8))*(T_prom_C**2))+(2*(10**(-5))*T_prom_C)+0.0083                           #Unidades: Btu/lb*°F

            Pr_C=(Visc_C*Cp_C)/(Condc_C)
            s_C= Dens_C/62.2487

        if Sustancia_Caliente_Seleccionada == "Acido nitrico 70%":
            R_C= 0.001

            #Función Propiedades: Estado Liquido:
            if T_prom_C <= 180:
                Dens_C= (-0.0675*T_prom_C)+92.155                                   #Unidades: lb/ft3
                Cp_C= (0.0003*T_prom_C)+0.5595                                      #Unidades: lb/h*ft
                Visc_C= (0.0001*(T_prom_C**2))-(0.0418*T_prom_C)+4.7608            #Unidades: Btu/h*°F
                Condc_C= (-1*(10**(-6))*(T_prom_C**2))+(0.0003*T_prom_C)+0.1285     #Unidades: Btu/lb*°F
                
            #Función Propiedades: Estado Gas:
            if T_prom_C > 180:
                Dens_C= ((-0.0002)*T_prom_C)+0.1369                                #Unidades: lb/ft3
                Cp_C= (0.0002*T_prom_C)+0.2248                                     #Unidades: lb/h*ft
                Visc_C= (4*10**(-5)*T_prom_C)+0.0146                               #Unidades: Btu/h*°F
                Condc_C= (2*10**(-5)*T_prom_C)+0.0051                              #Unidades: Btu/lb*°F

            Pr_C=(Visc_C*Cp_C)/(Condc_C)
            s_C= Dens_C/62.2487

        #SUSTANCIAS FRIAS:

        if Sustancia_Fria_Seleccionada == "Tetracloruro de Carbono":
            R_F= 0.0005
            
            #Función Propieades: Estado liquido:
            if T_prom_F <= 169:
                Dens_F= (-0.0653*T_prom_F)+103.61       #Unidades: lb/ft3
                Cp_F= (0.0001*T_prom_F)+0.176           #Unidades: lb/h*ft
                Visc_F= (-0.0098*T_prom_F)+2.8045       #Unidades: Btu/h*°F
                Condc_F= ((-7*10**(-5))*T_prom_F)+0.0631  #Unidades: Btu/lb*°F
            
            #Función Propieades: Estado Gaseoso:
            if T_prom_F > 169:
                Dens_F= (7*(10**(-7))*(T_prom_F**2))-(0.0008*T_prom_F)+0.4621       #Unidades: lb/ft3
                Cp_F= ((5*(10**(-5)))*T_prom_F)+0.1301                              #Unidades: lb/h*ft
                Visc_F= ((5*(10**(-5)))*T_prom_F)+0.0196                            #Unidades: Btu/h*°F
                Condc_F= (1*(10**(-5))*T_prom_F)+0.0031                             #Unidades: Btu/lb*°F

            Pr_F=(Visc_F*Cp_F)/(Condc_F)
            s_F= Dens_F/62.24879
            m_F= (m_C*Cp_C*(T_entr_C-T_sal_C))/(Cp_F*(T_sal_F-T_entr_F))

        if Sustancia_Fria_Seleccionada == "Agua":
            R_F= 0.001
            
            #Función Propiedades: Estado Liquido:
            if T_prom_F <= 212:
                Dens_F= (-0.0272*T_prom_F)+64.984                                   #Unidades: lb/ft3
                Cp_F= (1*(10**(-6))*(T_prom_F**2))-(0.0002*T_prom_F)+1.0383         #Unidades: lb/h*ft
                Visc_F= (0.0001*(T_prom_F**2))-(0.0409*T_prom_F)+4.7526             #Unidades: Btu/h*°F
                Condc_F= (-1*(10**(-6))*(T_prom_F**2))+(0.0007*T_prom_F)+0.3088     #Unidades: Btu/lb*°F
                
            #Función Propiedades: Estado Gas:
            if T_prom_F > 212:
                Dens_F= (-5*(10**(-5))*(T_prom_F))+0.0466                                #Unidades: lb/ft3
                Cp_F= (7*(10**(-8))*(T_prom_F**2))+(2*(10**(-5))*T_prom_F)+0.4483        #Unidades: lb/h*ft
                Visc_F= (6*(10**(-5))*T_prom_F)+0.0174                                   #Unidades: Btu/h*°F
                Condc_F= (-3*(10**(-8))*(T_prom_F**2))+(1*(10**(-5))*T_prom_F)+0.0107    #Unidades: Btu/lb*°F

            Pr_F=(Visc_F*Cp_F)/(Condc_F)
            s_F= Dens_F/62.24879
            m_F= (m_C*Cp_C*(T_entr_C-T_sal_C))/(Cp_F*(T_sal_F-T_entr_F))

                #Datos del problema base:

            #Fluido Caliente (CCl4):

        if Sustancia_Fria_Seleccionada == "Kerosene":
            R_F= 0.001

            #Función Propiedades: Estado Liquido:
            if T_prom_F <= 350:
                Dens_F= (-0.141*T_prom_F)+51.362                                    #Unidades: lb/ft3
                Cp_F= (0.0006*T_prom_F)+0.3934                                      #Unidades: lb/h*ft
                Visc_F= (5*(10**(-5))*(T_prom_F**2))-(0.0304*T_prom_F)+5.3733       #Unidades: Btu/h*°F
                Condc_F= (-4*(10**(-5))*T_prom_F)+0.0707                            #Unidades: Btu/lb*°F
                
            Pr_F=(Visc_F*Cp_F)/(Condc_F)
            s_F= Dens_F/62.2487
            m_F= (m_C*Cp_C*(T_entr_C-T_sal_C))/(Cp_F*(T_sal_F-T_entr_F))

        if Sustancia_Fria_Seleccionada == "Etilenglicol":
            R_F= 0.001

            #Función Propiedades: Estado Liquido:
            if T_prom_F <= 350:
                Dens_F= (-0.0276*T_prom_C)+71.544                                                                                       #Unidades: lb/ft3
                Cp_F= (0.0007*T_prom_F)+0.5105                                                                                          #Unidades: lb/h*ft
                Visc_F= (2*(10**(-8))*(T_prom_F**4))-(2*(10**(-5))*(T_prom_F**3))+(0.0087*(T_prom_F**2))-(1.5671*T_prom_F)+113.57       #Unidades: Btu/h*°F
                Condc_F= (-2*(10**(-7))*(T_prom_F**2))+(9*(10**(-5))*T_prom_F)+0.1412                                                   #Unidades: Btu/lb*°F
                
            Pr_F=(Visc_F*Cp_F)/(Condc_F)
            s_F= Dens_F/62.2487      
            m_F= (m_C*Cp_C*(T_entr_C-T_sal_C))/(Cp_F*(T_sal_F-T_entr_F))

        if Sustancia_Fria_Seleccionada == "Acido acético 5%":
            R_F= 0.001

            #Función Propiedades: Estado Liquido:
            if T_prom_F <= 210:
                Dens_F= (-1*10**(-5)*(T_prom_F**2))-(0.0269*T_prom_F)+65.414                                   #Unidades: lb/ft3
                Cp_F= (1*(10**(-6))*(T_prom_F**2))-(0.0001*T_prom_F)+ 0.9528                                   #Unidades: lb/h*ft
                Visc_F= (0.0001*(T_prom_F**2))-(0.0516*T_prom_F)+ 6.0902                                       #Unidades: Btu/h*°F
                Condc_F= (-7*(10**(-7))*(T_prom_F**2))+(0.0005*T_prom_F)+0.2713                                #Unidades: Btu/lb*°F
                
            #Función Propiedades: Estado Gas:
            if T_prom_F > 210:
                Dens_F= (7*10**(-8)*(T_prom_F**2))-(9*10**(-5)*(T_prom_F))+0.0578                              #Unidades: lb/ft3
                Cp_F= (9*10**(-5)*T_prom_F)+0.4144                                                             #Unidades: lb/h*ft
                Visc_F= (4*(10**(-5))*T_prom_F)+0.0144                                                         #Unidades: Btu/h*°F
                Condc_F= (1*(10**(-8))*(T_prom_F**2))+(2*(10**(-5))*T_prom_F)+0.0083                           #Unidades: Btu/lb*°F

            Pr_F=(Visc_F*Cp_F)/(Condc_F)
            s_F= Dens_F/62.2487
            m_F= (m_C*Cp_C*(T_entr_C-T_sal_C))/(Cp_F*(T_sal_F-T_entr_F))

        if Sustancia_Fria_Seleccionada == "Acido nitrico 70%":
            R_F= 0.001

            #Función Propiedades: Estado Liquido:
            if T_prom_F <= 180:
                Dens_F= (-0.0675*T_prom_F)+92.155                                   #Unidades: lb/ft3
                Cp_F= (0.0003*T_prom_F)+0.5595                                      #Unidades: lb/h*ft
                Visc_F= (0.0001*(T_prom_F**2))-(0.0418*T_prom_F)+4.7608            #Unidades: Btu/h*°F
                Condc_F= (-1*(10**(-6))*(T_prom_F**2))+(0.0003*T_prom_F)+0.1285     #Unidades: Btu/lb*°F
                
            #Función Propiedades: Estado Gas:
            if T_prom_F > 180:
                Dens_F= ((-0.0002)*T_prom_F)+0.1369                                #Unidades: lb/ft3
                Cp_F= (0.0002*T_prom_F)+0.2248                                     #Unidades: lb/h*ft
                Visc_F= (4*10**(-5)*T_prom_F)+0.0146                               #Unidades: Btu/h*°F
                Condc_F= (2*10**(-5)*T_prom_F)+0.0051                              #Unidades: Btu/lb*°F

            Pr_F=(Visc_F*Cp_F)/(Condc_F)
            s_F= Dens_F/62.2487
            m_F= (m_C*Cp_C*(T_entr_C-T_sal_C))/(Cp_F*(T_sal_F-T_entr_F))

        #-------------------------------------------------------------------------------------------------------------------------------------------------
        #-------------------------------------------------------------------------------------------------------------------------------------------------

        #Variables de selección:
        Conf_Contracorriente=[None]

        #Variables de cálculo:

        Dis= None                #Diametro interno de la coraza: Unidades: in
        Nt=None                   #Número de tubos
        BWG=None                 
        Lt=None                  #Longitud de tubería: Unidades: ft
        Arreglo=None              #Arreglo de tuberías (Triangular (2) o cuadrado (1) )
        Pt=None                   #Pitch: Unidades: in
        nTubos=None               #Pasos por los tubos
        nCoraza=1                   #Pasos por la coraza
        B=None                    #Espaciado de los deflectores: Unidades: in
        Dip=None                  #Diametro interno de la tubería: Unidades: in
        d0=None                  #Diametro externo de la tubería: Unidades: in
        Espesor=None              #Espesor de la tubería: Unidades: in
        Spp=None                  #Superficie por pie lineal de la tubería: Unidades: ft
        Ap1=None                  #Area de flujo del tubo: Unidades: in^2        

        #-------------------------------------------------------------------------------------------------------------------------------------------------


        #-------------------------------------------------------------------------------------------------------------------------------------------------

        #Catalogo:

            #Catalogo Tuberías para intercambiadores de calor y condesadores:

                #Lista para d0 --> 1/2
        BWG_1_2= [12,14,16,18,20]    
        Espesor_1_2= [0.109,0.083,0.065,0.049,0.035]        #Unidades: in
        Dip_1_2= [0.282,0.334,0.370,0.402,0.430]            #Unidades: in
        Ap1_1_2= [0.0625,0.0876,0.1076,0.127,0.145]         #Unidades: in^2

                #Lista para d0 --> 3/4
        BWG_3_4= [10,11,12,13,14,15,16,17,18]
        Espesor_3_4= [0.134,0.120,0.109,0.095,0.083,0.072,0.065,0.058,0.049]        #Unidades: in
        Dip_3_4= [0.482,0.510,0.532,0.560,0.584,0.606,0.620,0.634,0.652]            #Unidades: in
        Ap1_3_4= [0.182,0.204,0.223,0.247,0.268,0.289,0.302,0.314,0.334]            #Unidades: in^2

                #Lista para d0 --> 1:
        BWG_1= [8,9,10,11,12,13,14,15,16,17,18]
        Espesor_1= [0.165,0.148,0.134,0.120,0.109,0.095,0.083,0.072,0.065,0.058,0.049]      #Unidades: in    
        Dip_1= [0.67,0.704,0.732,0.76,0.782,0.81,0.834,0.856,0.87,0.884,0.902]              #Unidades: in
        Ap1_1= [0.355,0.389,0.421,0.455,0.479,0.515,0.546,0.576,0.594,0.613,0.639]          #Unidades: in^2

                #Lista para d0 --> 1 1/4:
        BWG_1_1_4= [8,9,10,11,12,13,14,15,16,17,18]
        Espesor_1_1_4= [0.165,0.148,0.134,0.12,0.109,0.095,0.083,0.072,0.065,0.058,0.049]       #Unidades: in
        Dip_1_1_4= [0.92,0.954,0.982,1.01,1.03,1.06,1.08,1.11,1.12,1.13,1.15]                   #Unidades: in
        Ap1_1_1_4= [0.665,0.714,0.757,0.8,0.836,0.884,0.923,0.96,0.985,1.01,1.04]               #Unidades: in^2

                #Lista para d0 --> 1 1/2:
        BWG_1_1_2= [8,9,10,11,12,13,14,15,16,17,18]
        Espesor_1_1_2= [0.165,0.148,0.134,0.12,0.109,0.095,0.083,0.072,0.065,0.058,0.049]       #Unidades: in
        Dip_1_1_2= [1.17,1.20,1.23,1.26,1.28,1.31,1.33,1.36,1.37,1.38,1.40]                     #Unidades: in
        Ap1_1_1_2= [1.075,1.14,1.19,1.25,1.29,1.35,1.40,1.44,1.47,1.50,1.54]                    #Unidades: in^2

            #Catalogo Número de tuberías en función del Pitch/d0/Dis

            #Configuración Cuadrada:

                #Lista para d0= 3/4 y Pt= 1: 
        Dis_1_C= [8,10,12,13.25,15.25,17.25,19.25,21.25,23.25,25,27,29,31,33,35,37,39]
        Nt_1_1P_C= [32,52,81,97,137,177,224,277,341,413,481,553,657,749,845,934,1049]
        Nt_1_2P_C= [26,52,76,90,124,166,220,270,324,394,460,526,640,718,824,914,1024]
        Nt_1_4P_C= [20,40,68,82,116,158,204,246,308,370,432,480,600,688,780,886,982]

                #Lista para d0= 1 y Pt= 1 1/4: 
        Dis_2_C= [8,10,12,13.25,15.25,17.25,19.25,21.25,23.25,25,27,29,31,33,35,37,39]
        Nt_2_1P_C= [21,32,48,61,81,112,138,177,213,260,300,341,406,465,522,596,665]
        Nt_2_2P_C= [16,32,45,56,76,112,132,166,208,252,288,326,398,460,518,574,644]
        Nt_2_4P_C=[14,26,40,52,68,96,128,158,192,238,278,300,380,432,488,562,624]

                #Lista para d0= 1.25 y Pt= 25/16 
        Dis_3_C= [10,12,13.25,15.25,17.25,19.25,21.25,23.25,25,27,29,31,33,35,37,39]
        Nt_3_1P_C= [16,30,32,44,56,78,96,127,140,166,193,226,258,293,334,370]
        Nt_3_2P_C= [12,24,30,40,53,73,90,112,135,160,188,220,252,287,322,362]
        Nt_3_4P_C= [10,22,30,37,51,71,86,106,127,151,178,209,244,275,311,348]

                #Lista para d0= 1.5 y Pt= 15/8
        Dis_4_C= [12,13.25,15.25,17.25,19.25,21.25,23.25,25,27,29,31,33,35,37,39]
        Nt_4_1P_C= [16,22,29,39,50,62,78,94,112,131,151,176,202,224,252]
        Nt_4_2P_C= [16,22,29,39,48,60,74,90,108,127,146,170,196,220,246]
        Nt_4_4P_C= [12,16,25,34,45,57,70,86,102,120,141,164,188,217,237]

            #Configuración Triangular:

                #Lista para d0= 3/4 y Pt= 15/16: 
        Dis_1_T= [8,10,12,13.25,15.25,17.25,19.25,21.25,23.25,25,27,29,31,33,35,37,39]
        Nt_1_1P_T= [36,62,109,127,170,239,301,361,442,532,637,721,847,974,1102,1240,1377]
        Nt_1_2P_T= [32,56,98,114,160,224,282,342,420,506,602,692,822,938,1068,1200,1330]
        Nt_1_4P_T= [26,47,86,96,140,194,252,314,386,468,550,640,766,878,1004,1144,1258]

                #Lista para d0= 3/4 y Pt= 1: 
        Dis_2_T= [8,10,12,13.25,15.25,17.25,19.25,21.25,23.25,25,27,29,31,33,35,37,39]
        Nt_2_1P_T= [37,61,92,109,151,203,262,316,384,470,559,630,745,856,970,1074,1206]
        Nt_2_2P_T= [30,52,82,106,138,196,250,302,376,452,534,604,728,830,938,1044,1176]
        Nt_2_4P_T= [24,40,76,86,122,178,226,278,352,422,488,556,678,774,882,1012,1128]

                #Lista para d0= 1 y Pt= 1.25 
        Dis_3_T= [8,10,12,13.25,15.25,17.25,19.25,21.25,23.25,25,27,29,31,33,35,37,39]
        Nt_3_1P_T= [21,32,55,68,91,131,163,199,241,294,349,397,472,538,608,674,766]
        Nt_3_2P_T= [16,32,52,66,86,118,152,188,232,282,334,376,454,522,592,664,736]
        Nt_3_4P_T= [16,26,48,58,80,106,140,170,212,256,302,338,430,486,562,632,700]

                #Lista para d0= 1.25 y Pt= 25/16
        Dis_4_T= [10,12,13.25,15.25,17.25,19.25,21.25,23.25,25,27,29,31,33,35,37,39]
        Nt_4_1P_T= [20,32,38,54,69,95,117,140,170,202,235,275,315,357,407,449]
        Nt_4_2P_T= [18,30,36,51,66,91,112,136,164,196,228,270,305,348,390,436]
        Nt_4_4P_T= [14,26,32,45,62,86,105,130,155,185,217,255,297,335,380,425]

                #Lista para d0= 1.5 y Pt= 15/8
        Dis_5_T= [12,13.25,15.25,17.25,19.25,21.25,23.25,25,27,29,31,33,35,37,39]
        Nt_5_1P_T= [18,27,36,48,61,76,95,115,136,160,184,215,246,275,307]
        Nt_5_2P_T= [14,22,34,44,58,72,91,110,131,154,177,206,238,268,299]
        Nt_5_4P_T= [14,18,32,42,55,70,86,105,125,147,172,200,230,260,290]

                #Lista de Variables combinatorias:

        d0_Pt_Catalogo= [1,2,3,4,5,6,7,8,9]

        d0_Catalogo= [1/2, 3/4, 1, 1.25, 1.5]

        Dis_Catalogo= [8,10,12,13.25,15.25,17.25,19.25,21.25,23.25,25,27,29,31,33,35,37,39]

        BWG_Catalogo= [8,9,10,11,12,13,14,15,16,17,18]

        Lt_Catalogo= [8, 12, 16, 20]

        Arreglo_Catalogo= [1,2]

        Pasos_Catalogo= [1,2,4]

        Pt_Catalogo= [1, 1.25, 25/16, 15/8, 15/16]

        Conf_Catalogo= [1,2]        #Contracorriente (1)  /   Paralelo (2)


        #-------------------------------------------------------------------------------------------------------------------------------------------------

        #Ciclo for de Selección optima de Diseño del intercambiador de Calor de tubos y coraza:

        Contador= 0
        resultados_column = []

        for d0_Pt_ ,Dis, BWG, Arreglo, Lt, nTubos, Conf_Contracorriente in itertools.product(d0_Pt_Catalogo, Dis_Catalogo, BWG_Catalogo, Arreglo_Catalogo, Lt_Catalogo, Pasos_Catalogo, Conf_Catalogo):
            
            Nt=None                   #Número de tubos                 
            Pt=None                   #Pitch: Unidades: in
            nCoraza=1                 #Pasos por la coraza
            Dip=None                  #Diametro interno de la tubería: Unidades: in
            d0=None                   #Diametro externo de la tubería: Unidades: in
            Espesor=None              #Espesor de la tubería: Unidades: in
            Spp=None                  #Superficie por pie lineal de la tubería: Unidades: ft
            Ap1=None                  #Area de flujo del tubo: Unidades: in^2 

            d0_Pt_L= [d0_Pt_]
            B= Dis*0.75


            if any(a in [1, 2, 3, 4] for a in d0_Pt_L):
                Arreglo = 1
                if d0_Pt_ == 1:
                    d0= d0_Catalogo[1]
                    Pt= Pt_Catalogo[0]

                if d0_Pt_ == 2:
                    d0= d0_Catalogo[2]
                    Pt= Pt_Catalogo[1]

                if d0_Pt_ == 3:
                    d0= d0_Catalogo[3]
                    Pt= Pt_Catalogo[2]

                if d0_Pt_ == 4:
                    d0= d0_Catalogo[4]
                    Pt= Pt_Catalogo[3]

            if any(a in [5, 6, 7, 8, 9] for a in d0_Pt_L):
                Arreglo = 2
                if d0_Pt_ == 5:
                    d0= d0_Catalogo[1]
                    Pt= Pt_Catalogo[4]

                if d0_Pt_ == 6:
                    d0= d0_Catalogo[1]
                    Pt= Pt_Catalogo[0]

                if d0_Pt_ == 7:
                    d0= d0_Catalogo[2]
                    Pt= Pt_Catalogo[1]

                if d0_Pt_ == 8:
                    d0= d0_Catalogo[3]
                    Pt= Pt_Catalogo[2]

                if d0_Pt_ == 9:
                    d0= d0_Catalogo[4]
                    Pt= Pt_Catalogo[3]

                #Correción de BWG para algunos Diametros externos de tubería:

        #d0 --> 1/2
            if BWG== 8 and d0== 1/2:
                BWG = 12

            if BWG== 9 and d0== 1/2:
                BWG = 12

            if BWG== 10 and d0== 1/2:
                BWG = 12

            if BWG== 11 and d0== 1/2:
                BWG = 12

        #d0 --> 3/4
            if BWG== 8 and d0== 3/4:
                BWG = 10

            if BWG== 9 and d0== 3/4:
                BWG = 10

        #d0 = 1.25 y Pt= 25/16     Arreglo: Cuadrado
            if d0_Pt_ == 3 and Dis == 8:
                Dis= 10

        #d0 = 1.5 y Pt= 15/8       Arreglo: Cuadrado
            if d0_Pt_ == 4 and Dis == 8:
                Dis= 12
            if d0_Pt_ == 4 and Dis == 10:
                Dis= 12

        #d0 = 1.25 y Pt= 25/16       Arreglo: Triangular
            if d0_Pt_ == 8 and Dis == 8:
                Dis= 10

        #d0 = 1.5 y Pt= 15/8       Arreglo: Cuadrado
            if d0_Pt_ == 9 and Dis == 8:
                Dis= 12
            if d0_Pt_ == 9 and Dis == 10:
                Dis= 12

            if d0 == 1/2:

                Spp = 0.1309                #Unidades: ft^2

                for i in range(0,5):

                    if BWG == BWG_1_2[i]:
                        Espesor = Espesor_1_2[i]
                        Dip = Dip_1_2[i]
                        Ap1 = Ap1_1_2[i]

            if d0 == 3/4:

                Spp = 0.1963                #Unidades: ft^2

                for i in range(0,9):

                    if BWG == BWG_3_4[i]:
                        Espesor = Espesor_3_4[i]
                        Dip = Dip_3_4[i]
                        Ap1 = Ap1_3_4[i]

            if d0 == 1:

                Spp = 0.2618                #Unidades: ft^2

                for i in range(0,11):

                    if BWG == BWG_1[i]:
                        Espesor = Espesor_1[i]
                        Dip = Dip_1[i]
                        Ap1 = Ap1_1[i]

            if d0 == 1.25:

                Spp = 0.3271                #Unidades: ft^2

                for i in range(0,11):

                    if BWG == BWG_1_1_4[i]:
                        Espesor = Espesor_1_1_4[i]
                        Dip = Dip_1_1_4[i]
                        Ap1 = Ap1_1_1_4[i]

            if d0 == 1.5:

                Spp = 0.3925                #Unidades: ft^2

                for i in range(0,11):

                    if BWG == BWG_1_1_2[i]:
                        Espesor = Espesor_1_1_2[i]
                        Dip = Dip_1_1_2[i]
                        Ap1 = Ap1_1_1_2[i]


            if Arreglo == 1:

                if d0 == 3/4 and Pt == 1:
                    for i in range(0,17):

                        if Dis == Dis_1_C[i]:
                            if nTubos == 1:
                                Nt= Nt_1_1P_C[i]
                            if nTubos == 2:
                                Nt= Nt_1_2P_C[i]
                            if nTubos == 4:
                                Nt= Nt_1_4P_C[i]

                if d0 == 1 and Pt== 1.25:
                    for i in range(0,17):
                        if Dis == Dis_2_C[i]:
                            if nTubos == 1:
                                Nt= Nt_2_1P_C[i]
                            if nTubos == 2:
                                Nt= Nt_2_2P_C[i]
                            if nTubos == 4:
                                Nt= Nt_2_4P_C[i]

                if d0 == 1.25 and Pt== 25/16:
                    for i in range(0,16):
                        if Dis == Dis_3_C[i]:
                            if nTubos == 1:
                                Nt= Nt_3_1P_C[i]
                            if nTubos == 2:
                                Nt= Nt_3_2P_C[i]
                            if nTubos == 4:
                                Nt= Nt_3_4P_C[i]

                if d0 == 1.5 and Pt== 15/8:
                    for i in range(0,15):
                        if Dis == Dis_4_C[i]:
                            if nTubos == 1:
                                Nt= Nt_4_1P_C[i]
                            if nTubos == 2:
                                Nt= Nt_4_2P_C[i]
                            if nTubos == 4:
                                Nt= Nt_4_4P_C[i]

            if Arreglo== 2:

                if d0 == 3/4 and Pt == 15/16:
                    for i in range(0,17):

                        if Dis == Dis_1_T[i]:
                            if nTubos == 1:
                                Nt= Nt_1_1P_T[i]
                            if nTubos == 2:
                                Nt= Nt_1_2P_T[i]
                            if nTubos == 4:
                                Nt= Nt_1_4P_T[i]

                if d0 == 3/4 and Pt== 1:
                    for i in range(0,17):
                        if Dis == Dis_2_T[i]:
                            if nTubos == 1:
                                Nt= Nt_2_1P_T[i]
                            if nTubos == 2:
                                Nt= Nt_2_2P_T[i]
                            if nTubos == 4:
                                Nt= Nt_2_4P_T[i]

                if d0 == 1 and Pt== 1.25:
                    for i in range(0,17):
                        if Dis == Dis_3_T[i]:
                            if nTubos == 1:
                                Nt= Nt_3_1P_T[i]
                            if nTubos == 2:
                                Nt= Nt_3_2P_T[i]
                            if nTubos == 4:
                                Nt= Nt_3_4P_T[i]

                if d0 == 1.25 and Pt== 25/16:
                    for i in range(0,16):
                        if Dis == Dis_4_T[i]:
                            if nTubos == 1:
                                Nt= Nt_4_1P_T[i]
                            if nTubos == 2:
                                Nt= Nt_4_2P_T[i]
                            if nTubos == 4:
                                Nt= Nt_4_4P_T[i]
                
                if d0 ==1.5  and Pt== 15/8:
                    for i in range(0,15):
                        if Dis == Dis_5_T[i]:
                            if nTubos == 1:
                                Nt= Nt_5_1P_T[i]
                            if nTubos == 2:
                                Nt= Nt_5_2P_T[i]
                            if nTubos == 4:
                                Nt= Nt_5_4P_T[i]

        #-------------------------------------------------------------------------------------------------------------------------------------------------    

            #Calculos:

            #Factor de correción F:
            R=(T_entr_C-T_sal_C)/(T_sal_F-T_entr_F)
            S= (T_sal_F-T_entr_F)/(T_entr_C-T_entr_F)
            F=((((R**2)+1)**(1/2))*(math.log((1-S)/(1-(R*S)))))/(((R-1)*(math.log((2-(S*(R+1-(((R**2)+1)**(1/2)))))/(2-(S*(R+1+(((R**2)+1)**(1/2)))))))))

            #Media logaritmica de la temperatura corregida (°F):
            if Conf_Contracorriente == 1:
                DT2= (T_entr_C-T_sal_F)
                DT1=(T_sal_C-T_entr_F)
                DTlm= (DT2-DT1)/(math.log(DT2/DT1))
                DTlm_C= DTlm*F
                Configuración="Contracorriente"
            if Conf_Contracorriente ==2:
                DT2= (T_entr_C-T_entr_F)
                DT1=(T_sal_C-T_sal_F)
                DTlm= (DT2-DT1)/(math.log(DT2/DT1))
                DTlm_C= DTlm*F
                Configuración="Paralelo"

            #Áreas de flujo:

                #Coraza:
            C=(Pt)-(Dip+Espesor)        #Unidades: in
            As=(Dis*C*B)/(Pt*144)       #Unidades: ft^2

                #Tubos:
            Ap2= (Nt*Ap1)/(144*nTubos)  #Unidades: ft^2

            #Flux másico (lb/h*ft^2):

                #Coraza:
            Gs=(m_F/As) 

                #Tubos:
            Gp=(m_C/Ap2)

            #Velocidades másicas (ft/s):

                #Tubos:
            V=(Gp/(3600*Dens_C))

            #Número de Reynolds:

                #Coraza
            if Arreglo == True:  #Arreglo Cuadrado
                Deq=(4*((Pt**2)-((math.pi*(d0**2))/4)))/(math.pi*d0)
            else:
                Deq=(4*(((Pt/2)*(0.86*Pt))-((1/2)*((math.pi*(d0**2))/4))))/((1/2)*(math.pi*d0))

            Re_Coraza=(Deq*Gs)/(Visc_F)

                #Tubos:
            Re_Tubos= (Dip*Gp)/(Visc_C)

            #Coeficientes convectivos (Btu/h*ft^2*°F):

                #Coraza:
            if 0.4 < Re_Coraza < 4:
                Nu_Coraza=(0.989)*(Re_Coraza**(0.330))*(Pr_F**(1/3))
            if 4 <= Re_Coraza < 40:
                Nu_Coraza=(0.911)*(Re_Coraza**(0.385))*(Pr_F**(1/3))
            if 40 <= Re_Coraza < 4000:
                Nu_Coraza=(0.683)*(Re_Coraza**(0.466))*(Pr_F**(1/3))
            if 4000 <= Re_Coraza < 40000:
                Nu_Coraza=(0.193)*(Re_Coraza**(0.618))*(Pr_F**(1/3))
            if 40000 <= Re_Coraza:
                Nu_Coraza=(0.027)*(Re_Coraza**(0.805))*(Pr_F**(1/3))

            ho= (Nu_Coraza*Condc_F)/(Deq/12)

                #Tubos:
            Nu_Tubos= (0.023)*(Re_Tubos**(0.8))*(Pr_C**(0.3))
            hi= (Nu_Tubos*Condc_C)/(Dip/12)

            #Coeficiente interno corregido:

            hi_o=(hi*(Dip/d0))

            #Coeficiente Total limpio (Btu/h*ft^2*°F):

            Uc=(hi_o*ho)/(hi_o + ho)

            #Area de transferencia (ft^2):

            At= (Nt*Lt*Spp)

            #Coeficiente total de diseño (Btu/h*ft^2*°F):

            Ud= ((1/Uc)+(R_C)+(R_F))**(-1)

            #Metodo NTU: Cálculo de la efectividad de un intercambiador de tubos y coraza:

            C_C= m_C*Cp_C
            C_F= m_F*Cp_F

            if C_C < C_F:
                Cmin= C_C
                Cmáx= C_F
            
            if C_C >= C_F:
                Cmin= C_F
                Cmáx= C_C

            NTU= (Ud*At)/(Cmin)
            c=Cmin/Cmáx

            if nTubos==1:
                if Conf_Contracorriente==1:
                    Efectividad= ((1-(math.exp(-NTU*(1-c))))/(1-(c*(math.exp(-NTU*(1-c))))))*100
                if Conf_Contracorriente==2:
                    Efectividad= ((1-(math.exp(-NTU*(1+c))))/(1+c))*100
            
            if nTubos >= 2:
                C1= ((1+ (c**2))**(1/2))
                Efectividad= (2*100)*((1 + c + (C1*((1+(math.exp(-NTU*C1)))/(1-(math.exp(-NTU*C1))))))**(-1))

            #Calculos de caidas de presión:

                #Coraza:
            N_1= (12*Lt)/(B)
            f_s= (0.0014)+(0.125/(Re_Coraza**(0.32)))
            Dp_s= ((f_s)*(Gs**2)*(Dis/12)*(N_1))/(2*(4.18*10**(8))*(Dens_F)*(Deq/12))

                #Tubos:
            f_p= (0.0014)+(0.125/(Re_Tubos**(0.32)))
            Dp_p= ((f_p)*(Gp**2)*(Lt)*(nTubos))/(2*(4.18*10**(8))*(Dens_C)*(Dip/12))
            Dp_r= (4*nTubos/s_C)*((V**2)/(2*32.2))*(Dens_C/144)
            Dp_total= (Dp_p + Dp_r)/(144)

            RangoInferiorDps= float(P_input_Coraza_1.value)
            RangoSuperiorDps= float(P_input_Coraza_2.value)
            RangoInferiorDptotal= float(P_input_Tubos_1.value)
            RangoSuperiorDptotal= float(P_input_Tubos_2.value)
            ValorMinimoEfectividad = float(Min_efectividad.value)

            if Arreglo == 1:
                NArreglo= "Cuadrada"
            if Arreglo == 2:
                NArreglo= "Triangular"

            Contador += 1

                    # Mostrar los resultados

            if RangoInferiorDps <= Dp_s <= RangoSuperiorDps and RangoInferiorDptotal <= Dp_total <= RangoSuperiorDptotal and Efectividad > ValorMinimoEfectividad:     
                resultados_column.append(
                    ft.Column([
                        ft.Text("-----------------------------------------------------------------------------------------"),
                        ft.Text(f"RESULTADOS DE DISEÑO {Contador}", size=30,text_align=ft.TextAlign.CENTER, color=ft.colors.RED_500),
                        ft.Text("DISEÑO:", size=27,text_align=ft.TextAlign.CENTER, color=ft.colors.RED_400),
                        ft.Text(f"CONFIGURACIÓN: {Configuración}", size=26,text_align=ft.TextAlign.CENTER, color=ft.colors.RED_300),
                        ft.Text(f"DISTRIBUCIÓN: {NArreglo}", size=26,text_align=ft.TextAlign.CENTER, color=ft.colors.RED_300),
                        ft.Text("TUBOS:", size=25,text_align=ft.TextAlign.CENTER, color=ft.colors.RED_200),
                        ft.Text(f"Pasos por los tubos: {nTubos}",text_align=ft.TextAlign.CENTER),
                        ft.Text(f"Diametro nominal de tuberías: {d0}",text_align=ft.TextAlign.CENTER),
                        ft.Text(f"BWG: {BWG}",text_align=ft.TextAlign.CENTER),
                        ft.Text(f"Longitud de tuberías: {Lt}",text_align=ft.TextAlign.CENTER),
                        ft.Text(f"Pitch de tuberías: {Pt}",text_align=ft.TextAlign.CENTER),
                        ft.Text(f"Número de tubos: {Nt}",text_align=ft.TextAlign.CENTER),
                        ft.Text("CORAZA:", size=25,text_align=ft.TextAlign.CENTER, color=ft.colors.RED_200),
                        ft.Text(f"Pasos por la coraza: {nCoraza}",text_align=ft.TextAlign.CENTER),
                        ft.Text(f"Diametro interno de la coraza: {Dis}",text_align=ft.TextAlign.CENTER),
                        ft.Text(f"Espaciado de deflectores: {B}",text_align=ft.TextAlign.CENTER),
                        ft.Text(f"VARIABLES DE IMPORTANCIA:", size=27,text_align=ft.TextAlign.CENTER, color=ft.colors.RED_200),
                        ft.Text(f"Coeficiente total de diseño: {Ud: .3f}",text_align=ft.TextAlign.CENTER),
                        ft.Text(f"Área de transferencia: {At}",text_align=ft.TextAlign.CENTER),
                        ft.Text(f"Caida de presión en la tubería: {Dp_total: .3f}",text_align=ft.TextAlign.CENTER),
                        ft.Text(f"Caida de presión en la coraza: {Dp_s: .3f}",text_align=ft.TextAlign.CENTER),
                        ft.Text(f"Efectividad: {Efectividad: .3f}",text_align=ft.TextAlign.CENTER),
                            #ft.Text(f"Reynolds Coraza: {Re_Coraza: .3f}",text_align=ft.TextAlign.CENTER),
                            #ft.Text(f"Reynolds Tubos: {Re_Tubos: .3f}",text_align=ft.TextAlign.CENTER),
                            #ft.Text(f"hio: {hi_o: .3f}",text_align=ft.TextAlign.CENTER),
                            #ft.Text(f"htubos: {ho: .3f}",text_align=ft.TextAlign.CENTER),
                            #ft.Text(f"Nu coraza: {Nu_Coraza: .3f}",text_align=ft.TextAlign.CENTER),
                            #ft.Text(f"Nu tubos: {Nu_Tubos: .3f}",text_align=ft.TextAlign.CENTER),
                            #ft.Text(f"Uc: {Uc: .3f}",text_align=ft.TextAlign.CENTER),
                            #ft.Text(f"Gs coraza: {Gs: .3f}",text_align=ft.TextAlign.CENTER),
                            #ft.Text(f"Gp tubos: {Gp: .3f}",text_align=ft.TextAlign.CENTER),
                        ft.Text("-----------------------------------------------------------------------------------------"),
                    ])
                )

        resultados_list_view = ft.ListView(
            controls=resultados_column,
            spacing=10,
            auto_scroll=True,
            height=600,
            )

        # Contenedor para centrar el ListView
        centrado_container = ft.Container(
            content=resultados_list_view,
            alignment=ft.alignment.center,          # Alinea el contenido en el centro
            width=None,                             # Ancho del contenedor, ajústalo según sea necesario
            padding=ft.padding.all(10)              # Padding alrededor del ListView
        )

        # Contenedor principal para centrar todo
        contenedor_principal = ft.Container(
            content=centrado_container,
            alignment=ft.alignment.center,          # Alinea el contenido en el centro
            width=None,                             # Ajusta el ancho según tu diseño
            padding=ft.padding.all(10)              # Padding alrededor del contenedor principal
        )
        progress_ring.visible=False
        Sustancia_Caliente_Seleccionada = ""
        Sustancia_Fria_Seleccionada = ""
        Boton_volver_inicio = ft.ElevatedButton(text="Volver al menú", on_click=cambiar_interfaz_1)
        page.add(contenedor_principal, Boton_volver_inicio)
        page.update()
        print(Contador)



            # Creamos un botón para continuar
    continue_button = ft.ElevatedButton(
        text="¡Iniciar!",
        on_click=cambiar_interfaz_1  # Dirigir a otra pantalla
    )
            
            # Añadimos los elementos a la pantalla
    page.add(
        ft.Column(
            [
                welcome_text,
                continue_button,
            ],
            alignment=ft.MainAxisAlignment.CENTER,  # Centra los elementos en la pantalla
        )
    )

# Ejecutar la app en un entorno de escritorio o navegador automáticamente
ft.app(target=main)
