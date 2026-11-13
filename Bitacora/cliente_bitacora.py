import requests

BASE = "http://localhost:8001"

# 1. Consultar todas las incidencias sin filtros
r = requests.get(f"{BASE}/incidencias", timeout=10)
print("Todas:", r.json())

# 2. Filtrar solo por tipo
r = requests.get(f"{BASE}/incidencias", params={"tipo": "alerta"}, timeout=10)
print("Solo por tipo:", r.json())

# 3. Filtrar solo por estado
r = requests.get(f"{BASE}/incidencias", params={"estado": "abierta"}, timeout=10)
print("Solo por estado:", r.json())

# 4. Filtros combinados (tipo y estado)
r = requests.get(
    f"{BASE}/incidencias", 
    params={"tipo": "alerta", "estado": "abierta"}, 
    timeout=10
)
print("Filtros combinados:", r.json())