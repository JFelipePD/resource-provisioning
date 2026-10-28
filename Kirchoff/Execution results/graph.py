# -*- coding: utf-8 -*-
import datetime
import os
import re
import sys
import matplotlib.pyplot as plt
import pandas as pd

if len(sys.argv) < 2:
  print("Uso correto: python3 graph.py <nome_do_arquivo_sem_extensao>")
  sys.exit(1)

file_name = sys.argv[1].replace(".txt", "")
file_path = file_name + ".txt"

if not os.path.exists(file_path):
  print(f"Erro: O arquivo '{file_path}' nao foi encontrado na pasta atual.")
  sys.exit(1)

with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
  lines = file.readlines()


def timeToStr(totalSecs):
  m, s = divmod(float(totalSecs), 60)
  h, m = divmod(m, 60)
  return "{:d}:{:02d}:{:02d}".format(int(h), int(m), int(s))


log2 = "Time;accepted;rejected;idle;qos\n"

for i in lines:
  index = i.find("Process Request:")
  if index > -1:
    line = i[index:]
    line = re.sub("([aA-zZ])", "", line)
    line = line.replace(" ", "")
    line = line.replace(":", ";")
    line = line.replace(",", ".")
    line = line.replace("-∞", "0")
    log2 += timeToStr(i[0 : index - 2]) + ";" + line[2:]

rows = [
    x.split(";")
    for x in log2.strip().split("\n")
    if x.strip() and len(x.split(";")) == 5
]

if len(rows) > 1:
  header = rows[0]
  data = rows[1:]

  dfm = pd.DataFrame(data, columns=header)
  dfm["accepted"] = dfm["accepted"].astype(float)
  dfm["rejected"] = dfm["rejected"].astype(float)
  dfm["idle"] = dfm["idle"].astype(float)
  dfm["qos"] = dfm["qos"].astype(float)

  fig, ax = plt.subplots(figsize=(12, 6), dpi=300)

  x_indices = range(len(dfm))
  capacity = dfm["accepted"] + dfm["idle"]
  load = dfm["accepted"] + dfm["rejected"]
  y_a = dfm["accepted"]

  # Curvas formatadas para artigo científico
  ax.fill_between(
      x_indices,
      capacity,
      color="#2ecc71",
      alpha=0.35,
      label="Recursos Alocados (Capacity)",
  )
  ax.plot(
      x_indices,
      load,
      label="Carga Total (Workload)",
      color="#2c3e50",
      linestyle=":",
      linewidth=0.9,
      alpha=0.85,
  )
  ax.plot(
      x_indices,
      y_a,
      label="Requisicoes Aceitas (Accepted)",
      color="#2980b9",
      linewidth=0.8,
      alpha=0.9,
  )

  # Distribuicao limpa no Eixo X (exibe apenas 10 rótulos de tempo)
  n_ticks = 10
  step = max(1, len(dfm) // n_ticks)
  tick_positions = list(range(0, len(dfm), step))
  tick_labels = [dfm["Time"].iloc[i] for i in tick_positions]

  ax.set_xticks(tick_positions)
  ax.set_xticklabels(tick_labels, rotation=30, ha="right", fontsize=9)

  ax.set_title(
      f"Provisionamento de Recursos vs. Demanda ({file_name})",
      fontsize=12,
      pad=12,
      fontweight="bold",
  )
  ax.set_xlabel("Tempo Simulado (hh:mm:ss)", fontsize=10, labelpad=8)
  ax.set_ylabel("Quantidade de Requisicoes", fontsize=10, labelpad=8)
  ax.grid(True, linestyle="--", alpha=0.4)
  ax.legend(loc="upper right", framealpha=0.9, fontsize=9)

  plt.tight_layout()

  os.makedirs("graph", exist_ok=True)
  desc = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
  output_pdf = f"graph/{file_name}_{desc}.pdf"
  output_png = f"graph/{file_name}_{desc}.png"

  plt.savefig(output_pdf, format="pdf", bbox_inches="tight")
  plt.savefig(output_png, format="png", bbox_inches="tight")

  print("Sucesso! Graficos gerados em:")
  print(f" - PDF: {output_pdf}")
  print(f" - PNG: {output_png}")
else:
  print(f"Atencao: Nenhuma linha valida encontrada em {file_path}")