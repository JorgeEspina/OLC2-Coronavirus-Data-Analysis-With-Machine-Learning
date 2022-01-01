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
        #tipo = 1
    elif ext[1] == '.xlsx':
        dataset = pd.read_excel(Datos)
    elif ext[1] == '.json':
        dataset = pd.read_json(Datos)

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
    conclusion = 'Tendencia infeccion de Covid-19 en '+pais + ' con un contador y media como error de : ' + str(val_r2) +' y con un rme de ' + str(val_rmse)
    #plot.show()
    return jsonify({"message":"Analisis Realizado de Reporte1","image64":my_string.decode('utf-8'),"conclusion":conclusion})
 
#Predicción de Infertados en un País.
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

    # Plot de la grafica
    #dataset.plot(x='Dias', y='Infectados', style='o')
    plot.plot(x_new, y_new, color='red', linewidth=3)
    plot.grid()
    plot.xlim(x_new_min,x_new_max)
    plot.ylim(0,y_new_max)
    title = 'Degree = {}; RMSE = {}; R2 = {}'.format(poly_degree, round(rmse,2), round(r2,2))
    plot.title('Predicción de Infectados en  '+pais+"\n " + title, fontsize=10)
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
    conclusion = 'Predicción de Infectados en '+pais + ' con un contador y media como error de : ' + str(val_r2) +' y con un rme de ' + str(val_rmse)
    return jsonify({"message":"Analisis Realizado de Reporte2","image64":my_string.decode('utf-8'),"conclusion":conclusion})

#Indice de Progresión de la pandemia. --->falta
@app.route('/Analisis_Reporte3', methods = ['POST']) 
def Reporte3():
    # use savefig() before show().
    plot.savefig("Reporte3.png")
    with open("Reporte2.png", "rb") as img_file:
        my_string =  base64.b64encode(img_file.read())
    img_file.close()
    plot.close()
    #plot.show()
    conclusion = 'Predicción de Infectados en '
    return jsonify({"message":"Analisis Realizado de Reporte 3","image64":my_string.decode('utf-8'),"conclusion":conclusion})

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
    t= 0
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

    # Plot de la grafica
    #dataset.plot(x='Dias', y='Infectados', style='o')
    plot.plot(x_new, y_new, color='red', linewidth=3)
    plot.grid()
    plot.xlim(x_new_min,x_new_max)
    plot.ylim(0,y_new_max)
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
    conclusion ='Predicción de mortalidad por Covid-19 en el Departamento de '+departamento + ' con un contador y media como error de : ' + str(val_r2) +' y con un rme de ' + str(val_rmse)
    return jsonify({"message":"Analisis Realizado de Reporte 4","image64":my_string.decode('utf-8'),"conclusion":conclusion})

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
    poly_degree = 7 # duda del grado de la polinomia revisar
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
    conclusion ='Predicción de mortalidad por Covid-19 en '+pais + ' con un contador y media como error de : ' + str(val_r2) +' y con un rme de ' + str(val_rmse)
    return jsonify({"message":"Analisis Realizado de Reporte 5","image64":my_string.decode('utf-8'),"conclusion":conclusion})

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
    conclusion = 'Análisis del número de muertes por coronavirus en '+pais + 'Modelo : Y = {}; X+{}; RMSE = {}; R2 = {}'.format(str(model.coef_[0][0]),str(model.intercept_[0]),round(rmse,2), round(r2,2))
    return jsonify({"message":"Analisis Realizado de Reporte 6","image64":my_string.decode('utf-8'),"conclusion":conclusion})

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
    conclusion = 'Tendencia infeccion de Covid-19 por dia en '+pais + ' con un contador y media como error de : ' + str(r2) +' y con un rme de ' + str(rmse)
    return jsonify({"message":"Analisis Realizado de Reporte 7","image64":my_string.decode('utf-8'),"conclusion":conclusion})

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

    # Prediccion desde el dia 0 hasta el dia que solicite
    x_new_min = 0.0
    x_new_max = 365


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
    plot.title('Predicción de Infectados en  '+pais+"\n " + title, fontsize=10)
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
    conclusion = 'Predicción de casos de un país para un año.'
    return jsonify({"message":"Analisis Realizado de Reporte 8","image64":my_string.decode('utf-8'),"conclusion":conclusion})

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
    conclusion = 'Tendencia Vacunacion de Covid-19 de '+pais + ' con un contador y media como error de : ' + str(r2) +' y con un rme de ' + str(rmse)
    return jsonify({"message":"Analisis Realizado de Reporte 9","image64":my_string.decode('utf-8'),"conclusion":conclusion})

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
    plot.ylim(0,y_new_max)
    title = 'Degree = {}; RMSE = {}; R2 = {}'.format(poly_degree, round(rmse,2), round(r2,2))
    plot.title('Ánalisis Comparativo de Vacunaciópn entre '+pais+'\n' + title, fontsize=10)
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
    conclusion = 'Tendencia Vacunacion de Covid-19 de '+pais + ' con un contador y media como error de : ' + str(r2) +' y con un rme de ' + str(rmse)
    return jsonify({"message":"Analisis Realizado de Reporte 10","image64":my_string.decode('utf-8'),"conclusion":conclusion})

#Porcentaje de hombres infectados por covid-19 en un País desde el primer caso activo
@app.route('/Analisis_Reporte11', methods = ['POST']) 
def Reporte11():
    body = {
        "var1":request.json['var1'],
        "var2":request.json['var2'],
        "var3":request.json['var3'],
        "var10":request.json['var10'],
        "var11":request.json['var11']
    }   
    encabezadoPais = body['var1']
    pais = body['var2']
    encabezadoConfirmados = body['var3']
    encabezadoGenero = body['var10']
    hombre = body['var11']
    #Dias = int(dias) 
    print(body)
    # data 
    
    ''' comienza filtro para pais'''
    print(encabezadoPais)

    Datos =  dataset.loc[dataset[encabezadoPais]==pais]
    Datos = pd.DataFrame(Datos)
    
    Todoshombres = Datos.loc[Datos[encabezadoGenero]==hombre]

    Todosinfectados = Todoshombres[encabezadoConfirmados]
    
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
    plot.title('Porcentaje de hombres infectados por covid-19 en un '+pais + ' desde el primer caso activo\n ' + title, fontsize=10)
    plot.xlabel('Dias')
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
    conclusion = 'Porcentaje de hombres infectados por covid-19 en un '+pais + ' desde el primer caso activo  con un contador y media como error de : ' + str(val_r2) +' y con un rme de ' + str(val_rmse)
    #plot.show()
    return jsonify({"message":"Analisis Realizado de Reporte1","image64":my_string.decode('utf-8'),"conclusion":conclusion})

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
    conclusion = 'Muertes promedio por casos confirmados covid 19 en '+pais + ' con un contador y media como error de : ' + str(val_r2) +' y con un rme de ' + str(val_rmse)
    return jsonify({"message":"Analisis Realizado de Reporte13","image64":my_string.decode('utf-8'),"conclusion":conclusion})

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
    #print(my_string.decode('utf-8'))
    #plot.show()
    conclusion = 'Casos confirmados y edad de covid 19 en '+pais + ' con un contador y media como error de : ' + str(val_r2) +' y con un rme de ' + str(val_rmse)
    return jsonify({"message":"Analisis Realizado de Reporte13","image64":my_string1.decode('utf-8'),"conclusion":conclusion})

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
    plot.xlabel('Dias')
    plot.ylabel('Confirmados')

    plot.legend(('Regresion Poliminomial','Datos'))
    # use savefig() before show().
    plot.savefig("Reporte132.png")
    with open("Reporte132.png", "rb") as img_file:
        my_string =  base64.b64encode(img_file.read())
    img_file.close()
    plot.close()
    #print(my_string.decode('utf-8'))
    #plot.show()
    conclusion = 'Muertes promedio por  edad de covid 19 en '+pais + ' con un contador y media como error de : ' + str(val_r2) +' y con un rme de ' + str(val_rmse)
    return jsonify({"message":"Analisis Realizado de Reporte13","image64":my_string.decode('utf-8'),"conclusion":conclusion})


''' FIN CONSULTA DE REPORTE 13''' 
# Muertes según regiones de un país - Covid 19.
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
    
    # use savefig() before show().
    plot.savefig("Reporte15.png")
    with open("Reporte15.png", "rb") as img_file:
        my_string =  base64.b64encode(img_file.read())
    #print(my_string.decode('utf-8'))
    #plot.show()
    img_file.close()
    plot.close()
    conclusion = 'Porcentaje de hombres infectados por covid-19 en un ' + ' desde el primer caso activo  con un contador y media como error de : '+' y con un rme de ' 
    #plot.show()
    return jsonify({"message":"Analisis Realizado de Reporte15","image64":my_string.decode('utf-8'),"conclusion":conclusion})

#Porcentaje de muertes frente al total de casos en un país, región o continente.
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
    
    # use savefig() before show().
    plot.savefig("Reporte17.png")
    with open("Reporte17.png", "rb") as img_file:
        my_string =  base64.b64encode(img_file.read())
    #print(my_string.decode('utf-8'))
    #plot.show()
    img_file.close()
    plot.close()
    conclusion = 'Porcentaje de hombres infectados por covid-19 en un ' + ' desde el primer caso activo  con un contador y media como error de : '+' y con un rme de ' 
    #plot.show()
    return jsonify({"message":"Analisis Realizado de Reporte17","image64":my_string.decode('utf-8'),"conclusion":conclusion})

#Comportamiento y clasificación de personas infectadas por COVID-19 por municipio en un País.
@app.route('/Analisis_Reporte18', methods = ['POST']) 
def Reporte18():
    
    # use savefig() before show().
    plot.savefig("Reporte18.png")
    with open("Reporte18.png", "rb") as img_file:
        my_string =  base64.b64encode(img_file.read())
    #print(my_string.decode('utf-8'))
    #plot.show()
    img_file.close()
    plot.close()
    conclusion = 'Porcentaje de hombres infectados por covid-19 en un ' + ' desde el primer caso activo  con un contador y media como error de : '+' y con un rme de ' 
    #plot.show()
    return jsonify({"message":"Analisis Realizado de Reporte18","image64":my_string.decode('utf-8'),"conclusion":conclusion})

# Predicción de muertes en el último día del primer año de infecciones en un país.
@app.route('/Analisis_Reporte19', methods = ['POST']) 
def Reporte19():
    
    # use savefig() before show().
    plot.savefig("Reporte19.png")
    with open("Reporte19.png", "rb") as img_file:
        my_string =  base64.b64encode(img_file.read())
    #print(my_string.decode('utf-8'))
    #plot.show()
    img_file.close()
    plot.close()
    conclusion = 'Porcentaje de hombres infectados por covid-19 en un ' + ' desde el primer caso activo  con un contador y media como error de : '+' y con un rme de ' 
    #plot.show()
    return jsonify({"message":"Analisis Realizado de Reporte19","image64":my_string.decode('utf-8'),"conclusion":conclusion})

# Tasa de crecimiento de casos de COVID-19 en relación con nuevos casos diarios y tasa de muerte por COVID-19
@app.route('/Analisis_Reporte20', methods = ['POST']) 
def Reporte20():
    
    # use savefig() before show().
    plot.savefig("Reporte20.png")
    with open("Reporte20.png", "rb") as img_file:
        my_string =  base64.b64encode(img_file.read())
    #print(my_string.decode('utf-8'))
    #plot.show()
    img_file.close()
    plot.close()
    conclusion = 'Porcentaje de hombres infectados por covid-19 en un ' + ' desde el primer caso activo  con un contador y media como error de : '+' y con un rme de ' 
    #plot.show()
    return jsonify({"message":"Analisis Realizado de Reporte20","image64":my_string.decode('utf-8'),"conclusion":conclusion})

# Predicciones de casos y muertes en todo el mundo - Neural Network MLPRegressor
@app.route('/Analisis_Reporte21', methods = ['POST']) 
def Reporte21():
    
    # use savefig() before show().
    plot.savefig("Reporte21.png")
    with open("Reporte21.png", "rb") as img_file:
        my_string =  base64.b64encode(img_file.read())
    #print(my_string.decode('utf-8'))
    #plot.show()
    img_file.close()
    plot.close()
    conclusion = 'Porcentaje de hombres infectados por covid-19 en un ' + ' desde el primer caso activo  con un contador y media como error de : '+' y con un rme de ' 
    #plot.show()
    return jsonify({"message":"Analisis Realizado de Reporte21","image64":my_string.decode('utf-8'),"conclusion":conclusion})

#Tasa de mortalidad por coronavirus (COVID-19) en un país.
@app.route('/Analisis_Reporte22', methods = ['POST']) 
def Reporte22():
    
    # use savefig() before show().
    plot.savefig("Reporte22.png")
    with open("Reporte22.png", "rb") as img_file:
        my_string =  base64.b64encode(img_file.read())
    #print(my_string.decode('utf-8'))
    #plot.show()
    img_file.close()
    plot.close()
    conclusion = 'Porcentaje de hombres infectados por covid-19 en un ' + ' desde el primer caso activo  con un contador y media como error de : '+' y con un rme de ' 
    #plot.show()
    return jsonify({"message":"Analisis Realizado de Reporte22","image64":my_string.decode('utf-8'),"conclusion":conclusion})

#Factores de muerte por COVID-19 en un país.
@app.route('/Analisis_Reporte23', methods = ['POST']) 
def Reporte23():
    
    # use savefig() before show().
    plot.savefig("Reporte23.png")
    with open("Reporte23.png", "rb") as img_file:
        my_string =  base64.b64encode(img_file.read())
    #print(my_string.decode('utf-8'))
    #plot.show()
    img_file.close()
    plot.close()
    conclusion = 'Porcentaje de hombres infectados por covid-19 en un ' + ' desde el primer caso activo  con un contador y media como error de : '+' y con un rme de ' 
    #plot.show()
    return jsonify({"message":"Analisis Realizado de Reporte23","image64":my_string.decode('utf-8'),"conclusion":conclusion})

#Comparación entre el número de casos detectados y el número de pruebas de un país.
@app.route('/Analisis_Reporte24', methods = ['POST']) 
def Reporte24():
    
    # use savefig() before show().
    plot.savefig("Reporte21.png")
    with open("Reporte24.png", "rb") as img_file:
        my_string =  base64.b64encode(img_file.read())
    #print(my_string.decode('utf-8'))
    #plot.show()
    img_file.close()
    plot.close()
    conclusion = 'Porcentaje de hombres infectados por covid-19 en un ' + ' desde el primer caso activo  con un contador y media como error de : '+' y con un rme de ' 
    #plot.show()
    return jsonify({"message":"Analisis Realizado de Reporte24","image64":my_string.decode('utf-8'),"conclusion":conclusion})

#Predicción de casos confirmados por día
@app.route('/Analisis_Reporte24', methods = ['POST']) 
def Reporte25():
    
    # use savefig() before show().
    plot.savefig("Reporte25.png")
    with open("Reporte25.png", "rb") as img_file:
        my_string =  base64.b64encode(img_file.read())
    #print(my_string.decode('utf-8'))
    #plot.show()
    img_file.close()
    plot.close()
    conclusion = 'Porcentaje de hombres infectados por covid-19 en un ' + ' desde el primer caso activo  con un contador y media como error de : '+' y con un rme de ' 
    #plot.show()
    return jsonify({"message":"Analisis Realizado de Reporte25","image64":my_string.decode('utf-8'),"conclusion":conclusion})


if __name__ == '__main__':
    app.run(debug=True)