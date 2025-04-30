#Pseudo código
# func_det(a,b,c,d)
# det = (a[0] - b[0]) * (a[1] - d[1]) - (a[1] - b[1]) * (c[0] - d[0])
# if det == 0 
# return True
# else:
# return none

# ponto inicial = [-15,115]
# esse x e y são as listas
# caminhos = []
# func_plot(x,y)
# for i in range(len x)
# if(det=(a=[x[i],y[i]],b=[x[i+1],y[i+1]]....)
# caminho.append(a,b,c,d)

import numpy as np
import matplotlib.pyplot as plt
import math

def intersecta(seg1, seg2):
    k, l = seg1
    m, n = seg2
    det = (n[0] - m[0]) * (l[1] - k[1]) - (n[1] - m[1]) * (l[0] - k[0])
    if det == 0:
        return False
    s = ((n[0] - m[0]) * (m[1] - k[1]) - (n[1] - m[1]) * (m[0] - k[0])) / det
    t = ((l[0] - k[0]) * (m[1] - k[1]) - (l[1] - k[1]) * (m[0] - k[0])) / det
    return 0 < s < 1 and 0 < t < 1

def is_intersecting(segment, obstacles_edges):
    for obstacle in obstacles_edges:
        for edge in obstacle:
            if intersecta(segment, edge):
                return True
    return False

def ponto_dentro_do_quadrado(px, py, quadrado):
    x_vals = [p[0] for p in quadrado]
    y_vals = [p[1] for p in quadrado]
    xmin, xmax = min(x_vals), max(x_vals)
    ymin, ymax = min(y_vals), max(y_vals)
    return xmin <= px <= xmax and ymin <= py <= ymax

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

def quadrado_para_arestas(quadrado):
    return [
        (quadrado[0], quadrado[1]),
        (quadrado[1], quadrado[2]),
        (quadrado[2], quadrado[3]),
        (quadrado[3], quadrado[0])
    ]

# Parâmetros
L = 10
pontos = 5
evitar = [(0, 100), (100, 0)]

# Geração de quadrados
sla1, sla2, quadrados = gerar_pontos(pontos, evitar)

# Concatenação dos pontos para visualização
sla1_final = [-15, 115]
sla2_final = [115, -15]
for i in range(len(sla1)):
    sla1_final.append(sla1[i])
    sla2_final.append(sla2[i])

# Preparar obstáculos como arestas
obstaculos_arestas = []
for quad in quadrados:
    obstaculos_arestas.append(quadrado_para_arestas(quad))

# Gerar conexões possíveis entre os vértices
todos_os_pontos = [(-15, 115), (115, -15)] + [(sla1[i], sla2[i]) for i in range(len(sla1))]
linhas_validas = []

for i in range(len(todos_os_pontos)):
    for j in range(i+1, len(todos_os_pontos)):
        p1 = todos_os_pontos[i]
        p2 = todos_os_pontos[j]
        segmento = (p1, p2)
        if not is_intersecting(segmento, obstaculos_arestas):
            linhas_validas.append(segmento)

# Plotagem
plt.figure(figsize=(10, 10))
plt.xlim(-20, 120)
plt.ylim(-20, 120)

# Pontos
area = [10] * len(sla2_final)
plt.scatter(sla1_final, sla2_final, c='red', s=area, zorder=5, label='Pontos')

# Obstáculos
for quadrado in quadrados:
    x_vals = [p[0] for p in quadrado] + [quadrado[0][0]]
    y_vals = [p[1] for p in quadrado] + [quadrado[0][1]]
    plt.plot(x_vals, y_vals, color='blue')

# Caminhos válidos
for linha in linhas_validas:
    x_vals = [linha[0][0], linha[1][0]]
    y_vals = [linha[0][1], linha[1][1]]
    plt.plot(x_vals, y_vals, color='green', linewidth=0.8, zorder=1)

plt.title("Caminhos Válidos entre Pontos sem Interseção com Obstáculos")
plt.grid(True)
plt.legend()
plt.show()
