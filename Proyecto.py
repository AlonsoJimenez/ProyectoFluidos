from matplotlib import container
from numpy.lib import info
from IPython.display import HTML
from IPython.display import display

from ipywidgets import interactive
import ipywidgets as widgets
import numpy as np
import math
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


def potencia(diametro, tiempoLlenado, volumen):
    return 55

def velocidad(diametro, volumen, tiempoLlenado):
    return 25

def volumenLlenado(velocidad, tiempo):
    return 100



def graficas():
    
    display (tag)
    
    def GraficoInteractivoGeneral(diametro, volumen, tiempoLlenado, tiempo):

      potProb = potencia(diametro, tiempoLlenado, volumen)
      velProb = velocidad(diametro, volumen, tiempoLlenado)
      volProb = volumenLlenado(velocidad, tiempo)


      fig,ax1 = plt.subplots ()

      ax1.set_title('Valores del problema')
      ax1.bar(['Potencia $(W)$', 'Velocidad salida $(m/s)$', 'Volumen llenado $(%)$'], [potProb, velProb, volProb])
      ax1.set_ylim([0, 100])  

      plt.show()

      return


    diametroTuboEtiqueta = widgets.Label (value="Diametro tubería $(m)$:")
    diametroTuboSlider = widgets.FloatSlider(min=1, max=5, step=0.1, value=0.0)
    cajaDiametroTubo = widgets.HBox([diametroTuboEtiqueta, diametroTuboSlider])

    tiempoLlenadoEtiqueta = widgets.Label (value="Tiempo llenado $(h)$:")
    tiempoLlenadoSlider = widgets.FloatSlider(min=1, max=10, step=0.01, value=0.0)
    cajaTiempoLlenado = widgets.HBox([tiempoLlenadoEtiqueta, tiempoLlenadoSlider])

    volumenEtiqueta = widgets.Label (value="Volumen a llenar $(m^3)$:")
    volumenSlider = widgets.FloatSlider(min=0, max=10, step=0.01, value=0.0)
    cajaVolumen = widgets.HBox([volumenEtiqueta, volumenSlider])

    play = widgets.Play(value=0, min=0, max=tiempoLlenadoSlider.value, step=0.1, disabled=False)
    tieEtiqueta = widgets.Label (value="Tiempo $(h)$:")
    tieSlider = widgets.FloatSlider(min=0, max=tiempoLlenadoSlider.value,)
    widgets.jslink((play, 'value'), (tieSlider, 'value'))
    cajaTiempo = widgets.HBox([tieEtiqueta, tieSlider])

    salida = widgets.interactive_output(GraficoInteractivoGeneral, {'diametro':diametroTuboSlider,
                                                                  'volumen':volumenSlider,
                                                                  'tiempoLlenado': tiempoLlenadoSlider,
                                                                  'tiempo':tieSlider})

    display(cajaDiametroTubo, cajaTiempoLlenado, cajaVolumen, cajaTiempo, play, salida)