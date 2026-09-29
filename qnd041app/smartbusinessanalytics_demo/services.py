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

  # 3. Carga oficial del modelo pre-entrenado compatible con la librería instalada
  model = timesfm.TimesFM_2p5_200M_torch.from_pretrained(
      "google/timesfm-2.5-200m-pytorch"
  )

  model.compile(
      timesfm.ForecastConfig(
          max_context=512,
          max_horizon=horizonte_meses,
          normalize_inputs=True,
          use_continuous_quantile_head=True,
          fix_quantile_crossing=True,
      )
  )

  # 4. Ejecutar inferencia (TimesFM recibe la lista de arreglos de contexto)
  point_forecast, quantile_forecast = model.forecast(
      inputs=[context_data],
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