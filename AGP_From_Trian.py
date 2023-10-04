import matplotlib.pyplot as plt
import tripy

"""
#Poligonos probados
polygon = [(0,0),(0,10),(10,10),(10,0)]

polygon = [(0,0),(0,101),(20,100),(30,60),(40,100),(60,100),
(60,0),(40,10),(40,40),(20,40),(20,10)]

polygon = [(-2,3),(3,0),(4,2),(8,0),(14,0),(16,2),(15,8),(13,7),(12,3),(8,8),(14,8),
(9,11),(4,8),(6,5),(2,8.5),(4,11),(0.5,11),(-2,7.5),(2,6),(-3,6),(-2,3)]
"""
polygon = [(87,45), (63,44), (75,36), (68,25), (58,45), (49,36), (54,29),(44,29),(44,22),(60,22),(60,15),
(36,15),(36,-8),(66,-22),(52,4),(65,4),(66,-1),(78,-4),(81,3),(78,17),(89,15),(101,20),(101,31), (87,35)]


#Lista utilizada para los puntos pertenecientes a un triangulo ya utilizado
black_list_points = []

#Funcion que obtiene el punto mas recurrente de una lista de triangulos
def most_freq(poligon, triangles):
    global black_list_points
    max_count = 0
    list = []
    final_list = []
    most = False
    #Se separa cada punto de la lista de triangulos en una lista nueva
    for i in poligon:
        for j in triangles:
            for k in range(0,3):
                #print(j[k])
                if i == j[k]:
                    list.append(j[k])

    #Si existen puntos en la lista negra se eliminan de la lista
    for i in list:
        if i not in black_list_points:
            final_list.append(i)

    #Se busca el punto mas recurrente de la lista
    for i in final_list:
        current = final_list.count(i)
        if(current > max_count):
            max_count = current
            most = i
    return most

#Funcion que remueve todos los triangulos que contengan el punto mas frecuente
# ademas agrega a la lista negra los puntos pertenecientes a dichos triangulos
def remove_triangles(triangles, point):
    list = []
    black_list_triangles = []
    #Se eliminan los triangulos que contienen el punto mas frecuente
    for i in triangles:
        if point in i:
            black_list_triangles.append(i)
        else:
            list.append(i)
    global black_list_points

    #Se agregan a la lista negra los puntos de dichos triangulos
    for i in black_list_triangles:
        for j in i:
            if j not in black_list_points:
                black_list_points.append(j)

    return list

#Funcion que obtiene las camaras a colocar
def final_cameras(polygon, triangles):
    cameras = []
    #Mientras existan triangulaciones
    while triangles != []:
        #Se busca el punto mas frecuente de las triangulaciones
        m = most_freq(polygon, triangles)
        if not m:
            break
        
        #Se agrega el punto a la lista de camaras
        #print("\nMost f : ", m)
        cameras.append(m)
        #Se eliminan las triangulaciones que contengan dicho punto
        triangles = remove_triangles(triangles, m)
        #print("\nTriangles: ", triangles)
    return cameras

#Funcion que grafica el poligono, las triangulaciones y las camaras
def find_and_graph(polygon):
    #print("Polygon: ", polygon)
    #Se obtiene triangulacion
    triangles = tripy.earclip(polygon)
    #print("Triangles: ", triangles)
    
    #Listas de puntos utilizadas para graficar el poligono
    plot_poligonx = [];  plot_poligony = []
    for i in polygon:
        #Se obtiene las coordenadas en x del poligono
        plot_poligonx.append(i[0])
        #Se obtiene las coordenadas en y del poligono
        plot_poligony.append(i[1])
    
    #Se agrega el primer punto de nuevo
    plot_poligonx.append(plot_poligonx[0])
    plot_poligony.append(plot_poligony[0])
    
    #Listas de puntos utilizadas para graficar las triangulaciones
    plot_trianglex = []; plot_triangley = []

    for i in triangles:
        aux_trianglex = []
        aux_triangley = []
        for j in i:
            #Se obtiene las coordenadas en x de la triangulacion
            aux_trianglex.append(j[0])
            #Se obtiene las coordenadas en y de la triangulacion
            aux_triangley.append(j[1])
        aux_trianglex.append(i[0][0])
        aux_triangley.append(i[0][1])

        plot_trianglex.append(aux_trianglex)
        plot_triangley.append(aux_triangley)

    #Se obtiene la lista de camaras
    cameras = final_cameras(polygon, triangles)

    #Listas de puntos utilizadas para graficar las camaras
    plot_camerax = []; plot_cameray = []
    for i in cameras:
        plot_camerax.append(i[0])
        plot_cameray.append(i[1])

    #Se grafican las camaras
    plt.scatter(plot_camerax, plot_cameray, marker=".", s=500, color='k')
    #plt.plot(plot_trianglex, plot_triangley, color='g', alpha=0.3)

    #Se grafican las triangulaciones
    for i in range(len(plot_trianglex)):
        plt.plot(plot_trianglex[i], plot_triangley[i], color='g', alpha=0.1)
    
    #Se grafica el poligono
    plt.plot(plot_poligonx, plot_poligony, color='b')
    
    return plt.show()
    
find_and_graph(polygon)
