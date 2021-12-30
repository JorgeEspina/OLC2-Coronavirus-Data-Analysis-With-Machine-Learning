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


@app.route('/Analisis_Reporte1', methods = ['POST']) 
def Reporte1():
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
    val_rmse = rmse
    val_r2 = r2

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
    plot.title('Predicción de Infectados en  '+pais+"\n " + title, fontsize=10)
    plot.xlabel('Dias')
    plot.ylabel('Infectados')

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

@app.route('/Analisis_Reporte4', methods = ['POST']) 
def Reporte4():
    body = {
        "var6":request.json['var6'],
        "var7":request.json['var7'],
        "var5":request.json['var5'],
        "var4":request.json['var4']
    }   
    encabezadoDepartamento = body['var6']
    departamento = body['var7']
    encabezadoMuertes = body['var5']
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
    print(encabezadoDepartamento)

    Datos =  dataset.loc[dataset[encabezadoDepartamento]==departamento]
    Datos = pd.DataFrame(Datos)

    Todosinfectados = Datos[encabezadoMuertes]
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
    plot.title('Predicción de mortalidad por Covid-19 en el Departamento de  '+departamento+"\n " + title, fontsize=10)
    plot.xlabel('Dias')
    plot.ylabel('Muertes')

    # use savefig() before show().
    plot.savefig("Reporte4.png")
    with open("Reporte4.png", "rb") as img_file:
        my_string =  base64.b64encode(img_file.read())
    img_file.close()
    plot.close()
    #plot.show()
    conclusion ='Predicción de mortalidad por Covid-19 en el Departamento de '+departamento + ' con un contador y media como error de : ' + str(val_r2) +' y con un rme de ' + str(val_rmse)
    return jsonify({"message":"Analisis Realizado de Reporte 4","image64":my_string.decode('utf-8'),"conclusion":conclusion})


@app.route('/Analisis_Reporte5', methods = ['POST']) 
def Reporte5():
    body = {
        "var1":request.json['var1'],
        "var2":request.json['var2'],
        "var5":request.json['var5'],
        "var4":request.json['var4']
    }   
    encabezadoPais = body['var1']
    pais = body['var2']
    encabezadoMuertes = body['var5']
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

    Todosinfectados = Datos[encabezadoMuertes]
    vinfectados = []
    for z in range(Dias):
        vinfectados.append(Todosinfectados.iloc[z])
    print(vinfectados)

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
    plot.title('Predicción de mortalidad por Covid-19 en  '+pais+"\n " + title, fontsize=10)
    plot.xlabel('Dias')
    plot.ylabel('Muertes')

    # use savefig() before show().
    plot.savefig("Reporte5.png")
    with open("Reporte5.png", "rb") as img_file:
        my_string =  base64.b64encode(img_file.read())
    img_file.close()
    plot.close()
    #plot.show()
    conclusion ='Predicción de mortalidad por Covid-19 en '+pais + ' con un contador y media como error de : ' + str(val_r2) +' y con un rme de ' + str(val_rmse)
    return jsonify({"message":"Analisis Realizado de Reporte 5","image64":my_string.decode('utf-8'),"conclusion":conclusion})

if __name__ == '__main__':
    app.run(debug=True)