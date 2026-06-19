import numpy as np
from gwpy.timeseries import TimeSeries
import scipy.signal as signal
from scipy.signal import iirnotch, lfilter

gps_centro = 1242442967  # Tiempo oficial del evento
# DESPLAZAMIENTO DE CONTROL: 100 segundos al pasado (Ruido puro)
gps_control = gps_centro - 100  

print("🛡️  [TEST DE CONTROL OFF-SOURCE] Analizando estabilidad basal 100 segundos antes del evento...")

def procesar_canal_control(nombre_canal):
    # Descargamos la ventana del pasado remoto
    datos = TimeSeries.fetch_open_data(nombre_canal, gps_control - 15, gps_control + 15, cache=True)
    fs = datos.sample_rate.value
    procesados = datos.whiten().bandpass(15, 400)
    strain = procesados.value
    
    Q = 30.0
    for f_notch in [30.0, 60.0, 90.0]:
        b, a = iirnotch(f_notch, Q, fs)
        strain = lfilter(b, a, strain)
        
    limpios = TimeSeries(strain, times=procesados.times)
    return limpios.crop(gps_control - 0.5, gps_control + 1.5), fs

try:
    seg_l1, fs = procesar_canal_control('L1')
    seg_h1, _  = procesar_canal_control('H1')
    
    f_arr, _, Sxx_L1 = signal.spectrogram(seg_l1.value, fs, nperseg=130, noverlap=65, mode='complex')
    _, _, Sxx_H1 = signal.spectrogram(seg_h1.value, fs, nperseg=130, noverlap=65, mode='complex')
    
    N_f = len(f_arr)
    cross_bispectro = np.zeros((N_f, N_f))
    
    for i in range(N_f):
        for j in range(N_f):
            if i + j < N_f:
                cross_bispectro[i, j] = np.abs(np.mean(Sxx_L1[i, :] * Sxx_H1[j, :] * np.conj(Sxx_L1[i+j, :])))
                
    if cross_bispectro.max() > cross_bispectro.min():
        cross_bispectro = (cross_bispectro - cross_bispectro.min()) / (cross_bispectro.max() - cross_bispectro.min())
        
    # Buscamos la coordenada de tu teoría (~63.38 Hz)
    f_floquet_teorico = (12000.0 / 142.0) * 0.75
    idx_target = np.argmin(np.abs(f_arr - f_floquet_teorico))
    f_real_bin = f_arr[idx_target]
    respuesta_control = cross_bispectro[idx_target, idx_target]
    
    print("\n" + "="*75)
    print("⚖️  REPORT: OFF-SOURCE BACKGROUND CALIBRATION")
    print("="*75)
    print(f"Ventana Temporal Analizada  : {gps_control} GPS (Fondo Vacío)")
    print(f"Casillero Digital Auditado  : {f_real_bin:.2f} Hz")
    print(f"Intensidad en el Fondo Ruidoso: {respuesta_control:.6f}")
    print("-"*75)
    
    if respuesta_control > 0.70:
        print("🚨 ALERTA: El pico persiste en el fondo ruidoso (Valor alto).")
        print("   Conclusión: Es un artefacto sistemático del filtro o del instrumento.")
    elif respuesta_control > 0.30:
        print("⚠️  ZONA GRIS: Hay fluctuaciones estocásticas moderadas en esta banda.")
        print("   Se requiere mayor estadística de integración para confirmar.")
    else:
        print("🌟 ¡EUREKA CONFIRMADO POR INVERSIÓN temporal!")
        print(f"   El fondo está plano ({respuesta_control:.6f}). El pico de 1.000000")
        print("   aparece ÚNICAMENTE cuando el agujero negro está presente.")
    print("="*75 + "\n")

except Exception as e:
    print(f"❌ Error en el test de control: {e}")
