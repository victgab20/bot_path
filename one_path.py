import numpy as np
import matplotlib.pyplot as plt
import math
import networkx as nx

def intersecta(seg1, seg2):
    k, l = seg1
    m, n = seg2
    det = (n[0] - m[0]) * (l[1] - k[1]) - (n[1] - m[1]) * (l[0] - k[0])
    if det == 0:
        return False
    s = ((n[0] - m[0]) * (m[1] - k[1]) - (n[1] - m[1]) * (m[0] - k[0])) / det
    t = ((l[0] - k[0]) * (m[1] - k[1]) - (l[1] - k[1]) * (m[0] - k[0])) / det
    return 0 < s < 1 and 0 < t < 1

def ponto_dentro_do_quadrado(px, py, quadrado):
    x_coords = [p[0] for p in quadrado]
    y_coords = [p[1] for p in quadrado]
    return min(x_coords) <= px <= max(x_coords) and min(y_coords) <= py <= max(y_coords)

def gerar_pontos(n_valor, evitar):
    sla1 = []
    sla2 = []
    quadrados = []
    gerados = 0
    while gerados < n_valor:
        x = np.random.randint(0, 100)
        y = np.random.randint(0, 100)
        p1 = (x, y)
        p2 = (x + L, y)
        p3 = (x + L, y - L)
        p4 = (x, y - L)
        valido = True
        for quadrado in quadrados:
            for ponto in [p1, p2, p3, p4]:
                if ponto_dentro_do_quadrado(ponto[0], ponto[1], quadrado):
                    valido = False
                    break
            if not valido:
                break
        if valido:
            sla1.extend([p1[0], p2[0], p3[0], p4[0]])
            sla2.extend([p1[1], p2[1], p3[1], p4[1]])
            quadrados.append([p1, p2, p3, p4])
            gerados += 1
    return sla1, sla2, quadrados

# Parâmetros
#aparentemente 15 de L e 30 pontos é o limite
L = 10
pontos = 25
evitar = []
sla1, sla2, quadrados = gerar_pontos(pontos, evitar)
sla1_final = [-15, 115] + sla1
sla2_final = [115, -15] + sla2

vertices = [(sla1_final[i], sla2_final[i]) for i in range(len(sla1_final))]
grafo = nx.Graph()
for v in vertices:
    grafo.add_node(v)

for quadrado in quadrados:
    for i in range(4):
        grafo.add_edge(quadrado[i], quadrado[(i + 1) % 4])

for i in range(len(vertices)):
    for j in range(i + 1, len(vertices)):
        p1, p2 = vertices[i], vertices[j]
        if p1 == p2:
            continue
        mesmo_quadrado = any(p1 in q and p2 in q for q in quadrados)
        if mesmo_quadrado:
            continue
        visivel = True
        for quadrado in quadrados:
            lados = [(quadrado[k], quadrado[(k + 1) % 4]) for k in range(4)]
            if any(intersecta((p1, p2), lado) for lado in lados):
                visivel = False
                break
        if visivel:
            grafo.add_edge(p1, p2)

inicio = (-15, 115)
fim = (115, -15)
try:
    caminho = nx.shortest_path(grafo, source=inicio, target=fim)
except nx.NetworkXNoPath:
    caminho = []

plt.figure(figsize=(10, 10))
plt.xlim(-20, 120)
plt.ylim(-20, 120)

plt.scatter(sla1_final, sla2_final, c='red', s=10, zorder=5)

for quadrado in quadrados:
    x_vals = [p[0] for p in quadrado] + [quadrado[0][0]]
    y_vals = [p[1] for p in quadrado] + [quadrado[0][1]]
    plt.plot(x_vals, y_vals, color='blue', zorder=1)

for i in range(len(caminho) - 1):
    x_vals = [caminho[i][0], caminho[i+1][0]]
    y_vals = [caminho[i][1], caminho[i+1][1]]
    plt.plot(x_vals, y_vals, color='green', linewidth=2, zorder=6)

plt.title("Caminho entre pontos evitando obstáculos")
plt.gca().set_aspect('equal', adjustable='box')
plt.grid(True)
plt.show()