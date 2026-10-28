import os

# Filtra apenas os arquivos de log com extensão .txt
dirs = [f for f in os.listdir('.') if f.endswith('.txt')]
dirs.sort()

def explore(line, value):
    index = line.find(value)
    if index > -1:
        line = line[index + len(value):]
        return line.strip()
    return None

def openFile(lines):
    model = None
    interval = None
    days = None
    hours = None
    accepted = None
    rejected = None
    qos = None

    for line in lines:
        if model is None: model = explore(line, "Prediction Model:")
        if interval is None: interval = explore(line, "Billing Time:")
        if days is None: days = explore(line, "Number of days:")
        if hours is None: hours = explore(line, "VM hours:")
        if accepted is None: accepted = explore(line, "Accepted:")
        if rejected is None: rejected = explore(line, "Rejected:")
        if qos is None: qos = explore(line, "QoS violations:")

    val = int(interval) / 60 if interval is not None else None
    return model, val, days, hours, accepted, rejected, qos

for filename in dirs:
    try:
        with open(filename, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()
            print(filename, openFile(lines))
    except Exception as e:
        print(f"Erro ao ler {filename}: {e}")
