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

def mesmos_pontos_do_quadrado(p1, p2, quadrado):
    return p1 in quadrado and p2 in quadrado

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
    x1, y1 = quadrado[0]
    x2, y2 = quadrado[1]
    x3, y3 = quadrado[2]
    x4, y4 = quadrado[3]

    xmin = min(x1, x2, x3, x4)
    xmax = max(x1, x2, x3, x4)
    ymin = min(y1, y2, y3, y4)
    ymax = max(y1, y2, y3, y4)

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
        p5 = (x, y)
        valido = True
        for quadrado in quadrados:
            for ponto in [p1, p2, p3, p4]:
                if ponto_dentro_do_quadrado(ponto[0], ponto[1], quadrado):
                    valido = False
                    break
            if not valido:
                break
        if valido:
            sla1.extend([p1[0], p2[0], p3[0], p4[0], p5[0]])
            sla2.extend([p1[1], p2[1], p3[1], p4[1], p5[1]])
            quadrados.append([p1, p2, p3, p4])
            gerados += 1

    return sla1, sla2, quadrados

L = 10
pontos = 6
evitar = [(0, 100), (100, 0)]
sla1, sla2, quadrados = gerar_pontos(pontos, evitar)

sla1_final = [-15, 115]
sla2_final = [115, -15]

for i in range(len(sla1)):
    sla1_final.append(sla1[i])
    sla2_final.append(sla2[i])

plt.figure(figsize=(10, 10))
plt.xlim(-20, 120)
plt.ylim(-20, 120)

area = [10] * len(sla2_final)
plt.scatter(sla1_final, sla2_final, c='red', s=area, zorder=5, label='Pontos')

for i in range(0, len(sla1), 5):
    plt.plot(sla1[i:i+5], sla2[i:i+5], color='blue')

for i in range(len(sla1_final)):
    for j in range(i + 1, len(sla1_final)):
        p1 = (sla1_final[i], sla2_final[i])
        p2 = (sla1_final[j], sla2_final[j])

        cruza_algum_lado = False

        for quadrado in quadrados:
            lados_do_quadrado = [
                (quadrado[0], quadrado[1]),
                (quadrado[1], quadrado[2]),
                (quadrado[2], quadrado[3]),
                (quadrado[3], quadrado[0])
            ]
            if mesmos_pontos_do_quadrado(p1, p2, quadrado):
              cruza_algum_lado = True
              break

            for q1, q2 in lados_do_quadrado:
                if intersecta((p1, p2), (q1, q2)):
                    cruza_algum_lado = True
                    break

            if cruza_algum_lado:
                break

        if not cruza_algum_lado:
            plt.plot([p1[0], p2[0]], [p1[1], p2[1]], color='gray', linestyle='--', linewidth=0.5)

plt.gca().set_aspect('equal', adjustable='box')
plt.legend()
plt.show()
