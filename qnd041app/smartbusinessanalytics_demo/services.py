import numpy as np
import pandas as pd
import timesfm
from .models import EstadoFinanciero


def predecir_metrica_financiera_torch(
    usuario_id=None,
    metrica: str = "utilidad_neta",
    horizonte_meses: int = 6,
):
  # 1. Obtener el histórico desde el ORM
  qs = EstadoFinanciero.objects.all()
  if usuario_id:
    qs = qs.filter(usuario_id=usuario_id)

  qs = qs.order_by("fecha_fin")

  registros = []
  for obj in qs:
    valor_obj = getattr(obj, metrica)
    # Manejar si el campo es MoneyField (djmoney) o Decimal puro
    if hasattr(valor_obj, "amount"):
      val = float(valor_obj.amount)
    elif valor_obj is not None:
      val = float(valor_obj)
    else:
      val = 0.0

    registros.append({"fecha": obj.fecha_fin, "valor": val})

  df = pd.DataFrame(registros)
  if df.empty or len(df) < 3:
    raise ValueError(
        "No hay suficientes datos históricos para generar un pronóstico."
    )

  # 2. Normalizar y asegurar periodicidad mensual
  df["fecha"] = pd.to_datetime(df["fecha"])
  df = df.set_index("fecha").resample("ME").last().fillna(0.0)

  context_data = df["valor"].astype(np.float32).values

  # 3. Cargar el modelo TimesFM usando la ruta local del checkpoint descargado
  # (Apunta a la carpeta checkpoints dentro del snapshot que encontraste)
  checkpoint_path = "/Users/smartquail/.cache/huggingface/hub/models--google--timesfm-1.0-200m/snapshots/8775f7531211ac864b739fe776b0b255c277e2be/checkpoints"

  model = timesfm.TimesFm(
      backend="torch",
      horizon_len=horizonte_meses,
      input_patch_len=32,
      output_patch_len=128,
      num_layers=20,
      model_dims=1280,
  )
  
  model.load_from_checkpoint(checkpoint_path)

  # 4. Ejecutar inferencia (TimesFM requiere una lista de inputs y frecuencia)
  # frequency=0 indica datos de alta frecuencia/mensuales según la API estándar
  point_forecast, quantile_forecast = model.forecast(
      inputs=[context_data],
      freq=[0] * len([context_data]), 
  )

  return {
      "historico": df["valor"].tolist(),
      "fechas_historico": df.index.strftime("%Y-%m-%d").tolist(),
      "pronostico_punto": point_forecast[0].tolist(),
      "cuantiles": (
          quantile_forecast[0].tolist()
          if quantile_forecast is not None
          else None
      ),
  }