import warnings
warnings.filterwarnings('ignore')

!pip install fluids
!jupyter nbextension enable --py widgetsnbextension --sys-prefix
!jupyter serverextension enable voila --sys-prefix

from matplotlib import container
from numpy.lib import info
from IPython.display import HTML
from IPython.display import display
from ipywidgets import interactive
import ipywidgets as widgets
import numpy as np
import math
import fluids
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.image as img
from matplotlib.offsetbox import  AnnotationBbox, OffsetImage



tag = HTML('''<script>
code_show=false; 
function code_toggle() {
    if (code_show){
        $('div.cell.code_cell.rendered.selected div.input').hide();
    } else {
        $('div.cell.code_cell.rendered.selected div.input').show();
    }
    code_show = !code_show
} 

$( document ).ready(code_toggle);
</script>

Para mostrar/ocultar código presione <a href="javascript:code_toggle()">aquí</a>.''')

g = 9.81
peso = 9780.57
l = 36 + 22
vis = 8.94E-7
epsilon = 4.6E-5
difAlturas = 22-2.5
eficiencia = 0.65


def hCodos(diametro, velocidad):
    ft = 0
    if(diametro == 12.7):
        ft = 0.027
    elif(diametro == 19.05):
        ft = 0.025
    elif(diametro == 25.4):
        ft = 0.023
    elif(diametro == 31.75):
        ft = 0.022
    elif(diametro == 38.1):
        ft = 0.021
    elif(diametro == 44.45):
        ft = 0.02
    elif(diametro == 50.8):
        ft = 0.019
    return (2*30*ft*velocidad**2)/(2*g)

def Reynolds(velocidad, diametro):
    diametro = diametro/1000
    return velocidad*diametro/vis    

def hTuberia(velocidad, diametro):
    reynolds = Reynolds(velocidad, diametro)
    diametro = diametro/1000
    f = fluids.friction.friction_factor(Re=reynolds, eD=epsilon/diametro)
    hl = f*(l/diametro)*((velocidad**2)/(2*g))
    return hl

def hEntradaSalida(velocidad):
    return velocidad**2/(2*g)

def hValvula(diametro, velocidad):
    ft = 0
    if(diametro == 12.7):
        ft = 0.027
    elif(diametro == 19.05):
        ft = 0.025
    elif(diametro == 25.4):
        ft = 0.023
    elif(diametro == 31.75):
        ft = 0.022
    elif(diametro == 38.1):
        ft = 0.021
    elif(diametro == 44.45):
        ft = 0.02
    elif(diametro == 50.8):
        ft = 0.019
    return 340*ft*velocidad**2/(2*g)

def potencia(diametro, tiempoLlenado, volumen):
    velocidad = velocidadCalculada(diametro/1000, volumen, tiempoLlenado)
    caudal = volumen/tiempoLlenado
    hc = hCodos(diametro, velocidad)
    ht = hTuberia(velocidad, diametro)
    hv = hValvula(diametro, velocidad)
    hes = hEntradaSalida(velocidad)
    ha = difAlturas + hc + ht + hes + hv
    return (ha*peso*caudal)/eficiencia

def velocidadCalculada(diametro, volumen, tiempoLlenado):
    return (volumen/(tiempoLlenado))/(math.pi*(diametro/(2))**2)

def volumenLlenado(volumen, tiempoLlenado, tiempo):
    volumenL = tiempo*(volumen/tiempoLlenado)
    return volumenL*100/volumen



def graficas():
    
    display (tag)
    
    def GraficoInteractivoGeneral(diametro, vacas, tiempoLlenado, tiempo):

      volumen = vacas*120/1000
      tiempo = tiempo*3600  
      tiempoLlenado = tiempoLlenado*3600

      potProb = potencia(diametro, tiempoLlenado, volumen)
      velProb = velocidadCalculada(diametro/1000, volumen, tiempoLlenado)
      volProb = volumenLlenado(volumen, tiempoLlenado, tiempo)

    

      fig,(ax1, ax2, ax3) = plt.subplots (1, 3, figsize = (20,7), dpi= 120, sharex = True)

      ax1.set_title('Potencia $(W)$ = '+str(potProb))
      ax1.bar(['Valores del problema'], [potProb])
      ax1.set_ylim([0, 750])  

      ax2.set_title('Velocidad $(m/s)$ = '+str(velProb))
      ax2.bar(['Valores del problema'], [velProb])
      ax2.set_ylim([0, 10]) 

      ax3.set_title('Volumen llenado: '+str(volProb)+' %')
      ax3.bar(['Valores del problema'], [volProb])
      ax3.set_ylim([0, 100]) 

      plt.show()

      return


    diametroTuboEtiqueta = widgets.Label (value="Diametro nominal tubería $(mm)$:")
    diametroTuboSlider = widgets.FloatSlider(min=12.7, max=50.8, step=6.35, value=25.4)
    cajaDiametroTubo = widgets.HBox([diametroTuboEtiqueta, diametroTuboSlider])

    tiempoLlenadoEtiqueta = widgets.Label (value="Tiempo llenado $(h)$:")
    tiempoLlenadoSlider = widgets.FloatSlider(min=1, max=10, step=0.01, value=1.5)
    cajaTiempoLlenado = widgets.HBox([tiempoLlenadoEtiqueta, tiempoLlenadoSlider])

    vacasEtiqueta = widgets.Label (value="Cantidad vacas")
    vacasSlider = widgets.IntSlider(min=1, max=50, step=1, value=30)
    cajaVacas = widgets.HBox([vacasEtiqueta, vacasSlider])

    play = widgets.Play(value=0, min=0, max=tiempoLlenadoSlider.value, step=0.1, disabled=False)
    tieEtiqueta = widgets.Label (value="Tiempo $(h)$:")
    tieSlider = widgets.FloatSlider(min=0, max=tiempoLlenadoSlider.value,)
    widgets.jslink((play, 'value'), (tieSlider, 'value'))
    cajaTiempo = widgets.HBox([tieEtiqueta, tieSlider])

    salida = widgets.interactive_output(GraficoInteractivoGeneral, {'diametro':diametroTuboSlider,
                                                                  'vacas':vacasSlider,
                                                                  'tiempoLlenado': tiempoLlenadoSlider,
                                                                  'tiempo':tieSlider})

    display(cajaDiametroTubo, cajaTiempoLlenado, cajaVacas, cajaTiempo, play, salida)