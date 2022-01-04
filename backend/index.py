from re import X
from flask import Flask, render_template, json, jsonify,request
from flask_cors import CORS
from scipy.sparse import data

from werkzeug.utils import secure_filename


''' Analisis '''
import pandas as pd
import numpy as np
import matplotlib.pyplot as plot
from sklearn.linear_model import LinearRegression  
from sklearn.preprocessing import PolynomialFeatures 
from sklearn.metrics import mean_squared_error, r2_score

import base64
import os
''' Fin'''
app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/Carga_Reporte', methods = ['POST']) 
def Carga():
    global dataset
    Datos =  request.files['files']  
    Nombre = secure_filename(Datos.filename)
    ext = os.path.splitext(Nombre) 
    
    if ext[1]=='.csv':
        dataset = pd.read_csv(Datos,encoding='latin-1')  
    elif ext[1] == '.json':
        dataset = pd.read_json(Datos)
    elif ext[1] == '.xlsx':
        dataset = pd.read_excel(Datos)
    else:
        dataset = pd.read_excel(Datos)

    #df2 = dataset[dataset['Country/Region'] == 'Guatemala']
    print(dataset)
    return jsonify({"message":"ARCHIVO RECIBIDO"})

#Tendencia de la infección por Covid-19 en un País.
@app.route('/Analisis_Reporte1', methods = ['POST']) 
def Reporte1():
    body = {
        "var1":request.json['var1'],
        "var2":request.json['var2'],
        "var3":request.json['var3']
    }   
    encabezadoPais = body['var1']
    pais = body['var2']
    encabezadoConfirmados = body['var3']
    #Dias = int(dias) 
    print(body)
    # data 
    
    ''' comienza filtro para pais'''
    print(encabezadoPais)

    Datos =  dataset.loc[dataset[encabezadoPais]==pais]
    Datos = pd.DataFrame(Datos)
    

    Todosinfectados = Datos[encabezadoConfirmados]

    print(Todosinfectados.count())
    vdias = []
    t= 0
    for i in range(Todosinfectados.count()):
        vdias.append(i)
    
    print(vdias)
    Dias = Todosinfectados.count()
    print(Dias)
    vinfectados = []
    for z in range(Dias):
        vinfectados.append(Todosinfectados.iloc[z])
    print(vinfectados)
    '''BusquedaPais = dataset[encabezadoPais]
    print(pais)
    for i in dataset.index:
        if(BusquedaPais[i] == pais):
            index_Fil = i


    Fil = dataset.iloc[index_Fil,:]
    vinfectados = []

    for z in range(Dias):
        val = 4+z
        vinfectados.append(Fil.iloc[val])
    print(vinfectados)
    
    '''
    vinfectados = vinfectados.replace(np.nan,0)
    y_new_max = max(vinfectados)
    x = np.asarray(vdias)[:,np.newaxis]
    y = np.asarray(vinfectados)[:,np.newaxis]
    plot.scatter(x,y)
    # Transformar a regresion
    poly_degree = 3
    polynomial_features = PolynomialFeatures(degree = poly_degree)
    x_transform = polynomial_features.fit_transform(x)

    # ajustar el modelo
    model = LinearRegression().fit(x_transform, y)
    y_new = model.predict(x_transform)

    # calculate rmse and r2
    rmse = np.sqrt(mean_squared_error(y, y_new))
    r2 = r2_score(y, y_new)
    print('RMSE: ', rmse)
    print('R2: ', r2)
    val_rmse = rmse
    val_r2 = r2

    # Prediccion desde el dia 0 hasta el dia 50
    x_new_min = 0.0
    x_new_max = int(Dias)

    x_new = np.linspace(x_new_min, x_new_max, int(Dias))
    x_new = x_new[:,np.newaxis]

    x_new_transform = polynomial_features.fit_transform(x_new)
    y_new = model.predict(x_new_transform)

    # Plot de la grafica
    #dataset.plot(x='Dias', y='Infectados', style='o')
    plot.plot(x_new, y_new, color='coral', linewidth=3)
    plot.grid()
    plot.xlim(x_new_min,x_new_max)
    plot.ylim(0,y_new_max)
    title = 'Degree = {}; RMSE = {}; R2 = {}'.format(poly_degree, round(rmse,2), round(r2,2))
    plot.title('Tendencia de la infección por Covid-19 en '+pais+"\n " + title, fontsize=10)
    plot.xlabel('Dias')
    plot.ylabel('Infectados')
    plot.legend(('Regresion Poliminomial','Datos'))

    # use savefig() before show().
    plot.savefig("Reporte1.png")
    with open("Reporte1.png", "rb") as img_file:
        my_string =  base64.b64encode(img_file.read())
    #print(my_string.decode('utf-8'))
    #plot.show()
    img_file.close()
    plot.close()
    if round(val_r2) == 1:
        descripcionr2='es cercano a 1 Podemos concluir que el modelo lineal es adecuado para describir la relación que existe entre estas variables '
    else: 
        descripcionr2='es cercano a 0 Podemos concluir que el modelo lineal no es representativo lo que supone que el modelo no explica nada de la variación total de la variable Y ' 

    conclusion = 'Tendencia infeccion de Covid-19 en '+pais + ' la ejecucion se hara con respecto a infectados por dias  al ejecutarlo podremos prever la tendencia en los proximos meses si ira de alta o habra una baja.\n Al relizar la ejecucion podremos observar el valor RMSE: ' + str(val_rmse) +' nos da el error de 2 conjuntos entre los predichos y observados o conocidos, el R2:' + str(val_r2) +' ' + descripcionr2
    NombreReport = 'Tendencia infeccion de Covid-19 en '+pais 
    #plot.show()
    return jsonify({"message":"Analisis Realizado de Reporte1","image64":my_string.decode('utf-8'),"conclusion":conclusion,"NombreReport":NombreReport,"Grado":str(poly_degree),"rmse":str(val_rmse),"r2":str(val_r2)})
 
#Predicción de Infectados en un País.
@app.route('/Analisis_Reporte2', methods = ['POST']) 
def Reporte2():
    body = {
        "var1":request.json['var1'],
        "var2":request.json['var2'],
        "var3":request.json['var3'],
        "var4":request.json['var4']
    }   
    encabezadoPais = body['var1']
    pais = body['var2']
    encabezadoConfirmados = body['var3']
    dias = body['var4']
    DiasPredicion = int(dias)
    print(DiasPredicion)
    print(body)
    # data 
   
    ''' comienza filtro para pais''' 
    print(encabezadoPais)

    Datos =  dataset.loc[dataset[encabezadoPais]==pais]
    Datos = pd.DataFrame(Datos)

    Todosinfectados = Datos[encabezadoConfirmados]
    print(Todosinfectados.count())
    vdias = []
    t= 0
    for i in range(Todosinfectados.count()):
        vdias.append(i)
    
    print(vdias)
    Dias = Todosinfectados.count()
    print(Dias)
    vinfectados = []
    for z in range(Dias):
        vinfectados.append(Todosinfectados.iloc[z])
    print(vinfectados)

    y_new_max = max(vinfectados)
    x = np.asarray(vdias)[:,np.newaxis]
    y = np.asarray(vinfectados)[:,np.newaxis]
    plot.scatter(x,y)
    # Predecimos la Data
    poly_degree = 4
    polynomial_features = PolynomialFeatures(degree = poly_degree)
    x_transform = polynomial_features.fit_transform(x)

    # Procedemos a entrenar el modelo
    model = LinearRegression().fit(x_transform, y)
    # calculamos la varianza ,rmse y r2
    y_new = model.predict(x_transform)
    rmse = np.sqrt(mean_squared_error(y, y_new))
    r2 = r2_score(y, y_new)

    print('RMSE: ', rmse)
    print('R2: ', r2)
    val_rmse = rmse
    val_r2 = r2

    # Prediccion desde el dia 0 hasta el dia que solicite
    x_new_min = 0.0
    x_new_max = DiasPredicion


    x_new = np.linspace(x_new_min, x_new_max, Dias)
    x_new = x_new[:,np.newaxis]

    x_new_transform = polynomial_features.fit_transform(x_new)
    y_new = model.predict(x_new_transform)
    prediction = y_new[np.size(y_new)-1]
    # Plot de la grafica
    #dataset.plot(x='Dias', y='Infectados', style='o')
    plot.plot(x_new, y_new, color='red', linewidth=3)
    plot.grid()
    plot.xlim(x_new_min,x_new_max)
    plot.ylim(0,y_new_max)
    title = 'Degree = {}; RMSE = {}; R2 = {}'.format(poly_degree, round(rmse,2), round(r2,2))
    plot.title('Predicción de Infectados en  '+pais+' a una prediccion '+ str(DiasPredicion) + ' dias'"\n " + title, fontsize=10)
    plot.xlabel('Dias')
    plot.ylabel('Infectados')

    plot.legend(('Regresion Poliminomial','Datos'))
    # use savefig() before show().
    plot.savefig("Reporte2.png")
    with open("Reporte2.png", "rb") as img_file:
        my_string =  base64.b64encode(img_file.read())
    img_file.close()
    plot.close()
    #print(my_string.decode('utf-8'))
    #plot.show()
    if round(val_r2) == 1:
        descripcionr2='es cercano a 1 Podemos concluir que el modelo lineal es adecuado para describir la relación que existe entre estas variables '
    else: 
        descripcionr2='es cercano a 0 Podemos concluir que el modelo lineal no es representativo lo que supone que el modelo no explica nada de la variación total de la variable Y ' 

    NombreReport = 'Predicción de Infectados en '+pais +' a una prediccion '+ str(DiasPredicion) + ' dias'
    conclusion = 'Predicción de Infectados en '+pais +' a una prediccion'+ str(DiasPredicion) + ' dias la ejecucion se hara con respecto a infectados por dias  al ejecutarlo podremos ver la prediccion la cual es '+str(prediction)+' de infectados en los '+str(DiasPredicion) +' si ira de alta o habra una baja.\n Al relizar la ejecucion podremos observar el valor RMSE: ' + str(val_rmse) +' nos da el error de 2 conjuntos entre los predichos y observados o conocidos, el R2:' + str(val_r2) +' ' + descripcionr2
    return jsonify({"message":"Analisis Realizado de Reporte2","image64":my_string.decode('utf-8'),"conclusion":conclusion,"NombreReport":NombreReport,"Grado":str(poly_degree),"rmse":str(val_rmse),"r2":str(val_r2),"prediccion":str(prediction)})

#Indice de Progresión de la pandemia.                       
@app.route('/Analisis_Reporte3', methods = ['POST']) 
def Reporte3():
    body = {
        "var3":request.json['var3']
    }
    encabezadoConfirmados = body['var3']
    
    print(body)
    # data 
    
    ''' comienza filtro para pais''' 
    print(encabezadoConfirmados)

    Datos =  dataset[encabezadoConfirmados]
    #Datos = pd.DataFrame(Datos)

    print(Datos.count()) 

    vdias = []    
    for i in range(Datos.count()):
        vdias.append(i)
    
    #print(vdias)
    Dias = Datos.count()
    print(Dias)
    vconfirmados = []
    for z in range(Dias):
        vconfirmados.append(Datos.iloc[z])
    #print(vmuertos)

    y_new_max = max(vconfirmados)
    x = np.asarray(vdias)[:,np.newaxis]
    y = np.asarray(vconfirmados)[:,np.newaxis]


    # Procedemos a entrenar el modelo
    model = LinearRegression().fit(x, y)
    # calculamos la varianza ,rmse y r2
    y_new = model.predict(x)

    rmse = np.sqrt(mean_squared_error(y, y_new))
    r2 = r2_score(y, y_new)

    print('RMSE: ', rmse)
    print('R2: ', r2)


    # Prediccion desde el dia 0 hasta el dia que solicite
    x_new_min = 0.0
    x_new_max = Dias

    # Plot de la grafica
    plot.xlim(x_new_min, x_new_max, Dias)
    plot.ylim(0,y_new_max+5000)

    plot.grid()
   
    title = 'Modelo : Y = {}; X+{};RMSE = {}; R2 = {}'.format(str(model.coef_[0][0]),str(model.intercept_[0]),round(rmse,2), round(r2,2))
    plot.title('Indice de Progresión de la pandemia \n' + title, fontsize=10)
    plot.xlabel('Dias')
    plot.ylabel('No. Casos Confirmados')
    plot.scatter(x, y)
    plot.plot(x, y_new, color='red')
    plot.legend(('Regresion Lineal','Datos'))


    # use savefig() before show().
    plot.savefig("Reporte3.png")
    with open("Reporte3.png", "rb") as img_file:
        my_string =  base64.b64encode(img_file.read())
    img_file.close()
    plot.close()
    #plot.show()
    if round(r2) == 1:
        descripcionr2='es cercano a 1 Podemos concluir que el modelo lineal es adecuado para describir la relación que existe entre estas variables '
    else: 
        descripcionr2='es cercano a 0 Podemos concluir que el modelo lineal no es representativo lo que supone que el modelo no explica nada de la variación total de la variable Y ' 

    NombreReport = 'Indice de Progresión de la pandemia'
    conclusion = 'Indice de Progresión de la pandemia con un Modelo : Y = {}; X+{}; RMSE = {}; R2 = {}'.format(str(model.coef_[0][0]),str(model.intercept_[0]),round(rmse,2), round(r2,2)) + ' RMSE nos da el error de 2 conjuntos entre los predichos y observados o conocidos y R2 '+descripcionr2
    return jsonify({"message":"Analisis Realizado de Reporte 3","image64":my_string.decode('utf-8'),"conclusion":conclusion,"NombreReport":NombreReport,"rmse":str(rmse),"r2":str(r2),"modelo":'Y ='+str(model.coef_[0][0])+' X+'+str(model.intercept_[0])})

#Predicción de mortalidad por COVID en un Departamento.
@app.route('/Analisis_Reporte4', methods = ['POST']) 
def Reporte4():
    body = {
        "var6":request.json['var6'],
        "var7":request.json['var7'],
        "var4":request.json['var4'],
        "var5":request.json['var5']
    }   
    encabezadoDepartamento = body['var6']
    departamento = body['var7']
    encabezadoMuertes = body['var5']
    dias = body['var4']
    DiasPredicion = int(dias)
    print(DiasPredicion)
    print(body)
    # data 
    
    ''' comienza filtro para pais''' 
    print(encabezadoDepartamento)

    Datos =  dataset.loc[dataset[encabezadoDepartamento]==departamento]
    Datos = pd.DataFrame(Datos)

    Todosinfectados = Datos[encabezadoMuertes]
    print(Todosinfectados.count())
    vdias = []
    for i in range(Todosinfectados.count()):
        vdias.append(i)
    
    #print(vdias)
    Dias = Todosinfectados.count()
    print(Dias)
    vinfectados = []
    for z in range(Dias):
        vinfectados.append(Todosinfectados.iloc[z])
    #print(vinfectados)

    y_new_max = max(vinfectados)
    x = np.asarray(vdias)[:,np.newaxis]
    y = np.asarray(vinfectados)[:,np.newaxis]
    plot.scatter(x,y)
    # Predecimos la Data
    poly_degree = 4
    polynomial_features = PolynomialFeatures(degree = poly_degree)
    x_transform = polynomial_features.fit_transform(x)

    # Procedemos a entrenar el modelo
    model = LinearRegression().fit(x_transform, y)
    # calculamos la varianza ,rmse y r2
    y_new = model.predict(x_transform)
    rmse = np.sqrt(mean_squared_error(y, y_new))
    r2 = r2_score(y, y_new)

    print('RMSE: ', rmse)
    print('R2: ', r2)
    val_rmse = rmse
    val_r2 = r2

    # Prediccion desde el dia 0 hasta el dia que solicite
    x_new_min = 0.0
    x_new_max = DiasPredicion


    x_new = np.linspace(x_new_min, x_new_max, Dias)
    x_new = x_new[:,np.newaxis]

    x_new_transform = polynomial_features.fit_transform(x_new)
    y_new = model.predict(x_new_transform)
    prediction = y_new[np.size(y_new)-1]
    # Plot de la grafica
    #dataset.plot(x='Dias', y='Infectados', style='o')
    plot.plot(x_new, y_new, color='red', linewidth=3)
    plot.grid()
    plot.xlim(x_new_min,x_new_max)
    plot.ylim(0,y_new_max+100)
    title = 'Degree = {}; RMSE = {}; R2 = {}'.format(poly_degree, round(rmse,2), round(r2,2))
    plot.title('Predicción de mortalidad por Covid-19 en el Departamento de  '+departamento+"\n " + title, fontsize=10)
    plot.xlabel('Dias')
    plot.ylabel('Muertes')

    plot.legend(('Regresion Poliminomial','Datos'))
    # use savefig() before show().
    plot.savefig("Reporte4.png")
    with open("Reporte4.png", "rb") as img_file:
        my_string =  base64.b64encode(img_file.read())
    img_file.close() 
    plot.close()
    #plot.show()
    if round(val_r2) == 1:
        descripcionr2='es cercano a 1 Podemos concluir que el modelo lineal es adecuado para describir la relación que existe entre estas variables '
    else: 
        descripcionr2='es cercano a 0 Podemos concluir que el modelo lineal no es representativo lo que supone que el modelo no explica nada de la variación total de la variable Y ' 

    NombreReport = 'Predicción de mortalidad por Covid-19 en el Departamento de '+departamento +' a una prediccion'+ str(DiasPredicion) + ' dias'
    conclusion = 'Predicciónde mortalidad por Covid-19 en el Departamento de '+departamento +' a una prediccion'+ str(DiasPredicion) + ' dias la ejecucion se hara con respecto a muertes de un departamento por dias  al ejecutarlo podremos ver la prediccion la cual es '+str(prediction)+' de mortalidad en los '+str(DiasPredicion) +' si ira de alta o habra una baja.\n Al relizar la ejecucion podremos observar el valor RMSE: ' + str(val_rmse) +' nos da el error de 2 conjuntos entre los predichos y observados o conocidos, el R2:' + str(val_r2) +' ' + descripcionr2
    return jsonify({"message":"Analisis Realizado de Reporte4","image64":my_string.decode('utf-8'),"conclusion":conclusion,"NombreReport":NombreReport,"Grado":str(poly_degree),"rmse":str(val_rmse),"r2":str(val_r2),"prediccion":str(prediction)})

#Predicción de mortalidad por COVID en un País.
@app.route('/Analisis_Reporte5', methods = ['POST']) 
def Reporte5():
    body = {
        "var1":request.json['var1'],
        "var2":request.json['var2'],
        "var4":request.json['var4'],
        "var5":request.json['var5']
    }   
    encabezadoPais = body['var1']
    pais = body['var2']
    encabezadoMuertes = body['var5']
    dias = body['var4']
    DiasPredicion = int(dias)
    print(DiasPredicion)

    print(body)
    # data 
    
    ''' comienza filtro para pais''' 
    print(encabezadoPais)

    Datos =  dataset.loc[dataset[encabezadoPais]==pais]
    Datos = pd.DataFrame(Datos)

    Todosinfectados = Datos[encabezadoMuertes]
    print(Todosinfectados.count())
    vdias = []
    t= 0
    for i in range(Todosinfectados.count()):
        vdias.append(i)
    
    print(vdias)
    Dias = Todosinfectados.count()
    print(Dias)
    vinfectados = []
    for z in range(Dias):
        vinfectados.append(Todosinfectados.iloc[z])
    #print(vinfectados)

    y_new_max = max(vinfectados)
    x = np.asarray(vdias)[:,np.newaxis]
    y = np.asarray(vinfectados)[:,np.newaxis]
    plot.scatter(x,y)
    # Predecimos la Data
    poly_degree = 4 # duda del grado de la polinomia revisar
    polynomial_features = PolynomialFeatures(degree = poly_degree)
    x_transform = polynomial_features.fit_transform(x)

    # Procedemos a entrenar el modelo
    model = LinearRegression().fit(x_transform, y)
    # calculamos la varianza ,rmse y r2
    y_new = model.predict(x_transform)
    rmse = np.sqrt(mean_squared_error(y, y_new))
    r2 = r2_score(y, y_new)

    print('RMSE: ', rmse)
    print('R2: ', r2)
    val_rmse = rmse
    val_r2 = r2

    # Prediccion desde el dia 0 hasta el dia que solicite
    x_new_min = 0.0
    x_new_max = DiasPredicion


    x_new = np.linspace(x_new_min, x_new_max, Dias)
    x_new = x_new[:,np.newaxis]

    x_new_transform = polynomial_features.fit_transform(x_new)
    y_new = model.predict(x_new_transform)
    prediction = y_new[np.size(y_new)-1]
    # Plot de la grafica
    #dataset.plot(x='Dias', y='Infectados', style='o')
    plot.plot(x_new, y_new, color='red', linewidth=3)
    plot.grid()
    plot.xlim(x_new_min,x_new_max)
    plot.ylim(0,y_new_max)
    title = 'Degree = {}; RMSE = {}; R2 = {}'.format(poly_degree, round(rmse,2), round(r2,2))
    plot.title('Predicción de mortalidad por Covid-19 en  '+pais+"\n " + title, fontsize=10)
    plot.xlabel('Dias')
    plot.ylabel('Muertes')
    plot.legend(('Regresion Poliminomial','Datos'))
    # use savefig() before show().
    plot.savefig("Reporte5.png")
    with open("Reporte5.png", "rb") as img_file:
        my_string =  base64.b64encode(img_file.read())
    img_file.close()
    plot.close()
    #plot.show()
    if round(val_r2) == 1:
        descripcionr2='es cercano a 1 Podemos concluir que el modelo lineal es adecuado para describir la relación que existe entre estas variables '
    else: 
        descripcionr2='es cercano a 0 Podemos concluir que el modelo lineal no es representativo lo que supone que el modelo no explica nada de la variación total de la variable Y ' 

    NombreReport = 'Predicción de mortalidad por Covid-19 en el Pais de '+pais +' a una prediccion'+ str(DiasPredicion) + ' dias'
    conclusion = 'Predicciónde mortalidad por Covid-19 en el Pais de '+pais +' a una prediccion'+ str(DiasPredicion) + ' dias la ejecucion se hara con respecto a muertes de un pais por dias  al ejecutarlo podremos ver la prediccion la cual es '+str(prediction)+' de mortalidad en los '+str(DiasPredicion) +' si ira de alta o habra una baja.\n Al relizar la ejecucion podremos observar el valor RMSE: ' + str(val_rmse) +' nos da el error de 2 conjuntos entre los predichos y observados o conocidos, el R2:' + str(val_r2) +' ' + descripcionr2
    return jsonify({"message":"Analisis Realizado de Reporte5","image64":my_string.decode('utf-8'),"conclusion":conclusion,"NombreReport":NombreReport,"Grado":str(poly_degree),"rmse":str(val_rmse),"r2":str(val_r2),"prediccion":str(prediction)})

#Análisis del número de muertes por coronavirus en un País.
@app.route('/Analisis_Reporte6', methods = ['POST']) 
def Reporte6():
    body = {
        "var1":request.json['var1'],
        "var2":request.json['var2'],
        "var5":request.json['var5']
    }
    encabezadoPais = body['var1']   
    pais = body['var2']
    encabezadoMuertes = body['var5']
    
    print(body)
    # data 
    
    ''' comienza filtro para pais''' 
    print(encabezadoPais)

    Datos =  dataset.loc[dataset[encabezadoPais]==pais]
    Datos = pd.DataFrame(Datos)

    TodosMuertos = Datos[encabezadoMuertes]
    print(TodosMuertos.count()) 
    print(encabezadoMuertes)

    vdias = []    
    for i in range(TodosMuertos.count()):
        vdias.append(i)
    
    #print(vdias)
    Dias = TodosMuertos.count()
    print(Dias)
    vmuertos = []
    for z in range(Dias):
        vmuertos.append(TodosMuertos.iloc[z])
    #print(vmuertos)

    y_new_max = max(vmuertos)
    x = np.asarray(vdias)[:,np.newaxis]
    y = np.asarray(vmuertos)[:,np.newaxis]


    # Procedemos a entrenar el modelo
    model = LinearRegression().fit(x, y)
    # calculamos la varianza ,rmse y r2
    y_new = model.predict(x)

    rmse = np.sqrt(mean_squared_error(y, y_new))
    r2 = r2_score(y, y_new)

    print('RMSE: ', rmse)
    print('R2: ', r2)


    # Prediccion desde el dia 0 hasta el dia que solicite
    x_new_min = 0.0
    x_new_max = Dias

    # Plot de la grafica
    plot.xlim(x_new_min, x_new_max, Dias)
    plot.ylim(0,y_new_max)

    plot.grid()
   
    title = 'Modelo : Y = {}; X+{}; RMSE = {}; R2 = {}'.format(str(model.coef_[0][0]),str(model.intercept_[0]),round(rmse,2), round(r2,2))
    plot.title('Análisis del número de muertes por coronavirus en '+pais+"\n " + title, fontsize=10)
    plot.xlabel('Dias')
    plot.ylabel('No. Total de Muertes')
    plot.scatter(x, y)
    plot.plot(x, y_new, color='red')
    plot.legend(('Regresion Lineal','Datos'))
    # use savefig() before show().
    plot.savefig("Reporte6.png")
    with open("Reporte6.png", "rb") as img_file:
        my_string =  base64.b64encode(img_file.read())
    img_file.close()
    plot.close()
    #plot.show()
    if round(r2) == 1:
        descripcionr2='es cercano a 1 Podemos concluir que el modelo lineal es adecuado para describir la relación que existe entre estas variables '
    else: 
        descripcionr2='es cercano a 0 Podemos concluir que el modelo lineal no es representativo lo que supone que el modelo no explica nada de la variación total de la variable Y ' 

    NombreReport = 'Análisis del número de muertes por coronavirus en '+pais 
    conclusion = 'Análisis del número de muertes por coronavirus en '+pais +' Modelo : Y = {}; X+{}; RMSE = {}; R2 = {}'.format(str(model.coef_[0][0]),str(model.intercept_[0]),round(rmse,2), round(r2,2)) + ' RMSE nos da el error de 2 conjuntos entre los predichos y observados o conocidos y R2 '+descripcionr2
    return jsonify({"message":"Analisis Realizado de Reporte 6","image64":my_string.decode('utf-8'),"conclusion":conclusion,"NombreReport":NombreReport,"rmse":str(rmse),"r2":str(r2),"modelo":'Y ='+str(model.coef_[0][0])+' X+'+str(model.intercept_[0])})


#Tendencia del número de infectados por día de un País.
@app.route('/Analisis_Reporte7', methods = ['POST']) 
def Reporte7():
    body = {
        "var1":request.json['var1'],
        "var2":request.json['var2'],
        "var3":request.json['var3'],
        "var4":request.json['var4']
    }   
    encabezadoPais = body['var1']
    pais = body['var2']
    encabezadoConfirmados = body['var3']
    dias = body['var4']
    Dias = int(dias) 
    print(body)
    # data 
    vdias = []
    for i in range(Dias):
        vdias.append(i)
    
    print(vdias)
    print(Dias)
    ''' comienza filtro para pais'''
    print(encabezadoPais)

    Datos =  dataset.loc[dataset[encabezadoPais]==pais]
    Datos = pd.DataFrame(Datos)

    Todosinfectados = Datos[encabezadoConfirmados]
    vinfectados = []
    for z in range(Dias):
        vinfectados.append(Todosinfectados.iloc[z])
    print(vinfectados)
    '''BusquedaPais = dataset[encabezadoPais]
    print(pais)
    for i in dataset.index:
        if(BusquedaPais[i] == pais):
            index_Fil = i
    Fil = dataset.iloc[index_Fil,:]
    vinfectados = []
    for z in range(Dias):
        val = 4+z
        vinfectados.append(Fil.iloc[val])
    print(vinfectados)
    
    '''
    y_new_max = max(vinfectados)
    x = np.asarray(vdias)[:,np.newaxis]
    y = np.asarray(vinfectados)[:,np.newaxis]
    plot.scatter(x,y)
    # Transformar a regresion
    poly_degree = 3
    polynomial_features = PolynomialFeatures(degree = poly_degree)
    x_transform = polynomial_features.fit_transform(x)

    # ajustar el modelo
    model = LinearRegression().fit(x_transform, y)
    y_new = model.predict(x_transform)

    # calculate rmse and r2
    rmse = np.sqrt(mean_squared_error(y, y_new))
    r2 = r2_score(y, y_new)
    print('RMSE: ', rmse)
    print('R2: ', r2)


    # Prediccion desde el dia 0 hasta el dia 50
    x_new_min = 0.0
    x_new_max = int(dias)

    x_new = np.linspace(x_new_min, x_new_max, int(dias))
    x_new = x_new[:,np.newaxis]

    x_new_transform = polynomial_features.fit_transform(x_new)
    y_new = model.predict(x_new_transform)

    # Plot de la grafica
    #dataset.plot(x='Dias', y='Infectados', style='o')
    plot.plot(x_new, y_new, color='coral', linewidth=3)
    plot.grid()
    plot.xlim(x_new_min,x_new_max)
    plot.ylim(0,y_new_max)
    title = 'Degree = {}; RMSE = {}; R2 = {}'.format(poly_degree, round(rmse,2), round(r2,2))
    plot.title('Tendencia de la infección por Covid-19 en '+pais+"\n " + title, fontsize=10)
    plot.xlabel('Dias')
    plot.ylabel('Infectados')
 
    plot.legend(('Regresion Poliminomial','Datos'))
    # use savefig() before show().
    plot.savefig("Reporte7.png")
    with open("Reporte7.png", "rb") as img_file:
        my_string =  base64.b64encode(img_file.read())
    img_file.close()
    plot.close()
    #plot.show()
    if round(r2) == 1:
        descripcionr2='es cercano a 1 Podemos concluir que el modelo lineal es adecuado para describir la relación que existe entre estas variables '
    else: 
        descripcionr2='es cercano a 0 Podemos concluir que el modelo lineal no es representativo lo que supone que el modelo no explica nada de la variación total de la variable Y ' 

    conclusion = 'Tendencia infeccion de Covid-19 por '+dias + ' dias en '+pais + ' la ejecucion se hara con respecto a infectados por '+dias + '  al ejecutarlo podremos prever la tendencia que puede alcanzar proximos meses si ira de alta o habra una baja.\n Al realizar la ejecucion podremos observar el valor RMSE: ' + str(rmse) +' nos da el error de 2 conjuntos entre los predichos y observados o conocidos, el R2:' + str(r2) +' ' + descripcionr2
    NombreReport = 'Tendencia infeccion de Covid-19 por '+dias + ' dias en '+pais
    #plot.show()
    return jsonify({"message":"Analisis Realizado de Reporte7","image64":my_string.decode('utf-8'),"conclusion":conclusion,"NombreReport":NombreReport,"Grado":str(poly_degree),"rmse":str(rmse),"r2":str(r2)})


#Predicción de casos de un país para un año.
@app.route('/Analisis_Reporte8', methods = ['POST']) 
def Reporte8():
    body = {
        "var1":request.json['var1'],
        "var2":request.json['var2'],
        "var3":request.json['var3'],
        #"var4":request.json['var4']
    }   
    encabezadoPais = body['var1']
    pais = body['var2']
    encabezadoConfirmados = body['var3']
    #dias = body['var4']
    #Dias = int(dias) 
    print(body)
    # data 
    
    ''' comienza filtro para pais''' 
    print(encabezadoPais)

    Datos =  dataset.loc[dataset[encabezadoPais]==pais]
    Datos = pd.DataFrame(Datos)

    Todosinfectados = Datos[encabezadoConfirmados]
    vdias = []
    Dias = Todosinfectados.count()
    for i in range(Dias):
        vdias.append(i)
    
    print(vdias)
    print(Dias)
    vinfectados = []
    for z in range(Dias):
        vinfectados.append(Todosinfectados.iloc[z])
    print(vinfectados)

    y_new_max = max(vinfectados)
    x = np.asarray(vdias)[:,np.newaxis]
    y = np.asarray(vinfectados)[:,np.newaxis]
    plot.scatter(x,y)
    # Predecimos la Data
    poly_degree = 4
    polynomial_features = PolynomialFeatures(degree = poly_degree)
    x_transform = polynomial_features.fit_transform(x)

    # Procedemos a entrenar el modelo
    model = LinearRegression().fit(x_transform, y)
    # calculamos la varianza ,rmse y r2
    y_new = model.predict(x_transform)
    rmse = np.sqrt(mean_squared_error(y, y_new))
    r2 = r2_score(y, y_new)

    print('RMSE: ', rmse)
    print('R2: ', r2)
    val_rmse = rmse
    val_r2 = r2

    
    # Prediccion desde el dia 0 hasta el dia que solicite
    x_new_min = 0.0
    x_new_max = 365
    

    x_new = np.linspace(x_new_min, x_new_max, Dias)
    x_new = x_new[:,np.newaxis] 

    x_new_transform = polynomial_features.fit_transform(x_new)
    y_new = model.predict(x_new_transform)
    prediction = y_new[np.size(y_new)-1]
    # Plot de la grafica
    #dataset.plot(x='Dias', y='Infectados', style='o')
    plot.plot(x_new, y_new, color='red', linewidth=3)
    plot.grid()
    plot.xlim(x_new_min,x_new_max)
    plot.ylim(0,y_new_max)
    title = 'Degree = {}; RMSE = {}; R2 = {}'.format(poly_degree, round(rmse,2), round(r2,2))
    plot.title('Predicción de Infectados en  '+pais+' a una prediccion 365 dias'+"\n " + title, fontsize=10)
    plot.xlabel('Dias')
    plot.ylabel('Infectados')

    plot.legend(('Regresion Polinomial','Datos'))
    # use savefig() before show().
    plot.savefig("Reporte8.png")
    with open("Reporte8.png", "rb") as img_file:
        my_string =  base64.b64encode(img_file.read())
    img_file.close()
    plot.close()
    #plot.show()
    if round(val_r2) == 1:
        descripcionr2='es cercano a 1 Podemos concluir que el modelo lineal es adecuado para describir la relación que existe entre estas variables '
    else: 
        descripcionr2='es cercano a 0 Podemos concluir que el modelo lineal no es representativo lo que supone que el modelo no explica nada de la variación total de la variable Y ' 

    NombreReport = 'Predicción de Infectados por Covid-19 en el Pais de '+pais +' a una prediccion 365 dias'
    conclusion = 'Predicciónde Infectados por Covid-19 en el Pais de '+pais +' a una prediccion 365 dias la ejecucion se hara con respecto a Infectados de un pais por 365 dias  al ejecutarlo podremos ver la prediccion la cual es '+str(prediction)+' de mortalidad en los 365 si ira de alta o habra una baja.\n Al relizar la ejecucion podremos observar el valor RMSE: ' + str(val_rmse) +' nos da el error de 2 conjuntos entre los predichos y observados o conocidos, el R2:' + str(val_r2) +' ' + descripcionr2
    return jsonify({"message":"Analisis Realizado de Reporte8","image64":my_string.decode('utf-8'),"conclusion":conclusion,"NombreReport":NombreReport,"Grado":str(poly_degree),"rmse":str(val_rmse),"r2":str(val_r2),"prediccion":str(prediction)})

    
#Tendencia de la vacunación de en un País.
@app.route('/Analisis_Reporte9', methods = ['POST']) 
def Reporte9():
    body = {
        "var1":request.json['var1'],
        "var2":request.json['var2'],
        "var9":request.json['var9']
    }   
    encabezadoPais = body['var1']
    pais = body['var2']
    encabezadoVacunados = body['var9']
    #Dias = int(dias) 
    print(body)
    # data 
    
    ''' comienza filtro para pais'''
    print(encabezadoPais)

    Datos =  dataset.loc[dataset[encabezadoPais]==pais]
    Datos = pd.DataFrame(Datos)
    

    Todosinfectados = Datos[encabezadoVacunados]

    print(Todosinfectados.count())
    vdias = []
    t= 0
    for i in range(Todosinfectados.count()):
        vdias.append(i)
    
    print(vdias)
    Dias = Todosinfectados.count()
    print(Dias)
    vinfectados = []
    for z in range(Dias):
        vinfectados.append(Todosinfectados.iloc[z])
    print(vinfectados)
    
    y_new_max = max(vinfectados)
    x = np.asarray(vdias)[:,np.newaxis]
    y = np.asarray(vinfectados)[:,np.newaxis]
    plot.scatter(x,y)
    # Transformar a regresion
    poly_degree = 3
    polynomial_features = PolynomialFeatures(degree = poly_degree)
    x_transform = polynomial_features.fit_transform(x)

    # ajustar el modelo
    model = LinearRegression().fit(x_transform, y)
    y_new = model.predict(x_transform)

    # calculate rmse and r2
    rmse = np.sqrt(mean_squared_error(y, y_new))
    r2 = r2_score(y, y_new)
    print('RMSE: ', rmse)
    print('R2: ', r2)
    val_rmse = rmse
    val_r2 = r2
    
    # Prediccion desde el dia 0 hasta el dia 50
    x_new_min = 0.0
    x_new_max = int(Dias)

    x_new = np.linspace(x_new_min, x_new_max, int(Dias))
    x_new = x_new[:,np.newaxis]

    x_new_transform = polynomial_features.fit_transform(x_new)
    y_new = model.predict(x_new_transform)

    # Plot de la grafica
    #dataset.plot(x='Dias', y='Infectados', style='o')
    plot.plot(x_new, y_new, color='coral', linewidth=3)
    plot.grid()
    plot.xlim(x_new_min,x_new_max)
    plot.ylim(0,y_new_max)
    title = 'Degree = {}; RMSE = {}; R2 = {}'.format(poly_degree, round(rmse,2), round(r2,2))
    plot.title('Tendencia de Vacunados por Covid-19 en '+pais+"\n " + title, fontsize=10)
    plot.xlabel('Dias')
    plot.ylabel('Vacunados')
 
    plot.legend(('Regresion Poliminomial','Datos'))
    # use savefig() before show().
    plot.savefig("Reporte9.png")
    with open("Reporte9.png", "rb") as img_file:
        my_string =  base64.b64encode(img_file.read())
    img_file.close()
    plot.close()
    #plot.show()
    if round(r2) == 1:
        descripcionr2='es cercano a 1 Podemos concluir que el modelo lineal es adecuado para describir la relación que existe entre estas variables '
    else: 
        descripcionr2='es cercano a 0 Podemos concluir que el modelo lineal no es representativo lo que supone que el modelo no explica nada de la variación total de la variable Y ' 

    conclusion = 'Tendencia de Vacunados por Covid-19  '+pais + ' la ejecucion se hara con respecto a vacunados  al ejecutarlo podremos prever la tendencia que puede alcanzar proximos meses si ira de alta o habra una baja.\n Al realizar la ejecucion podremos observar el valor RMSE: ' + str(rmse) +' nos da el error de 2 conjuntos entre los predichos y observados o conocidos, el R2:' + str(r2) +' ' + descripcionr2
    NombreReport = 'Tendencia de Vacunados por Covid-19  en '+pais
    #plot.show()
    return jsonify({"message":"Analisis Realizado de Reporte9","image64":my_string.decode('utf-8'),"conclusion":conclusion,"NombreReport":NombreReport,"Grado":str(poly_degree),"rmse":str(rmse),"r2":str(r2)})

#Ánalisis Comparativo de Vacunaciópn entre 2 paises.
@app.route('/Analisis_Reporte10', methods = ['POST']) 
def Reporte10():
    body = {
        "var1":request.json['var1'],
        "var2":request.json['var2'],
        "var9":request.json['var9']
    }   
    encabezadoPais = body['var1']
    pais = body['var2']
    encabezadoVacunados = body['var9']
    #Dias = int(dias) 
    print(body)
    # data 
    
    ''' comienza filtro para pais'''
    print(encabezadoPais)

    Datos =  dataset.loc[dataset[encabezadoPais]==pais]
    Datos = pd.DataFrame(Datos)
    

    Todosinfectados = Datos[encabezadoVacunados]

    print(Todosinfectados.count())
    vdias = []
    t= 0
    for i in range(Todosinfectados.count()):
        vdias.append(i)
    
    print(vdias)
    Dias = Todosinfectados.count()
    print(Dias)
    vinfectados = []
    for z in range(Dias):
        vinfectados.append(Todosinfectados.iloc[z])
    print(vinfectados)
    
    y_new_max = max(vinfectados)
    x = np.asarray(vdias)[:,np.newaxis]
    y = np.asarray(vinfectados)[:,np.newaxis]
    plot.scatter(x,y)
    # Transformar a regresion
    poly_degree = 3
    polynomial_features = PolynomialFeatures(degree = poly_degree)
    x_transform = polynomial_features.fit_transform(x)

    # ajustar el modelo
    model = LinearRegression().fit(x_transform, y)
    y_new = model.predict(x_transform)

    # calculate rmse and r2
    rmse = np.sqrt(mean_squared_error(y, y_new))
    r2 = r2_score(y, y_new)
    print('RMSE: ', rmse)
    print('R2: ', r2)
    val_rmse = rmse
    val_r2 = r2
    
    # Prediccion desde el dia 0 hasta el dia 50
    x_new_min = 0.0
    x_new_max = int(Dias)

    x_new = np.linspace(x_new_min, x_new_max, int(Dias))
    x_new = x_new[:,np.newaxis]

    x_new_transform = polynomial_features.fit_transform(x_new)
    y_new = model.predict(x_new_transform)

    # Plot de la grafica
    #dataset.plot(x='Dias', y='Infectados', style='o')
    plot.plot(x_new, y_new, color='coral', linewidth=3)
    plot.grid()
    plot.xlim(x_new_min,x_new_max)
    plot.ylim(0,y_new_max+100)
    title = 'Degree = {}; RMSE = {}; R2 = {}'.format(poly_degree, round(rmse,2), round(r2,2))
    plot.title('Ánalisis Comparativo de Vacunación en '+pais+'\n' + title, fontsize=10)
    plot.xlabel('Dias')
    plot.ylabel('Vacunados')
 


    plot.legend(('Regresion Poliminomial','Datos'))
    # use savefig() before show().
    plot.savefig("Reporte10.png")
    with open("Reporte10.png", "rb") as img_file:
        my_string =  base64.b64encode(img_file.read())
    img_file.close()
    plot.close()
    #plot.show()
    if round(val_r2) == 1:
        descripcionr2='es cercano a 1 Podemos concluir que el modelo lineal es adecuado para describir la relación que existe entre estas variables '
    else: 
        descripcionr2='es cercano a 0 Podemos concluir que el modelo lineal no es representativo lo que supone que el modelo no explica nada de la variación total de la variable Y ' 

    NombreReport = 'Ánalisis Comparativo de Vacunación en  '+pais 
    conclusion = 'Ánalisis Comparativo de Vacunación en '+pais+' la ejecucion se hara con respecto a vacunacion al ejecutarlo podremos la vacunacionsi ira de alta o habra una baja.\n Al relizar la ejecucion podremos observar el valor RMSE: ' + str(val_rmse) +' nos da el error de 2 conjuntos entre los predichos y observados o conocidos, el R2:' + str(val_r2) +' ' + descripcionr2
    return jsonify({"message":"Analisis Realizado de Reporte10","image64":my_string.decode('utf-8'),"conclusion":conclusion,"NombreReport":NombreReport,"Grado":str(poly_degree),"rmse":str(val_rmse),"r2":str(val_r2)})

#Porcentaje de hombres infectados por covid-19 en un País desde el primer caso activo
@app.route('/Analisis_Reporte11', methods = ['POST']) 
def Reporte11():
    body = {
        "var1":request.json['var1'],
        "var2":request.json['var2'],
        "var3":request.json['var3'],
        "var10":request.json['var10']
    }   
    encabezadoPais = body['var1']
    pais = body['var2']
    encabezadoConfirmados = body['var3']
    encabezadoGenero = body['var10']
    #Dias = int(dias) 
    print(body)
    # data 
    
    ''' comienza filtro para pais'''
    print(encabezadoPais)

    Datos =  dataset.loc[dataset[encabezadoPais]==pais]
    Datos = pd.DataFrame(Datos)
    
    Todoshombres = Datos[encabezadoGenero]

    Todosinfectados = Datos[encabezadoConfirmados]
    
    print(Todosinfectados.count())
    vcanthombres = []
    t= 0
    for i in range(Todosinfectados.count()):
        vcanthombres.append(Todoshombres.iloc[i])
    
    print(vcanthombres)
    Dias = Todosinfectados.count()
    print(Dias)
    vinfectados = []
    for z in range(Dias):
        vinfectados.append(Todosinfectados.iloc[z])
    print(vinfectados)
    '''BusquedaPais = dataset[encabezadoPais]
    print(pais)
    for i in dataset.index:
        if(BusquedaPais[i] == pais):
            index_Fil = i


    Fil = dataset.iloc[index_Fil,:]
    vinfectados = []

    for z in range(Dias):
        val = 4+z
        vinfectados.append(Fil.iloc[val])
    print(vinfectados)
    
    '''
    y_new_max = max(vinfectados)
    x = np.asarray(vcanthombres)[:,np.newaxis]
    y = np.asarray(vinfectados)[:,np.newaxis]
    plot.scatter(x,y)
    # Transformar a regresion
    poly_degree = 3
    polynomial_features = PolynomialFeatures(degree = poly_degree)
    x_transform = polynomial_features.fit_transform(x)

    # ajustar el modelo
    model = LinearRegression().fit(x_transform, y)
    y_new = model.predict(x_transform)

    # calculate rmse and r2
    rmse = np.sqrt(mean_squared_error(y, y_new))
    r2 = r2_score(y, y_new)
    print('RMSE: ', rmse)
    print('R2: ', r2)
    val_rmse = rmse
    val_r2 = r2

    cant = max(vcanthombres)
    # Prediccion desde el dia 0 hasta el dia 50
    x_new_min = 0.0
    x_new_max = int(cant)

    x_new = np.linspace(x_new_min, x_new_max, int(cant))
    x_new = x_new[:,np.newaxis]

    x_new_transform = polynomial_features.fit_transform(x_new)
    y_new = model.predict(x_new_transform)

    # Plot de la grafica
    #dataset.plot(x='Dias', y='Infectados', style='o')
    plot.plot(x_new, y_new, color='coral', linewidth=3)
    plot.grid()
    plot.xlim(x_new_min,x_new_max)
    plot.ylim(0,y_new_max)
    title = 'Degree = {}; RMSE = {}; R2 = {}'.format(poly_degree, round(rmse,2), round(r2,2))
    plot.title('Porcentaje de hombres infectados por covid-19 en un '+pais + ' desde el primer caso activo\n ' + title, fontsize=10)
    plot.xlabel('Cantidad Hombres')
    plot.ylabel('Infectados')
    plot.legend(('Regresion Poliminomial','Datos'))

    # use savefig() before show().
    plot.savefig("Reporte11.png")
    with open("Reporte11.png", "rb") as img_file:
        my_string =  base64.b64encode(img_file.read())
    #print(my_string.decode('utf-8'))
    #plot.show()
    img_file.close()
    plot.close()
    if round(r2) == 1:
        descripcionr2='es cercano a 1 Podemos concluir que el modelo lineal es adecuado para describir la relación que existe entre estas variables '
    else: 
        descripcionr2='es cercano a 0 Podemos concluir que el modelo lineal no es representativo lo que supone que el modelo no explica nada de la variación total de la variable Y ' 

    conclusion = 'Porcentaje de hombres infectados por covid-19 en un '+pais + ' la ejecucion se hara con respecto a hombres infectados a infectados del dia  al ejecutarlo podremos prever la tendencia que puede alcanzar proximos meses si ira de alta o habra una baja.\n Al realizar la ejecucion podremos observar el valor RMSE: ' + str(rmse) +' nos da el error de 2 conjuntos entre los predichos y observados o conocidos, el R2:' + str(r2) +' ' + descripcionr2
    NombreReport = 'Porcentaje de hombres infectados por covid-19 en un  '+pais
    #plot.show()
    return jsonify({"message":"Analisis Realizado de Reporte11","image64":my_string.decode('utf-8'),"conclusion":conclusion,"NombreReport":NombreReport,"Grado":str(poly_degree),"rmse":str(rmse),"r2":str(r2)})

    
# Ánalisis Comparativo entres 2 o más paises o continentes. ---->falta
@app.route('/Analisis_Reporte12', methods = ['POST']) 
def Reporte12():
    
    # use savefig() before show().
    plot.savefig("Reporte12.png")
    with open("Reporte12.png", "rb") as img_file:
        my_string =  base64.b64encode(img_file.read())
    #print(my_string.decode('utf-8'))
    #plot.show()
    img_file.close()
    plot.close()
    conclusion = 'Porcentaje de hombres infectados por covid-19 en un ' + ' desde el primer caso activo  con un contador y media como error de : '+' y con un rme de ' 
    #plot.show()
    return jsonify({"message":"Analisis Realizado de Reporte12","image64":my_string.decode('utf-8'),"conclusion":conclusion})

#Muertes promedio por casos confirmados y edad de covid 19 en un País.
''' INICIO CONSULTA DE REPORTE 13''' 

@app.route('/Analisis_Reporte13', methods = ['POST']) 
def Reporte13():
    body = {
        "var1":request.json['var1'],
        "var2":request.json['var2'],
        "var3":request.json['var3'],
        "var5":request.json['var5'],
        "var12":request.json['var12']
    }   
    encabezadoPais = body['var1']
    pais = body['var2']
    encabezadoConfirmados = body['var3']
    encabezadoEdad = body['var12']
    encabezadoMuerte =  body['var5']   
    print(body)
    # data 
   
    ''' comienza filtro para pais''' 
    print(encabezadoPais)

    Datos =  dataset.loc[dataset[encabezadoPais]==pais]
    Datos = pd.DataFrame(Datos)

    TodasEdades = Datos[encabezadoEdad]
    
    Todosinfectados = Datos[encabezadoConfirmados]
    TodasMuertes = Datos[encabezadoMuerte]
    print(Todosinfectados.count())
    #print(TodasMuertes)
    vmuerte = []

    for i in range(TodasMuertes.count()):
        vmuerte.append(TodasMuertes.iloc[i])

    #print(vmuerte)
    Dias = Todosinfectados.count()
    print(Dias)
    vinfectados = []
    for z in range(Dias):
        vinfectados.append(Todosinfectados.iloc[z])
    print(vinfectados)

    y_new_max = max(vinfectados)
    x = np.asarray(vmuerte)[:,np.newaxis]
    y = np.asarray(vinfectados)[:,np.newaxis]
    plot.scatter(x,y)
    # Predecimos la Data
    poly_degree = 4
    polynomial_features = PolynomialFeatures(degree = poly_degree)
    x_transform = polynomial_features.fit_transform(x)

    # Procedemos a entrenar el modelo
    model = LinearRegression().fit(x_transform, y)
    # calculamos la varianza ,rmse y r2
    y_new = model.predict(x_transform)
    rmse = np.sqrt(mean_squared_error(y, y_new))
    r2 = r2_score(y, y_new)

    print('RMSE: ', rmse)
    print('R2: ', r2)
    val_rmse = rmse
    val_r2 = r2

    # Prediccion desde el dia 0 hasta el dia que solicite
    x_new_min = 0.0
    x_new_max = max(vmuerte)


    x_new = np.linspace(x_new_min, x_new_max, max(vmuerte))
    x_new = x_new[:,np.newaxis]

    x_new_transform = polynomial_features.fit_transform(x_new)
    y_new = model.predict(x_new_transform)

    # Plot de la grafica
    #dataset.plot(x='Dias', y='Infectados', style='o')
    plot.plot(x_new, y_new, color='red', linewidth=3)
    plot.grid()
    plot.xlim(x_new_min,x_new_max)
    plot.ylim(0,y_new_max)
    title = 'Degree = {}; RMSE = {}; R2 = {}'.format(poly_degree, round(rmse,2), round(r2,2))
    plot.title('Muertes promedio del segmento por casos confirmados de covid 19 en  '+pais+"\n " + title, fontsize=10)
    plot.xlabel('Muertes')
    plot.ylabel('Confirmados')

    plot.legend(('Regresion Poliminomial','Datos'))
    # use savefig() before show().
    plot.savefig("Reporte13.png")
    with open("Reporte13.png", "rb") as img_file:
        my_string =  base64.b64encode(img_file.read())
    img_file.close()
    plot.close()
    #print(my_string.decode('utf-8'))
    #plot.show()
    if round(r2) == 1:
        descripcionr2='es cercano a 1 Podemos concluir que el modelo lineal es adecuado para describir la relación que existe entre estas variables '
    else: 
        descripcionr2='es cercano a 0 Podemos concluir que el modelo lineal no es representativo lo que supone que el modelo no explica nada de la variación total de la variable Y ' 

    conclusion = 'Muertes promedio por casos confirmados covid 19 en '+pais  + ' la ejecucion se hara con respecto a muertes promedio del dia  al ejecutarlo podremos prever la tendencia que puede alcanzar proximos meses si ira de alta o habra una baja.\n Al realizar la ejecucion podremos observar el valor RMSE: ' + str(rmse) +' nos da el error de 2 conjuntos entre los predichos y observados o conocidos, el R2:' + str(r2) +' ' + descripcionr2
    NombreReport = 'Muertes promedio por casos confirmados covid 19 en  '+pais
    #plot.show()
    return jsonify({"message":"Analisis Realizado de Reporte13","image64":my_string.decode('utf-8'),"conclusion":conclusion,"NombreReport":NombreReport,"Grado":str(poly_degree),"rmse":str(rmse),"r2":str(r2)})


@app.route('/Analisis_Reporte13_1', methods = ['POST']) 
def Reporte13_1():
    body = {
        "var1":request.json['var1'],
        "var2":request.json['var2'],
        "var3":request.json['var3'],
        "var5":request.json['var5'],
        "var12":request.json['var12']
    }   
    encabezadoPais = body['var1']
    pais = body['var2']
    encabezadoConfirmados = body['var3']
    encabezadoEdad = body['var12']
    encabezadoMuerte =  body['var5'] 
    print(body)
    # data 
   
    ''' comienza filtro para pais''' 
    print(encabezadoPais)

    Datos =  dataset.loc[dataset[encabezadoPais]==pais]
    Datos = pd.DataFrame(Datos)

    TodasEdades = Datos[encabezadoEdad]
    print(TodasEdades)
    TodosMuertes = Datos[encabezadoMuerte]
    Todosinfectados = Datos[encabezadoConfirmados]
    print(Todosinfectados.count())
    vedades = []

    for i in range(TodasEdades.count()):
        vedades.append(TodasEdades.iloc[i])

    print(vedades)
    Dias = Todosinfectados.count()
    print(Dias)
    vinfectados = []
    for z in range(Dias):
        vinfectados.append(Todosinfectados.iloc[z])
    print(vinfectados)

    y_new_max = max(vinfectados)
    x = np.asarray(vedades)[:,np.newaxis]
    y = np.asarray(vinfectados)[:,np.newaxis]
    plot.scatter(x,y)
    # Predecimos la Data
    poly_degree = 4
    polynomial_features = PolynomialFeatures(degree = poly_degree)
    x_transform = polynomial_features.fit_transform(x)

    # Procedemos a entrenar el modelo
    model = LinearRegression().fit(x_transform, y)
    # calculamos la varianza ,rmse y r2
    y_new = model.predict(x_transform)
    rmse = np.sqrt(mean_squared_error(y, y_new))
    r2 = r2_score(y, y_new)

    print('RMSE: ', rmse)
    print('R2: ', r2)
    val_rmse = rmse
    val_r2 = r2

    # Prediccion desde el dia 0 hasta el dia que solicite
    x_new_min = 0.0
    x_new_max = max(vedades)


    x_new = np.linspace(x_new_min, x_new_max, max(vedades))
    x_new = x_new[:,np.newaxis]

    x_new_transform = polynomial_features.fit_transform(x_new)
    y_new = model.predict(x_new_transform)

    # Plot de la grafica
    #dataset.plot(x='Dias', y='Infectados', style='o')
    plot.plot(x_new, y_new, color='red', linewidth=3)
    plot.grid()
    plot.xlim(x_new_min,x_new_max)
    plot.ylim(0,y_new_max)
    title = 'Degree = {}; RMSE = {}; R2 = {}'.format(poly_degree, round(rmse,2), round(r2,2))
    plot.title('Casos confirmados y edad de covid 19 en  '+pais+"\n " + title, fontsize=10)
    plot.xlabel('Edad')
    plot.ylabel('Casos Confirmados')

    plot.legend(('Regresion Poliminomial','Datos'))
    # use savefig() before show().
    plot.savefig("Reporte131.png")
    with open("Reporte131.png", "rb") as img_file:
        my_string1 =  base64.b64encode(img_file.read())
    img_file.close()
    plot.close()
    if round(r2) == 1:
        descripcionr2='es cercano a 1 Podemos concluir que el modelo lineal es adecuado para describir la relación que existe entre estas variables '
    else: 
        descripcionr2='es cercano a 0 Podemos concluir que el modelo lineal no es representativo lo que supone que el modelo no explica nada de la variación total de la variable Y ' 

    conclusion = 'Casos confirmados y edad de covid 19 en '+pais  + ' la ejecucion se hara con respecto a muertes promedio del dia  al ejecutarlo podremos prever la tendencia que puede alcanzar proximos meses si ira de alta o habra una baja.\n Al realizar la ejecucion podremos observar el valor RMSE: ' + str(rmse) +' nos da el error de 2 conjuntos entre los predichos y observados o conocidos, el R2:' + str(r2) +' ' + descripcionr2
    NombreReport = 'Casos confirmados y edad de covid 19 en  '+pais
    #plot.show()
    return jsonify({"message":"Analisis Realizado de Reporte13","image64":my_string1.decode('utf-8'),"conclusion":conclusion,"NombreReport":NombreReport,"Grado":str(poly_degree),"rmse":str(rmse),"r2":str(r2)})

@app.route('/Analisis_Reporte13_2', methods = ['POST']) 
def Reporte13_2():
    body = {
        "var1":request.json['var1'],
        "var2":request.json['var2'],
        "var3":request.json['var3'],
        "var5":request.json['var5'],
        "var12":request.json['var12']
    }   
    encabezadoPais = body['var1']
    pais = body['var2']
    encabezadoConfirmados = body['var3']
    encabezadoEdad = body['var12']
    encabezadoMuerte =  body['var5']    
    print(body)
    # data 
   
    ''' comienza filtro para pais''' 
    print(encabezadoPais)

    Datos =  dataset.loc[dataset[encabezadoPais]==pais]
    Datos = pd.DataFrame(Datos)

    TodasEdades = Datos[encabezadoEdad]
    print(TodasEdades)
    TodosMuertes = Datos[encabezadoMuerte]
    Todosinfectados = Datos[encabezadoConfirmados]
    print(TodosMuertes.count())
    vedades = []

    for i in range(TodasEdades.count()):
        vedades.append(TodasEdades.iloc[i])

    print(vedades)
    Dias = TodosMuertes.count()
    print(Dias)
    vmuertes = []
    for z in range(Dias):
        vmuertes.append(TodosMuertes.iloc[z])
    print(vmuertes)

    y_new_max = max(vmuertes)
    x = np.asarray(vedades)[:,np.newaxis]
    y = np.asarray(vmuertes)[:,np.newaxis]
    plot.scatter(x,y)
    # Predecimos la Data
    poly_degree = 4
    polynomial_features = PolynomialFeatures(degree = poly_degree)
    x_transform = polynomial_features.fit_transform(x)

    # Procedemos a entrenar el modelo
    model = LinearRegression().fit(x_transform, y)
    # calculamos la varianza ,rmse y r2
    y_new = model.predict(x_transform)
    rmse = np.sqrt(mean_squared_error(y, y_new))
    r2 = r2_score(y, y_new)

    print('RMSE: ', rmse)
    print('R2: ', r2)
    val_rmse = rmse
    val_r2 = r2

    # Prediccion desde el dia 0 hasta el dia que solicite
    x_new_min = 0.0
    x_new_max = max(vedades)


    x_new = np.linspace(x_new_min, x_new_max, max(vedades))
    x_new = x_new[:,np.newaxis]


    x_new_transform = polynomial_features.fit_transform(x_new)
    y_new = model.predict(x_new_transform)

    # Plot de la grafica
    #dataset.plot(x='Dias', y='Infectados', style='o')
    plot.plot(x_new, y_new, color='red', linewidth=3)
    plot.grid()
    plot.xlim(x_new_min,x_new_max)
    plot.ylim(0,y_new_max)
    title = 'Degree = {}; RMSE = {}; R2 = {}'.format(poly_degree, round(rmse,2), round(r2,2))
    plot.title('Muertes promedio del segmento por  edad de covid 19 en  '+pais+"\n " + title, fontsize=10)
    plot.xlabel('Edad')
    plot.ylabel('No. Muertes')

    plot.legend(('Regresion Poliminomial','Datos'))
    # use savefig() before show().
    plot.savefig("Reporte132.png")
    with open("Reporte132.png", "rb") as img_file:
        my_string =  base64.b64encode(img_file.read())
    img_file.close()
    plot.close()
    #print(my_string.decode('utf-8'))
    #plot.show()
    if round(r2) == 1:
        descripcionr2='es cercano a 1 Podemos concluir que el modelo lineal es adecuado para describir la relación que existe entre estas variables '
    else: 
        descripcionr2='es cercano a 0 Podemos concluir que el modelo lineal no es representativo lo que supone que el modelo no explica nada de la variación total de la variable Y ' 

    conclusion = 'Muertes promedio del segmento por  edad de covid 19 en '+pais  + ' la ejecucion se hara con respecto a muertes promedio del dia  al ejecutarlo podremos prever la tendencia que puede alcanzar proximos meses si ira de alta o habra una baja.\n Al realizar la ejecucion podremos observar el valor RMSE: ' + str(rmse) +' nos da el error de 2 conjuntos entre los predichos y observados o conocidos, el R2:' + str(r2) +' ' + descripcionr2
    NombreReport = 'Muertes promedio del segmento por  edad de covid 19 en  '+pais
    #plot.show()
    return jsonify({"message":"Analisis Realizado de Reporte13","image64":my_string.decode('utf-8'),"conclusion":conclusion,"NombreReport":NombreReport,"Grado":str(poly_degree),"rmse":str(rmse),"r2":str(r2)})


''' FIN CONSULTA DE REPORTE 13''' 

# Muertes según regiones de un país - Covid 19.             ---->falta
@app.route('/Analisis_Reporte14', methods = ['POST']) 
def Reporte14():
    
    # use savefig() before show().
    plot.savefig("Reporte14.png")
    with open("Reporte14.png", "rb") as img_file:
        my_string =  base64.b64encode(img_file.read())
    #print(my_string.decode('utf-8'))
    #plot.show()
    img_file.close()
    plot.close()
    conclusion = 'Porcentaje de hombres infectados por covid-19 en un ' + ' desde el primer caso activo  con un contador y media como error de : '+' y con un rme de ' 
    #plot.show()
    return jsonify({"message":"Analisis Realizado de Reporte14","image64":my_string.decode('utf-8'),"conclusion":conclusion})

#Tendencia de casos confirmados de Coronavirus en un departamento de un País.
@app.route('/Analisis_Reporte15', methods = ['POST']) 
def Reporte15():
    body = {
        "var1":request.json['var1'],
        "var2":request.json['var2'],
        "var5":request.json['var5'],
        "var6":request.json['var6'],
        "var7":request.json['var7'],
        "var4":request.json['var4'],
        "var3":request.json['var3']
    }   
    encabezadoPais = body['var1']   
    pais = body['var2']
    encabezadoDepartamento = body['var6']
    departamento = body['var7']
    encabezadoConfirmados = body['var3']

    print(body)
    # data 
    
    ''' comienza filtro para pais''' 
    print(encabezadoDepartamento)

    Datos =  dataset.loc[dataset[encabezadoPais]==pais]
    Datos = pd.DataFrame(Datos)

    print(Datos)

    TodosDepartamento =  Datos.loc[Datos[encabezadoDepartamento]==departamento]

    print(TodosDepartamento)
    Todosinfectados = TodosDepartamento[encabezadoConfirmados]
    print(Todosinfectados.count())
    vdias = []

    for i in range(Todosinfectados.count()):
        vdias.append(i)
    
    #print(vdias)
    Dias = Todosinfectados.count()
    print(Dias)
    vinfectados = []
    for z in range(Dias):
        vinfectados.append(Todosinfectados.iloc[z])
    #print(vinfectados)

    y_new_max = max(vinfectados)
    x = np.asarray(vdias)[:,np.newaxis]
    y = np.asarray(vinfectados)[:,np.newaxis]
    plot.scatter(x,y)
    # Predecimos la Data
    poly_degree = 4
    polynomial_features = PolynomialFeatures(degree = poly_degree)
    x_transform = polynomial_features.fit_transform(x)

    # Procedemos a entrenar el modelo
    model = LinearRegression().fit(x_transform, y)
    # calculamos la varianza ,rmse y r2
    y_new = model.predict(x_transform)
    rmse = np.sqrt(mean_squared_error(y, y_new))
    r2 = r2_score(y, y_new)

    print('RMSE: ', rmse)
    print('R2: ', r2)
    val_rmse = rmse
    val_r2 = r2

    # Prediccion desde el dia 0 hasta el dia que solicite
    x_new_min = 0.0
    x_new_max = Dias


    x_new = np.linspace(x_new_min, x_new_max, Dias)
    x_new = x_new[:,np.newaxis]

    x_new_transform = polynomial_features.fit_transform(x_new)
    y_new = model.predict(x_new_transform)
    # Plot de la grafica
    #dataset.plot(x='Dias', y='Infectados', style='o')
    plot.plot(x_new, y_new, color='red', linewidth=3)
    plot.grid()
    plot.xlim(x_new_min,x_new_max)
    plot.ylim(0,y_new_max)
    title = 'Degree = {}; RMSE = {}; R2 = {}'.format(poly_degree, round(rmse,2), round(r2,2))
    plot.title('Tendencia de casos confirmados de Coronavirus en covid 19 en '+departamento+' de '+pais+" \n " + title, fontsize=10)
    plot.xlabel('Dias')
    plot.ylabel('No. Casos Confirmados')

    plot.legend(('Regresion Poliminomial','Datos'))
    # use savefig() before show().
    plot.savefig("Reporte15.png")
    with open("Reporte15.png", "rb") as img_file:
        my_string =  base64.b64encode(img_file.read())
    #print(my_string.decode('utf-8'))
    #plot.show()
    img_file.close()
    plot.close()
    if round(r2) == 1:
        descripcionr2='es cercano a 1 Podemos concluir que el modelo lineal es adecuado para describir la relación que existe entre estas variables '
    else: 
        descripcionr2='es cercano a 0 Podemos concluir que el modelo lineal no es representativo lo que supone que el modelo no explica nada de la variación total de la variable Y ' 

    conclusion = 'Tendencia de casos confirmados de Coronavirus en covid 19 en '+departamento+' de '+pais + ' la ejecucion se hara con respecto a casos confirmados infectados del dia  al ejecutarlo podremos prever la tendencia que puede alcanzar proximos meses si ira de alta o habra una baja.\n Al realizar la ejecucion podremos observar el valor RMSE: ' + str(rmse) +' nos da el error de 2 conjuntos entre los predichos y observados o conocidos, el R2:' + str(r2) +' ' + descripcionr2
    NombreReport = 'Tendencia de casos confirmados de Coronavirus en covid 19 en '+departamento+' de '+pais
    #plot.show()
    return jsonify({"message":"Analisis Realizado de Reporte15","image64":my_string.decode('utf-8'),"conclusion":conclusion,"NombreReport":NombreReport,"Grado":str(poly_degree),"rmse":str(rmse),"r2":str(r2)})


#Porcentaje de muertes frente al total de casos en un país, región o continente.        --> falta
@app.route('/Analisis_Reporte16', methods = ['POST']) 
def Reporte16():
    
    # use savefig() before show().
    plot.savefig("Reporte16.png")
    with open("Reporte16.png", "rb") as img_file:
        my_string =  base64.b64encode(img_file.read())
    #print(my_string.decode('utf-8'))
    #plot.show()
    img_file.close()
    plot.close()
    conclusion = 'Porcentaje de hombres infectados por covid-19 en un ' + ' desde el primer caso activo  con un contador y media como error de : '+' y con un rme de ' 
    #plot.show()
    return jsonify({"message":"Analisis Realizado de Reporte16","image64":my_string.decode('utf-8'),"conclusion":conclusion})

#Tasa de comportamiento de casos activos en relación al número de muertes en un continente.
@app.route('/Analisis_Reporte17', methods = ['POST']) 
def Reporte17():
    body = {
        "var11":request.json['var11'],
        "var13":request.json['var13'],
        "var3":request.json['var3'],
        "var5":request.json['var5']
    }
    encabezadoContinente = body['var11']   
    continente = body['var13']
    encabezadoCasos = body['var3']
    encabezadoMuertes = body['var5']
    
    print(body)
    # data 
    
    ''' comienza filtro para pais''' 
    print(encabezadoContinente)

    Datos =  dataset.loc[dataset[encabezadoContinente]==continente]
    Datos = pd.DataFrame(Datos)
    TodosCasos =  Datos[encabezadoCasos]
    TodosMuertos = Datos[encabezadoMuertes]
    print(TodosMuertos.count()) 
    print(encabezadoMuertes)

    vcasos = []    
    for i in range(TodosCasos.count()):
        vcasos.append(TodosCasos.iloc[i])
    
    #print(vdias)
    Dias = TodosMuertos.count()
    print(Dias)
    vmuertos = []
    for z in range(Dias):
        vmuertos.append(TodosMuertos.iloc[z])
    #print(vmuertos)

    y_new_max = max(vmuertos)
    x = np.asarray(vcasos)[:,np.newaxis]
    y = np.asarray(vmuertos)[:,np.newaxis]


    # Procedemos a entrenar el modelo
    model = LinearRegression().fit(x, y)
    # calculamos la varianza ,rmse y r2
    y_new = model.predict(x)

    rmse = np.sqrt(mean_squared_error(y, y_new))
    r2 = r2_score(y, y_new)

    print('RMSE: ', rmse)
    print('R2: ', r2)


    # Prediccion desde el dia 0 hasta el dia que solicite
    x_new_min = 0.0
    x_new_max = max(vcasos)

    # Plot de la grafica
    plot.xlim(x_new_min, x_new_max, max(vcasos))
    plot.ylim(0,y_new_max)

    plot.grid()
   
    title = 'Modelo : Y = {}; X+{}; RMSE = {}; R2 = {}'.format(str(model.coef_[0][0]),str(model.intercept_[0]),round(rmse,2), round(r2,2))
    plot.title('Tasa de comportamiento de casos activos en relación al número de muertes en '+continente+"\n " + title, fontsize=10)
    plot.xlabel('No. Casos')
    plot.ylabel('No. de Muertes')
    plot.scatter(x, y)
    plot.plot(x, y_new, color='red')
    plot.legend(('Regresion Lineal','Datos'))
    # use savefig() before show().
    plot.savefig("Reporte17.png")
    with open("Reporte17.png", "rb") as img_file:
        my_string =  base64.b64encode(img_file.read())
    #print(my_string.decode('utf-8'))
    #plot.show()
    img_file.close()
    plot.close()
    if round(r2) == 1:
        descripcionr2='es cercano a 1 Podemos concluir que el modelo lineal es adecuado para describir la relación que existe entre estas variables '
    else: 
        descripcionr2='es cercano a 0 Podemos concluir que el modelo lineal no es representativo lo que supone que el modelo no explica nada de la variación total de la variable Y ' 

    NombreReport = 'Tasa de comportamiento de casos activos en relación al número de muertes en '+continente
    conclusion ='Tasa de comportamiento de casos activos en relación al número de muertes en '+continente+"\n "+' Modelo : Y = {}; X+{}; RMSE = {}; R2 = {}'.format(str(model.coef_[0][0]),str(model.intercept_[0]),round(rmse,2), round(r2,2)) + ' RMSE nos da el error de 2 conjuntos entre los predichos y observados o conocidos y R2 '+descripcionr2
    return jsonify({"message":"Analisis Realizado de Reporte 17","image64":my_string.decode('utf-8'),"conclusion":conclusion,"NombreReport":NombreReport,"rmse":str(rmse),"r2":str(r2),"modelo":'Y ='+str(model.coef_[0][0])+' X+'+str(model.intercept_[0])})

#Comportamiento y clasificación de personas infectadas por COVID-19 por municipio en un País. ----->duda
'''INICIO REPORTE 18'''
@app.route('/Analisis_Reporte18', methods = ['POST']) 
def Reporte18():
    body = {
        "var1":request.json['var1'],
        "var2":request.json['var2'],
        "var3":request.json['var3'],
        "var10":request.json['var10'],
        "var19":request.json['var19'],
        "var20":request.json['var20'],
        "var21":request.json['var21']
    }
    encabezadoPais = body['var1']
    pais = body['var2']
    encabezadoConfirmados = body['var3']
    encabezadoGenero = body['var10']
    encabezadoGenero2 = body['var19']
    encabezadoMunicipio = body['var20']
    municipio = body['var21']

    print(body)

    ''' comienza filtro para pais''' 
    print(encabezadoMunicipio)

    Datos =  dataset.loc[dataset[encabezadoPais]==pais]
    Datos = pd.DataFrame(Datos)

    print(Datos)

    TodosMunicipio =  Datos.loc[Datos[encabezadoMunicipio]==municipio]
    print(TodosMunicipio)
    TodosGenero = TodosMunicipio[encabezadoGenero]
    print(TodosGenero)
    Todosinfectados = TodosMunicipio[encabezadoGenero2]
    print(Todosinfectados.count())
    vdias = []    
    for i in range(2):
        vdias.append(i)
    
    print(vdias)
    
    vconfirmados = []
    for z in range(1):
        vconfirmados.append(TodosGenero.iloc[z])
        men = TodosGenero.iloc[z]
        vconfirmados.append(Todosinfectados.iloc[z])
        woman = Todosinfectados.iloc[z]
    print(vconfirmados)

    y_new_max = max(Todosinfectados)+10
 
    x = np.asarray(vdias)[:,np.newaxis]
    y = np.asarray(vconfirmados)[:,np.newaxis]


    # Procedemos a entrenar el modelo
    model = LinearRegression().fit(x, y)
    # calculamos la varianza ,rmse y r2
    y_new = model.predict(x)

    rmse = np.sqrt(mean_squared_error(y, y_new))
    r2 = r2_score(y, y_new)

    print('RMSE: ', rmse)
    print('R2: ', r2)


    # Prediccion desde el dia 0 hasta el dia que solicite
    x_new_min = 0.0
    x_new_max = 3

    # Plot de la grafica
    plot.xlim(x_new_min, x_new_max, 2)
    plot.ylim(0,y_new_max)

    plot.grid()
   
    title = 'Modelo : Y = {}; X+{}; RMSE = {}; R2 = {}'.format(str(model.coef_[0][0]),str(model.intercept_[0]),round(rmse,2), round(r2,2))
    plot.title('Comportamiento y clasificación de personas infectadas \n de Coronavirus en covid 19 en '+municipio+' de '+pais+ '\n' + title, fontsize=10)
    plot.xlabel('Genero[pto. izq-->Hombres pto. der--> Mujeres ]')
    plot.ylabel('No. Casos Confirmados')
    plot.scatter(x+1, y)
    plot.plot(x+1, y_new,color='red')
    plot.legend(('Generos','Datos'))


    # use savefig() before show().
    plot.savefig("Reporte18.png")
    with open("Reporte18.png", "rb") as img_file:
        my_string =  base64.b64encode(img_file.read())
    img_file.close()
    plot.close()
    #plot.show()
    if round(r2) == 1:
        descripcionr2='es cercano a 1 Podemos concluir que el modelo lineal es adecuado para describir la relación que existe entre estas variables '
    else: 
        descripcionr2='es cercano a 0 Podemos concluir que el modelo lineal no es representativo lo que supone que el modelo no explica nada de la variación total de la variable Y ' 

    NombreReport = 'Comportamiento y clasificación de personas infectadas \n de Coronavirus en covid 19 en '+municipio+' de '+pais
    conclusion ='Comportamiento y clasificación de personas infectadas \n de Coronavirus en covid 19 en '+municipio+' de '+pais+"\n "+' Modelo : Y = {}; X+{}; RMSE = {}; R2 = {}'.format(str(model.coef_[0][0]),str(model.intercept_[0]),round(rmse,2), round(r2,2)) + ' nos dice que de hombres hay '+str(men)+' hombres infectados y de mujeres '+str(woman)+' infectadas la pendiente esta en relacion de  cantidad de hombre a mujeres infectadas RMSE nos da el error de 2 conjuntos entre los predichos y observados o conocidos y R2 '+descripcionr2
    return jsonify({"message":"Analisis Realizado de Reporte 18","image64":my_string.decode('utf-8'),"conclusion":conclusion,"NombreReport":NombreReport,"rmse":str(rmse),"r2":str(r2),"modelo":'Y ='+str(model.coef_[0][0])+' X+'+str(model.intercept_[0])})

@app.route('/Analisis_Reporte181', methods = ['POST']) 
def Reporte181():
    body = {
        "var1":request.json['var1'],
        "var2":request.json['var2'],
        "var3":request.json['var3'],
        "var10":request.json['var10'],
        "var19":request.json['var19'],
        "var20":request.json['var20'],
        "var21":request.json['var21']
    }
    encabezadoPais = body['var1']
    pais = body['var2']
    encabezadoConfirmados = body['var3']
    encabezadoGenero = body['var10']
    encabezadoGenero2 = body['var19']
    encabezadoMunicipio = body['var20']
    municipio = body['var21']

    print(body)

    ''' comienza filtro para pais''' 
    print(encabezadoMunicipio)

    Datos =  dataset.loc[dataset[encabezadoPais]==pais]
    Datos = pd.DataFrame(Datos)

    print(Datos)

    TodosMunicipio =  Datos.loc[Datos[encabezadoMunicipio]==municipio]
    TodosGenero = TodosMunicipio[encabezadoGenero2]
    print(TodosGenero)
    Todosinfectados = TodosMunicipio[encabezadoConfirmados]
    print("infectados que hay abajo")
    print(Todosinfectados.count())
    vdias = []

    for i in range(Todosinfectados.count()):
        vdias.append(i)
    
    #print(vdias)
    Dias = Todosinfectados.count()
    print(Dias)
    vinfectados = []
    for z in range(Dias):
        vinfectados.append(Todosinfectados.iloc[z])
    #print(vinfectados)

    y_new_max = max(vinfectados)
    x = np.asarray(vdias)[:,np.newaxis]
    y = np.asarray(vinfectados)[:,np.newaxis]
    plot.scatter(x,y)
    # Predecimos la Data
    poly_degree = 4
    polynomial_features = PolynomialFeatures(degree = poly_degree)
    x_transform = polynomial_features.fit_transform(x)

    # Procedemos a entrenar el modelo
    model = LinearRegression().fit(x_transform, y)
    # calculamos la varianza ,rmse y r2
    y_new = model.predict(x_transform)
    rmse = np.sqrt(mean_squared_error(y, y_new))
    r2 = r2_score(y, y_new)

    print('RMSE: ', rmse)
    print('R2: ', r2)
    val_rmse = rmse
    val_r2 = r2

    # Prediccion desde el dia 0 hasta el dia que solicite
    x_new_min = 0.0
    x_new_max = Dias


    x_new = np.linspace(x_new_min, x_new_max, Dias)
    x_new = x_new[:,np.newaxis]

    x_new_transform = polynomial_features.fit_transform(x_new)
    y_new = model.predict(x_new_transform)
    # Plot de la grafica
    #dataset.plot(x='Dias', y='Infectados', style='o')
    plot.plot(x_new, y_new, color='red', linewidth=3)
    plot.grid()
    plot.xlim(x_new_min,x_new_max)
    plot.ylim(0,y_new_max)
    title = 'Degree = {}; RMSE = {}; R2 = {}'.format(poly_degree, round(rmse,2), round(r2,2))
    plot.title('Comportamiento y clasificación de personas infectadas \n de Coronavirus en covid 19 en '+municipio+' de '+pais+" \n " + title, fontsize=10)
    plot.xlabel('Dias')
    plot.ylabel('No.' + encabezadoGenero2)

    plot.legend(('Regresion Poliminomial','Datos'))
    # use savefig() before show().
    plot.savefig("Reporte15.png")
    with open("Reporte15.png", "rb") as img_file:
        my_string =  base64.b64encode(img_file.read())
    #print(my_string.decode('utf-8'))
    #plot.show()
    img_file.close()
    plot.close()
    conclusion = 'Comportamiento y clasificación de personas infectadas \n de Coronavirus en covid 19 en ' +municipio+ ' de ' + pais+' desde el primer caso activo  con un contador y media como error de : ' + str(val_r2) +' y con un rme de ' + str(val_rmse)
    #plot.show()
    return jsonify({"message":"Analisis Realizado de Reporte18","image64":my_string.decode('utf-8'),"conclusion":conclusion})


'''FIN REPORTE 18'''
# Predicción de muertes en el último día del primer año de infecciones en un país.
@app.route('/Analisis_Reporte19', methods = ['POST']) 
def Reporte19():
    body = {
        "var1":request.json['var1'],
        "var2":request.json['var2'],
        "var5":request.json['var5'],
        "var14":request.json['var14']
    }   
    encabezadoPais = body['var1']
    pais = body['var2']
    encabezadoMuertes = body['var5']
    encabezadofecha = body['var14']
    
    print(body)
    # data 
   
    ''' comienza filtro para pais''' 
    print(encabezadoPais)

    Datos =  dataset.loc[dataset[encabezadoPais]==pais]
    Datos = pd.DataFrame(Datos)

    TodosMuertos = Datos[encabezadoMuertes]

    Mes = Datos[encabezadofecha].dt.month
    DiaMes = Datos[encabezadofecha].dt.day
    MesFinal = max(Mes)
    DiaFinal = max(DiaMes)
    if MesFinal ==1:
        DiasPredicion = 365-DiaFinal
    elif MesFinal ==2:
        DiasPredicion = 334-DiaFinal
    elif MesFinal ==3:
        DiasPredicion = 306-DiaFinal
    elif MesFinal ==4:
        DiasPredicion = 275-DiaFinal
    elif MesFinal ==5:
        DiasPredicion = 245-DiaFinal
    elif MesFinal ==6:
        DiasPredicion = 214-DiaFinal
    elif MesFinal ==7:
        DiasPredicion = 184-DiaFinal
    elif MesFinal ==8:
        DiasPredicion = 153-DiaFinal
    elif MesFinal ==9:
        DiasPredicion = 122-DiaFinal
    elif MesFinal ==10:
        DiasPredicion = 92-DiaFinal
    elif MesFinal ==11:
        DiasPredicion = 61-DiaFinal
    elif MesFinal ==12:
        DiasPredicion = 31-DiaFinal
    else:
        DiasPredicion = 365 #int(dias)
        print('vali verdura')

    print(DiasPredicion)

    print(TodosMuertos.count())
    vdias = []
    t= 0
    for i in range(TodosMuertos.count()):
        vdias.append(i)
    
    print(vdias)
    Dias = TodosMuertos.count()
    print(Dias)
    vinfectados = []
    for z in range(Dias):
        vinfectados.append(TodosMuertos.iloc[z])
    print(vinfectados)

    y_new_max = max(vinfectados)
    x = np.asarray(vdias)[:,np.newaxis]
    y = np.asarray(vinfectados)[:,np.newaxis]
    plot.scatter(x,y)
    # Predecimos la Data
    poly_degree = 4
    polynomial_features = PolynomialFeatures(degree = poly_degree)
    x_transform = polynomial_features.fit_transform(x)

    # Procedemos a entrenar el modelo
    model = LinearRegression().fit(x_transform, y)
    # calculamos la varianza ,rmse y r2
    y_new = model.predict(x_transform)
    rmse = np.sqrt(mean_squared_error(y, y_new))
    r2 = r2_score(y, y_new)

    print('RMSE: ', rmse)
    print('R2: ', r2)
    val_rmse = rmse
    val_r2 = r2

    # Prediccion desde el dia 0 hasta el dia que solicite
    x_new_min = 0.0
    x_new_max = DiasPredicion+30 # le aumente la prediccion a 30 dias mas 


    x_new = np.linspace(x_new_min, x_new_max, Dias)
    x_new = x_new[:,np.newaxis]

    x_new_transform = polynomial_features.fit_transform(x_new)
    y_new = model.predict(x_new_transform)

    
    prediction = y_new[np.size(y_new)-1]
     # Plot de la grafica
    #dataset.plot(x='Dias', y='Infectados', style='o')
    plot.plot(x_new, y_new, color='red', linewidth=3)
    plot.grid()
    plot.xlim(x_new_min,x_new_max)
    plot.ylim(0,y_new_max+100)
    title = 'Degree = {}; RMSE = {}; R2 = {}'.format(poly_degree, round(rmse,2), round(r2,2))
    plot.title('Predicción de muertes en el último día del primer año de infecciones en  '+pais+"\n " + title, fontsize=10)
    plot.xlabel('Dias')
    plot.ylabel('Muertos')

    plot.legend(('Regresion Poliminomial','Datos'))
    # use savefig() before show().
    plot.savefig("Reporte19.png")
    with open("Reporte19.png", "rb") as img_file:
        my_string =  base64.b64encode(img_file.read())
    img_file.close()
    plot.close()
    #print(my_string.decode('utf-8'))
    #plot.show()
    if round(val_r2) == 1:
        descripcionr2='es cercano a 1 Podemos concluir que el modelo lineal es adecuado para describir la relación que existe entre estas variables '
    else: 
        descripcionr2='es cercano a 0 Podemos concluir que el modelo lineal no es representativo lo que supone que el modelo no explica nada de la variación total de la variable Y ' 

    NombreReport = 'Predicción de muertes en el último día del primer año de infecciones en  '+pais +' a una prediccion'+ str(x_new_max) + ' dias'
    conclusion = 'Predicción de muertes en el último día del primer año de infecciones en  '+pais +' a una prediccion'+ str(x_new_max) + ' dias la ejecucion se hara con respecto a muertes de un pais por dias  al ejecutarlo podremos ver la prediccion la cual es '+str(prediction)+' de mortalidad en los '+str(DiasPredicion) +' si ira de alta o habra una baja.\n Al relizar la ejecucion podremos observar el valor RMSE: ' + str(val_rmse) +' nos da el error de 2 conjuntos entre los predichos y observados o conocidos, el R2:' + str(val_r2) +' ' + descripcionr2
    return jsonify({"message":"Analisis Realizado de Reporte19","image64":my_string.decode('utf-8'),"conclusion":conclusion,"NombreReport":NombreReport,"Grado":str(poly_degree),"rmse":str(val_rmse),"r2":str(val_r2),"prediccion":str(prediction)})

# Tasa de crecimiento de casos de COVID-19 en relación con nuevos casos diarios y tasa de muerte por COVID-19
@app.route('/Analisis_Reporte20', methods = ['POST']) 
def Reporte20():
    body = {
        "var5":request.json['var5'],
        "var16":request.json['var16']
    }
    encabezadoMuertes = body['var5']   
    encabezadosNuevosCasos = body['var16']

    print(body)
    # data 
    
    ''' comienza filtro ''' 
    print(encabezadosNuevosCasos)

    Datos =  dataset[encabezadosNuevosCasos]
    #Datos = pd.DataFrame(Datos)

    TodosResultados = dataset[encabezadoMuertes]
    print(TodosResultados.count()) 
    print(encabezadoMuertes)

    vresultEntregados = []    
    for i in range(TodosResultados.count()):
        vresultEntregados.append(TodosResultados.iloc[i])
    
    #print(vdias)
    Dias = TodosResultados.count()
    print(Dias)
    vconfirmados = []
    for z in range(Dias):
        vconfirmados.append(Datos.iloc[z])
    #print(vmuertos)

    y_new_max = max(vconfirmados)
    x = np.asarray(vresultEntregados)[:,np.newaxis]
    y = np.asarray(vconfirmados)[:,np.newaxis]


    plot.scatter(x,y)
    # Predecimos la Data
    poly_degree = 3
    polynomial_features = PolynomialFeatures(degree = poly_degree)
    x_transform = polynomial_features.fit_transform(x)

    # Procedemos a entrenar el modelo
    model = LinearRegression().fit(x_transform, y)
    # calculamos la varianza ,rmse y r2
    y_new = model.predict(x_transform)
    rmse = np.sqrt(mean_squared_error(y, y_new))
    r2 = r2_score(y, y_new)

    print('RMSE: ', rmse)
    print('R2: ', r2)
    val_rmse = rmse
    val_r2 = r2

    # Prediccion desde el dia 0 hasta el dia que solicite
    x_new_min = 0.0
    x_new_max = max(vresultEntregados)


    x_new = np.linspace(x_new_min, x_new_max, max(vresultEntregados))
    x_new = x_new[:,np.newaxis]

    x_new_transform = polynomial_features.fit_transform(x_new)
    y_new = model.predict(x_new_transform)
    # Plot de la grafica
    #dataset.plot(x='Dias', y='Infectados', style='o')
    plot.plot(x_new, y_new, color='red', linewidth=3)
    plot.grid()
    plot.xlim(x_new_min,x_new_max)
    plot.ylim(0,y_new_max+100)
    title = 'Degree = {}; RMSE = {}; R2 = {}'.format(poly_degree, round(rmse,2), round(r2,2))
    plot.title('Tasa de crecimiento de casos de COVID-19 en relación con nuevos casos diarios y tasa \n de muerte por COVID-19'+"\n " + title, fontsize=10)
    plot.xlabel('No. Muertes')
    plot.ylabel('No. Nuevos Casos')

    plot.legend(('Regresion Poliminomial','Datos'))

    # use savefig() before show().
    plot.savefig("Reporte20.png")
    with open("Reporte20.png", "rb") as img_file:
        my_string =  base64.b64encode(img_file.read())
    #print(my_string.decode('utf-8'))
    #plot.show()
    img_file.close()
    plot.close()
    if round(r2) == 1:
        descripcionr2='es cercano a 1 Podemos concluir que el modelo lineal es adecuado para describir la relación que existe entre estas variables '
    else: 
        descripcionr2='es cercano a 0 Podemos concluir que el modelo lineal no es representativo lo que supone que el modelo no explica nada de la variación total de la variable Y ' 

    conclusion = 'Tasa de crecimiento de casos de COVID-19 en relación con nuevos casos diarios y tasa  de muerte por COVID-19 en relación con nuevos casos diarios y tasa \n de muerte por COVID-19 ejecucion se hara con respecto a casos nuevos confirmados infectados del dia  al ejecutarlo podremos prever la tendencia que puede alcanzar proximos meses si ira de alta o habra una baja.\n Al realizar la ejecucion podremos observar el valor RMSE: ' + str(rmse) +' nos da el error de 2 conjuntos entre los predichos y observados o conocidos, el R2:' + str(r2) +' ' + descripcionr2
    NombreReport = 'Tasa de crecimiento de casos de COVID-19 en relación con nuevos casos diarios y tasa  de muerte por COVID-19'
    #plot.show()
    return jsonify({"message":"Analisis Realizado de Reporte20","image64":my_string.decode('utf-8'),"conclusion":conclusion,"NombreReport":NombreReport,"Grado":str(poly_degree),"rmse":str(rmse),"r2":str(r2)})

'''INICIO REPORTE 21'''
# Predicciones de casos y muertes en todo el mundo - Neural Network MLPRegressor
@app.route('/Analisis_Reporte21', methods = ['POST']) 
def Reporte21():
    body = {
        "var3":request.json['var3'],
        "var4":request.json['var4'],
        "var5":request.json['var5']
    }   
    encabezadoCasos = body['var3']
    encabezadoMuertes = body['var5']
    dias = body['var4']
    DiasPredicion = int(dias)
    print(DiasPredicion)

    print(body)
    # data 
    
    ''' comienza filtro''' 

    Datos =  dataset[encabezadoCasos]
    Datos = pd.DataFrame(Datos)

    Todosinfectados = dataset[encabezadoCasos]
    print(Todosinfectados.count())
    vdias = []

    for i in range(Todosinfectados.count()):
        vdias.append(i)
    
    print(vdias)
    Dias = Todosinfectados.count()
    print(Dias)
    vinfectados = []
    for z in range(Dias):
        vinfectados.append(Todosinfectados.iloc[z])
    #print(vinfectados)

    y_new_max = max(vinfectados)
    x = np.asarray(vdias)[:,np.newaxis]
    y = np.asarray(vinfectados)[:,np.newaxis]
    plot.scatter(x,y)
    # Predecimos la Data
    poly_degree = 3 # duda del grado de la polinomia revisar
    polynomial_features = PolynomialFeatures(degree = poly_degree)
    x_transform = polynomial_features.fit_transform(x)

    # Procedemos a entrenar el modelo
    model = LinearRegression().fit(x_transform, y)
    # calculamos la varianza ,rmse y r2
    y_new = model.predict(x_transform)
    prediction = y_new[np.size(y_new)-1]
    rmse = np.sqrt(mean_squared_error(y, y_new))
    r2 = r2_score(y, y_new)

    print('RMSE: ', rmse)
    print('R2: ', r2)
    val_rmse = rmse
    val_r2 = r2

     # Prediccion desde el dia 0 hasta el dia que solicite
    x_new_min = 0.0
    x_new_max = DiasPredicion # le aumente la prediccion a 30 dias mas 


    x_new = np.linspace(x_new_min, x_new_max, Dias)
    x_new = x_new[:,np.newaxis]

    x_new_transform = polynomial_features.fit_transform(x_new)
    y_new = model.predict(x_new_transform)

    
    prediction = y_new[np.size(y_new)-1]
     # Plot de la grafica
    #dataset.plot(x='Dias', y='Infectados', style='o')
    plot.plot(x_new, y_new, color='red', linewidth=3)
    plot.grid()
    plot.xlim(x_new_min,x_new_max)
    plot.ylim(0,y_new_max+100)
    title = 'Degree = {}; RMSE = {}; R2 = {}'.format(poly_degree, round(rmse,2), round(r2,2))
    plot.title('Predicciones de casos x dia en todo el mundo \n' + title, fontsize=10)
    plot.xlabel('Dias')
    plot.ylabel('No. Casos')

    plot.legend(('Regresion Poliminomial','Datos'))
    # use savefig() before show().
    plot.savefig("Reporte21.png")
    with open("Reporte21.png", "rb") as img_file:
        my_string =  base64.b64encode(img_file.read())
    #print(my_string.decode('utf-8'))
    #plot.show()
    img_file.close()
    plot.close()
    if round(val_r2) == 1:
        descripcionr2='es cercano a 1 Podemos concluir que el modelo lineal es adecuado para describir la relación que existe entre estas variables '
    else: 
        descripcionr2='es cercano a 0 Podemos concluir que el modelo lineal no es representativo lo que supone que el modelo no explica nada de la variación total de la variable Y ' 

    NombreReport = 'Predicciones de casos x dia en todo el mundo a una prediccion '+str(DiasPredicion)+' dias'
    conclusion = 'Predicciones de casos x dia en todo el mundo a una prediccion '+str(DiasPredicion)+' dias la ejecucion se hara con respecto a Casos Infectados x dia de un pais  al ejecutarlo podremos ver la prediccion la cual es '+str(prediction)+' de casos infectados en  '+str(DiasPredicion)+' si ira de alta o habra una baja.\n Al relizar la ejecucion podremos observar el valor RMSE: ' + str(val_rmse) +' nos da el error de 2 conjuntos entre los predichos y observados o conocidos, el R2:' + str(val_r2) +' ' + descripcionr2
    return jsonify({"message":"Analisis Realizado de Reporte21","image64":my_string.decode('utf-8'),"conclusion":conclusion,"NombreReport":NombreReport,"Grado":str(poly_degree),"rmse":str(val_rmse),"r2":str(val_r2),"prediccion":str(prediction)})

@app.route('/Analisis_Reporte211', methods = ['POST']) 
def Reporte211():
    body = {
        "var3":request.json['var3'],
        "var4":request.json['var4'],
        "var5":request.json['var5']
    }  

    encabezadoCasos = body['var3']
    encabezadoMuertes = body['var5']
    dias = body['var4']
    DiasPredicion = int(dias)
    print(DiasPredicion)

    print(body)
    # data 
    
    ''' comienza filtro''' 

    Datos =  dataset[encabezadoCasos]
    Datos = pd.DataFrame(Datos)

    TodosMuertes = dataset[encabezadoMuertes]
    print(TodosMuertes.count())
    vdias = []

    for i in range(TodosMuertes.count()):
        vdias.append(i)
    
    print(vdias)
    Dias = TodosMuertes.count()
    print(Dias)
    vinfectados = []
    for z in range(Dias):
        vinfectados.append(TodosMuertes.iloc[z])
    #print(vinfectados)

    y_new_max = max(vinfectados)
    x = np.asarray(vdias)[:,np.newaxis]
    y = np.asarray(vinfectados)[:,np.newaxis]
    plot.scatter(x,y)
    # Predecimos la Data
    poly_degree = 3 # duda del grado de la polinomia revisar
    polynomial_features = PolynomialFeatures(degree = poly_degree)
    x_transform = polynomial_features.fit_transform(x)

    # Procedemos a entrenar el modelo
    model = LinearRegression().fit(x_transform, y)
    # calculamos la varianza ,rmse y r2
    y_new = model.predict(x_transform)
    prediction = y_new[np.size(y_new)-1]

    rmse = np.sqrt(mean_squared_error(y, y_new))
    r2 = r2_score(y, y_new)

    print('RMSE: ', rmse)
    print('R2: ', r2)
    val_rmse = rmse
    val_r2 = r2

     # Prediccion desde el dia 0 hasta el dia que solicite
    x_new_min = 0.0
    x_new_max = DiasPredicion # le aumente la prediccion a 30 dias mas 


    x_new = np.linspace(x_new_min, x_new_max, Dias)
    x_new = x_new[:,np.newaxis]

    x_new_transform = polynomial_features.fit_transform(x_new)
    y_new = model.predict(x_new_transform)

    
    prediction = y_new[np.size(y_new)-1]
     # Plot de la grafica
    #dataset.plot(x='Dias', y='Infectados', style='o')
    plot.plot(x_new, y_new, color='red', linewidth=3)
    plot.grid()
    plot.xlim(x_new_min,x_new_max)
    plot.ylim(0,y_new_max+100)
    title = 'Degree = {}; RMSE = {}; R2 = {}'.format(poly_degree, round(rmse,2), round(r2,2))
    plot.title('Predicciones de muertes x Dia en todo el mundo \n' + title, fontsize=10)
    plot.xlabel('Dias')
    plot.ylabel('Muertos')

    plot.legend(('Regresion Poliminomial','Datos'))
    # use savefig() before show().
    plot.savefig("Reporte211.png")
    with open("Reporte211.png", "rb") as img_file:
        my_string =  base64.b64encode(img_file.read())
    #print(my_string.decode('utf-8'))
    #plot.show()
    img_file.close()
    plot.close()
    if round(val_r2) == 1:
        descripcionr2='es cercano a 1 Podemos concluir que el modelo lineal es adecuado para describir la relación que existe entre estas variables '
    else: 
        descripcionr2='es cercano a 0 Podemos concluir que el modelo lineal no es representativo lo que supone que el modelo no explica nada de la variación total de la variable Y ' 

    NombreReport = 'Predicciones de  Muertes x dia en todo el mundo a una prediccion '+str(DiasPredicion)+' dias'
    conclusion = 'Predicciones de Muertes x dia en todo el mundo a una prediccion '+str(DiasPredicion)+' dias la ejecucion se hara con respecto a  Muertes x dia de un pais  al ejecutarlo podremos ver la prediccion la cual es '+str(prediction)+' de mortalidad en los '+str(DiasPredicion)+' si ira de alta o habra una baja.\n Al relizar la ejecucion podremos observar el valor RMSE: ' + str(val_rmse) +' nos da el error de 2 conjuntos entre los predichos y observados o conocidos, el R2:' + str(val_r2) +' ' + descripcionr2
    return jsonify({"message":"Analisis Realizado de Reporte21","image64":my_string.decode('utf-8'),"conclusion":conclusion,"NombreReport":NombreReport,"Grado":str(poly_degree),"rmse":str(val_rmse),"r2":str(val_r2),"prediccion":str(prediction)})

''' FIN REPORTE 21 '''
#Tasa de mortalidad por coronavirus (COVID-19) en un país.
@app.route('/Analisis_Reporte22', methods = ['POST']) 
def Reporte22():
    body = {
        "var1":request.json['var1'],
        "var2":request.json['var2'],
        "var3":request.json['var3'],
        "var5":request.json['var5']
    }
    encabezadoPais = body['var1']   
    pais = body['var2']
    encabezadoConfirmados = body['var3']
    encabezadoMuertes = body['var5']
    
    print(body)
    # data 
    
    ''' comienza filtro para pais''' 
    print(encabezadoPais)

    Datos =  dataset.loc[dataset[encabezadoPais]==pais]
    Datos = pd.DataFrame(Datos)

    TodosMuertos = Datos[encabezadoMuertes]
    print(TodosMuertos.count()) 
    TodosConfirmados = Datos[encabezadoConfirmados]
    print(TodosConfirmados.count()) 
    print(encabezadoMuertes)

    vconfirmados = []    
    for i in range(TodosConfirmados.count()):
        vconfirmados.append(TodosConfirmados.iloc[i])
    
    #print(vdias)
    Dias = TodosMuertos.count()
    print(Dias)
    vmuertos = []
    for z in range(Dias):
        vmuertos.append(TodosMuertos.iloc[z])
    #print(vmuertos)

    y_new_max = max(vmuertos)
    x = np.asarray(vconfirmados)[:,np.newaxis]
    y = np.asarray(vmuertos)[:,np.newaxis]


    # Procedemos a entrenar el modelo
    model = LinearRegression().fit(x, y)
    # calculamos la varianza ,rmse y r2
    y_new = model.predict(x)

    rmse = np.sqrt(mean_squared_error(y, y_new))
    r2 = r2_score(y, y_new)

    print('RMSE: ', rmse)
    print('R2: ', r2)


    # Prediccion desde el dia 0 hasta el dia que solicite
    x_new_min = 0.0
    x_new_max = max(vconfirmados)

    # Plot de la grafica
    plot.xlim(x_new_min, x_new_max, max(vconfirmados))
    plot.ylim(0,y_new_max)

    plot.grid()
   
    title = 'Modelo : Y = {}; X+{}; RMSE = {}; R2 = {}'.format(str(model.coef_[0][0]),str(model.intercept_[0]),round(rmse,2), round(r2,2))
    plot.title('Tasa de mortalidad por coronavirus (COVID-19) en '+pais+"\n " + title, fontsize=10)
    plot.xlabel('No. Muertes')
    plot.ylabel('No. Casos Confirmados')
    plot.scatter(x, y)
    plot.plot(x, y_new, color='red')
    plot.legend(('Regresion Lineal','Datos'))
    # use savefig() before show().
    plot.savefig("Reporte22.png")
    with open("Reporte22.png", "rb") as img_file:
        my_string =  base64.b64encode(img_file.read())
    #print(my_string.decode('utf-8'))
    #plot.show()
    img_file.close()
    plot.close()
    if round(r2) == 1:
        descripcionr2='es cercano a 1 Podemos concluir que el modelo lineal es adecuado para describir la relación que existe entre estas variables '
    else: 
        descripcionr2='es cercano a 0 Podemos concluir que el modelo lineal no es representativo lo que supone que el modelo no explica nada de la variación total de la variable Y ' 

    NombreReport = 'Tasa de mortalidad por coronavirus (COVID-19) en '+pais
    conclusion ='Tasa de mortalidad por coronavirus (COVID-19) en '+pais+"\n "+' Modelo : Y = {}; X+{}; RMSE = {}; R2 = {}'.format(str(model.coef_[0][0]),str(model.intercept_[0]),round(rmse,2), round(r2,2)) + ' RMSE nos da el error de 2 conjuntos entre los predichos y observados o conocidos y R2 '+descripcionr2
    return jsonify({"message":"Analisis Realizado de Reporte 22","image64":my_string.decode('utf-8'),"conclusion":conclusion,"NombreReport":NombreReport,"rmse":str(rmse),"r2":str(r2),"modelo":'Y ='+str(model.coef_[0][0])+' X+'+str(model.intercept_[0])})

#Factores de muerte por COVID-19 en un país.                    ------>duda
@app.route('/Analisis_Reporte23', methods = ['POST']) 
def Reporte23():
    body = {
        "var1":request.json['var1'],
        "var2":request.json['var2'],
        "var18":request.json['var18']
    }   
    encabezadoPais = body['var1']
    pais = body['var2']
    encabezadoxFactor = body['var18']
    #Dias = int(dias) 
    print(body)
    # data 
    
    ''' comienza filtro para pais'''
    print(encabezadoPais)

    Datos =  dataset.loc[dataset[encabezadoPais]==pais]
    Datos = pd.DataFrame(Datos)
    
    TodosxFactor = Datos[encabezadoxFactor]

    #print(TodosxFactor.count())
    vdias = []
    t= 0
    for i in range(TodosxFactor.count()):
        vdias.append(i)
    
    #print(vdias)
    Dias = TodosxFactor.count()
    print(Dias)
    vinfectados = []
    for z in range(Dias):
        vinfectados.append(TodosxFactor.iloc[z])
    #print(vinfectados)
    
    y_new_max = max(vinfectados)
    x = np.asarray(vdias)[:,np.newaxis]
    y = np.asarray(vinfectados)[:,np.newaxis]
   # Procedemos a entrenar el modelo
    model = LinearRegression().fit(x, y)
    # calculamos la varianza ,rmse y r2
    y_new = model.predict(x)

    rmse = np.sqrt(mean_squared_error(y, y_new))
    r2 = r2_score(y, y_new)

    print('RMSE: ', rmse)
    print('R2: ', r2)


    # Prediccion desde el dia 0 hasta el dia que solicite
    x_new_min = 0.0
    x_new_max = Dias

    # Plot de la grafica
    plot.xlim(x_new_min, x_new_max, Dias)
    plot.ylim(0,y_new_max)

    plot.grid()
   
    title = 'Modelo : Y = {}; X+{}; RMSE = {}; R2 = {}'.format(str(model.coef_[0][0]),str(model.intercept_[0]),round(rmse,2), round(r2,2))
    plot.title('Factores de muerte por '+encabezadoxFactor+'en coronavirus  en '+pais+'\n' + title, fontsize=10)
    plot.xlabel('Dias')
    plot.ylabel('Factor x Muertes por ' + encabezadoxFactor)
    plot.scatter(x, y)
    plot.plot(x, y_new, color='red')
    plot.legend(('Regresion Lineal','Datos'))


    # use savefig() before show().
    plot.savefig("Reporte23.png")
    with open("Reporte23.png", "rb") as img_file:
        my_string =  base64.b64encode(img_file.read())
    img_file.close()
    plot.close()
    #plot.show()
    if round(r2) == 1:
        descripcionr2='es cercano a 1 Podemos concluir que el modelo lineal es adecuado para describir la relación que existe entre estas variables '
    else: 
        descripcionr2='es cercano a 0 Podemos concluir que el modelo lineal no es representativo lo que supone que el modelo no explica nada de la variación total de la variable Y ' 

    NombreReport = 'Factores de muerte por '+encabezadoxFactor+'en coronavirus  en '+pais
    conclusion ='Factores de muerte por '+encabezadoxFactor+'en coronavirus  en '+pais+"\n "+' Modelo : Y = {}; X+{}; RMSE = {}; R2 = {}'.format(str(model.coef_[0][0]),str(model.intercept_[0]),round(rmse,2), round(r2,2)) + ' RMSE nos da el error de 2 conjuntos entre los predichos y observados o conocidos y R2 '+descripcionr2
    return jsonify({"message":"Analisis Realizado de Reporte 23","image64":my_string.decode('utf-8'),"conclusion":conclusion,"NombreReport":NombreReport,"rmse":str(rmse),"r2":str(r2),"modelo":'Y ='+str(model.coef_[0][0])+' X+'+str(model.intercept_[0])})

''' INICIO REPORTE 24'''
#Comparación entre el número de casos detectados y el número de pruebas de un país.
@app.route('/Analisis_Reporte24', methods = ['POST']) 
def Reporte24():
    body = {
        "var1":request.json['var1'],
        "var2":request.json['var2'],
        "var3":request.json['var3'],
        "var17":request.json['var17']
    }
    encabezadoPais = body['var1']
    pais = body['var2']
    encabezadoPruebas = body['var17']   
    encabezadosCasos = body['var3']

    print(body)
    # data 
    
    ''' comienza filtro ''' 
    print(encabezadosCasos)
    Datos =  dataset.loc[dataset[encabezadoPais]==pais]
    Datos = pd.DataFrame(Datos)

    TodosCasos =  Datos[encabezadosCasos]
    #Datos = pd.DataFrame(Datos)

    TodosResultados = Datos[encabezadoPruebas]
    print(TodosResultados.count()) 
    print(encabezadoPruebas)

    vresultEntregados = []    
    for i in range(TodosResultados.count()):
        vresultEntregados.append(TodosResultados.iloc[i])
    
    #print(vdias)
    Dias = TodosResultados.count()
    print(Dias)
    vconfirmados = []
    for z in range(TodosCasos.count()):
        vconfirmados.append(z)
    #print(vmuertos)

    y_new_max = max(vresultEntregados)
    x = np.asarray(vconfirmados)[:,np.newaxis]
    y = np.asarray(vresultEntregados)[:,np.newaxis]


    plot.scatter(x,y)
    # Predecimos la Data
    poly_degree = 3
    polynomial_features = PolynomialFeatures(degree = poly_degree)
    x_transform = polynomial_features.fit_transform(x)

    # Procedemos a entrenar el modelo
    model = LinearRegression().fit(x_transform, y)
    # calculamos la varianza ,rmse y r2
    y_new = model.predict(x_transform)
    rmse = np.sqrt(mean_squared_error(y, y_new))
    r2 = r2_score(y, y_new)

    print('RMSE: ', rmse)
    print('R2: ', r2)
    val_rmse = rmse
    val_r2 = r2

    # Prediccion desde el dia 0 hasta el dia que solicite
    x_new_min = 0.0
    x_new_max = max(vconfirmados)


    x_new = np.linspace(x_new_min, x_new_max, max(vconfirmados))
    x_new = x_new[:,np.newaxis]

    x_new_transform = polynomial_features.fit_transform(x_new)
    y_new = model.predict(x_new_transform)
    # Plot de la grafica
    #dataset.plot(x='Dias', y='Infectados', style='o')
    plot.plot(x_new, y_new, color='red', linewidth=3)
    plot.grid()
    plot.xlim(x_new_min,x_new_max)
    plot.ylim(0,y_new_max+100)
    title = 'Degree = {}; RMSE = {}; R2 = {}'.format(poly_degree, round(rmse,2), round(r2,2))
    plot.title('Comparación entre el número de pruebas x Dia de '+pais+"\n " + title, fontsize=10)
    plot.xlabel('Dias')
    plot.ylabel('Resultado de Pruebas')

    plot.legend(('Regresion Poliminomial','Datos'))

    # use savefig() before show().
    plot.savefig("Reporte24.png")
    with open("Reporte24.png", "rb") as img_file:
        my_string =  base64.b64encode(img_file.read())
    #print(my_string.decode('utf-8'))
    #plot.show()
    img_file.close()
    plot.close()
    if round(r2) == 1:
        descripcionr2='es cercano a 1 Podemos concluir que el modelo lineal es adecuado para describir la relación que existe entre estas variables '
    else: 
        descripcionr2='es cercano a 0 Podemos concluir que el modelo lineal no es representativo lo que supone que el modelo no explica nada de la variación total de la variable Y ' 

    conclusion = 'Comparación entre el número de pruebas x Dia de  '+ pais + ' la ejecucion se hara con respecto a número de pruebas x Dia  al ejecutarlo podremos prever la tendencia que puede alcanzar proximos meses si ira de alta o habra una baja.\n Al realizar la ejecucion podremos observar el valor RMSE: ' + str(rmse) +' nos da el error de 2 conjuntos entre los predichos y observados o conocidos, el R2:' + str(r2) +' ' + descripcionr2
    NombreReport = 'Comparación entre el número de pruebas x Dia de  '+ pais
    #plot.show()
    return jsonify({"message":"Analisis Realizado de Reporte24","image64":my_string.decode('utf-8'),"conclusion":conclusion,"NombreReport":NombreReport,"Grado":str(poly_degree),"rmse":str(rmse),"r2":str(r2)})

@app.route('/Analisis_Reporte241', methods = ['POST']) 
def Reporte241():
    body = {
        "var1":request.json['var1'],
        "var2":request.json['var2'],
        "var3":request.json['var3'],
        "var17":request.json['var17']
    }
    encabezadoPais = body['var1']
    pais = body['var2']
    encabezadoPruebas = body['var17']   
    encabezadosCasos = body['var3']

    print(body)
    # data 
    
    ''' comienza filtro ''' 
    print(encabezadosCasos)
    Datos =  dataset.loc[dataset[encabezadoPais]==pais]
    Datos = pd.DataFrame(Datos)

    TodosCasos =  Datos[encabezadosCasos]
    #Datos = pd.DataFrame(Datos)

    TodosResultados = Datos[encabezadoPruebas]
    print(TodosResultados.count()) 
    print(encabezadoPruebas)

    vresultEntregados = []    
    for i in range(TodosResultados.count()):
        vresultEntregados.append(i)
    
    #print(vdias)
    Dias = TodosResultados.count()
    print(Dias)
    vconfirmados = []
    for z in range(TodosCasos.count()):
        vconfirmados.append(TodosCasos.iloc[z])
    #print(vmuertos)

    y_new_max = max(vconfirmados)
    x = np.asarray(vresultEntregados)[:,np.newaxis]
    y = np.asarray(vconfirmados)[:,np.newaxis]


    plot.scatter(x,y)
    # Predecimos la Data
    poly_degree = 3
    polynomial_features = PolynomialFeatures(degree = poly_degree)
    x_transform = polynomial_features.fit_transform(x)

    # Procedemos a entrenar el modelo
    model = LinearRegression().fit(x_transform, y)
    # calculamos la varianza ,rmse y r2
    y_new = model.predict(x_transform)
    rmse = np.sqrt(mean_squared_error(y, y_new))
    r2 = r2_score(y, y_new)

    print('RMSE: ', rmse)
    print('R2: ', r2)
    val_rmse = rmse
    val_r2 = r2

    # Prediccion desde el dia 0 hasta el dia que solicite
    x_new_min = 0.0
    x_new_max = max(vresultEntregados)


    x_new = np.linspace(x_new_min, x_new_max, max(vresultEntregados))
    x_new = x_new[:,np.newaxis]

    x_new_transform = polynomial_features.fit_transform(x_new)
    y_new = model.predict(x_new_transform)
    # Plot de la grafica
    #dataset.plot(x='Dias', y='Infectados', style='o')
    plot.plot(x_new, y_new, color='red', linewidth=3)
    plot.grid()
    plot.xlim(x_new_min,x_new_max)
    plot.ylim(0,y_new_max+100)
    title = 'Degree = {}; RMSE = {}; R2 = {}'.format(poly_degree, round(rmse,2), round(r2,2))
    plot.title('Comparación entre el número de casos detectados x Dia de '+pais+"\n " + title, fontsize=10)
    plot.xlabel(' Dias')
    plot.ylabel(' Casos Detectados')

    plot.legend(('Regresion Poliminomial','Datos'))

    # use savefig() before show().
    plot.savefig("Reporte24.png")
    with open("Reporte24.png", "rb") as img_file:
        my_string =  base64.b64encode(img_file.read())
    #print(my_string.decode('utf-8'))
    #plot.show()
    img_file.close()
    plot.close()
    if round(r2) == 1:
        descripcionr2='es cercano a 1 Podemos concluir que el modelo lineal es adecuado para describir la relación que existe entre estas variables '
    else: 
        descripcionr2='es cercano a 0 Podemos concluir que el modelo lineal no es representativo lo que supone que el modelo no explica nada de la variación total de la variable Y ' 

    conclusion = 'Comparación entre el número de casos detectados x Dia de  '+ pais + ' la ejecucion se hara con respecto a número de casos detectados x Dia  al ejecutarlo podremos prever la tendencia que puede alcanzar proximos meses si ira de alta o habra una baja.\n Al realizar la ejecucion podremos observar el valor RMSE: ' + str(rmse) +' nos da el error de 2 conjuntos entre los predichos y observados o conocidos, el R2:' + str(r2) +' ' + descripcionr2
    NombreReport = 'Comparación entre el número de casos detectados x Dia de  '+ pais
    #plot.show()
    return jsonify({"message":"Analisis Realizado de Reporte24","image64":my_string.decode('utf-8'),"conclusion":conclusion,"NombreReport":NombreReport,"Grado":str(poly_degree),"rmse":str(rmse),"r2":str(r2)})


'''FIN REPORTE 24'''
#Predicción de casos confirmados por día
@app.route('/Analisis_Reporte25', methods = ['POST']) 
def Reporte25():
    body = {
        "var3":request.json['var3'],
        "var15":request.json['var15'],
        "var4":request.json['var4']
    }
    encabezadoConfirmados = body['var3']   
    encabezadoResultados = body['var15']
    dias = body['var4']
    DiasPredicion = int(dias)
    print(body)
    # data 
    
    ''' comienza filtro ''' 
    print(encabezadoConfirmados)

    Datos =  dataset[encabezadoConfirmados]
    #Datos = pd.DataFrame(Datos)

    TodosResultados = dataset[encabezadoResultados]
    print(TodosResultados.count()) 
    print(encabezadoResultados)

    vresultEntregados = []    
    for i in range(TodosResultados.count()):
        vresultEntregados.append(TodosResultados.iloc[i])
    
    #print(vdias)
    Dias = TodosResultados.count()
    print(Dias)
    vconfirmados = []
    for z in range(Dias):
        vconfirmados.append(Datos.iloc[z])
    #print(vmuertos)

    y_new_max = max(vconfirmados)
    x = np.asarray(vresultEntregados)[:,np.newaxis]
    y = np.asarray(vconfirmados)[:,np.newaxis]


    plot.scatter(x,y)
    # Predecimos la Data
    poly_degree = 4
    polynomial_features = PolynomialFeatures(degree = poly_degree)
    x_transform = polynomial_features.fit_transform(x)

    # Procedemos a entrenar el modelo
    model = LinearRegression().fit(x_transform, y)
    # calculamos la varianza ,rmse y r2
    y_new = model.predict(x_transform)
    rmse = np.sqrt(mean_squared_error(y, y_new))
    r2 = r2_score(y, y_new)

    print('RMSE: ', rmse)
    print('R2: ', r2)
    val_rmse = rmse
    val_r2 = r2

    # Prediccion desde el dia 0 hasta el dia que solicite
    x_new_min = 0.0
    x_new_max = DiasPredicion


    x_new = np.linspace(x_new_min, x_new_max, Dias)
    x_new = x_new[:,np.newaxis]

    x_new_transform = polynomial_features.fit_transform(x_new)
    y_new = model.predict(x_new_transform)
    prediction = y_new[np.size(y_new)-1]
    # Plot de la grafica
    #dataset.plot(x='Dias', y='Infectados', style='o')
    plot.plot(x_new, y_new, color='red', linewidth=3)
    plot.grid()
    plot.xlim(x_new_min,x_new_max)
    plot.ylim(0,y_new_max+100)
    title = 'Degree = {}; RMSE = {}; R2 = {}'.format(poly_degree, round(rmse,2), round(r2,2))
    plot.title('Predicción de casos confirmados por día'+"\n " + title, fontsize=10)
    plot.xlabel('No. Resultados Entregados')
    plot.ylabel('No. Casos Confirmados')

    plot.legend(('Regresion Poliminomial','Datos'))

    # use savefig() before show().
    plot.savefig("Reporte25.png")
    with open("Reporte25.png", "rb") as img_file:
        my_string =  base64.b64encode(img_file.read())
    #print(my_string.decode('utf-8'))
    #plot.show()
    img_file.close()
    plot.close()
    if round(val_r2) == 1:
        descripcionr2='es cercano a 1 Podemos concluir que el modelo lineal es adecuado para describir la relación que existe entre estas variables '
    else: 
        descripcionr2='es cercano a 0 Podemos concluir que el modelo lineal no es representativo lo que supone que el modelo no explica nada de la variación total de la variable Y ' 

    NombreReport = 'Predicción de casos confirmados por '+ str(DiasPredicion) + ' dias'
    conclusion = 'Predicción de casos confirmados por '+ str(DiasPredicion) + ' dias la ejecucion se hara con respecto a casos confirmados por dias  al ejecutarlo podremos ver la prediccion la cual es '+str(prediction)+' de infectados en los '+str(DiasPredicion) +' si ira de alta o habra una baja.\n Al relizar la ejecucion podremos observar el valor RMSE: ' + str(val_rmse) +' nos da el error de 2 conjuntos entre los predichos y observados o conocidos, el R2:' + str(val_r2) +' ' + descripcionr2
    return jsonify({"message":"Analisis Realizado de Reporte25","image64":my_string.decode('utf-8'),"conclusion":conclusion,"NombreReport":NombreReport,"Grado":str(poly_degree),"rmse":str(val_rmse),"r2":str(val_r2),"prediccion":str(prediction)})
 

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')