# Manual Técnico

_Proyecto de Organización de lenguajes y Compiladores 2_

## Proyecto #2 - Coronavirus Data Analysis With Machine Learning🚀
## Integrante💁

| Nombre:                     | Carné     |
| --------------------------- | --------- |
| JORGE DAVID ESPINA MOLINA   | 201403632 |

## 📋 Frontend - Metodos
## 📋 Model
    export interface Reporte1 {   
      var1?: string;
      var2?: string;
      var3?: string;
      var4?: string;
      .....
    }
En la Carpeta models se creo un modelo para los parametros a enviar al backend de una forma mas eficiente.
## 📋 Services - Analisis
  En la carpeta services manejamos el servicio para la comunicacion con flask de cada reporte como carga masiva etc.
  
    Carga(config:FormData): Observable<any> {
      return this.http.post(getUrl()+':5000/Carga_Reporte',config);
    }
## 📋 Component -Principal
    public async Analisis(){         
        try {  
          switch (this.verSeleccionCategoria) {
            case "1":
              this.analisisService.AnalisisReporte1(this.Reporte).subscribe(
                  (res) => {
                    console.log(res);
                    this.Reporte.image64 = 'data:image/png;base64,';
                    this.Reporte.image64 += res.image64;
                    this.Reporte.conclusion =  res.conclusion;
                    this.Reporte.NombreReport = res.NombreReport;
                    this.Reporte.r2 = res.r2;
                    this.Reporte.rmse = res.rmse;
                    this.Reporte.Grado = res.Grado;
                    
                  },
                  (err) => {
                    console.log(err)
                    alert("hubo un error al generar el analisis revise bien la parametrizacion de variables")
                  
                  }
                );
                break;
                ..
                ..
                ..
                ..
          }
        } catch (error) {
          alert(
            'error al generar analisis '
          );
        }
    }
El metodo analisis ejecutamos el analisis dependiendo que analisis desea hacer sin antes haberlo seleccionado.

### ReportePDF
    ReportePDF() {}

Genero los reportes para su descarga dependiendo que reporte haya seleccionado para su analisis.

### capturarCategorias
    capturarCategorias(){}

Para capturar el reporte que se desea analizar.

### changeListener

    public async changeListener(files1: FileList){}
  Este metodo me ayuda capturar toda la informacion del archivo de entrada que voy a proceder a analizar.


## 📋 Backend - Metodos
## Run 

    if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')

#### Parametros
- debug=true es para modo produccion 
- host = '0.0.0.0' nos sirve para que pueda acceder al servicio desde un lugar externo en nuestro caso se necesito para que se pudiera consumir.

Metodo por defecto que es en el cual inicia flask.

## Carga de Archivo 
    @app.route('/Carga_Reporte', methods = ['POST']) 
    def Carga():
      
      return jsonify({"message":"ARCHIVO RECIBIDO"})
  
Este metodo nos ayudara para saber primero que extension es el archivo y asi saber como leerlo.


## Analisis del reporte que se pide.
    @app.route('/Analisis_Reporte#', methods = ['POST']) 
    def Reporte#():
        return jsonify({"message":"Analisis Realizado de Reporte#","image64":my_string.decode('utf-8'),"conclusion":conclusion,"NombreReport":NombreReport,"Grado":str(poly_degree),"rmse":str(val_rmse),"r2":str(val_r2)})
En cada analisis de un reporte se retorna un json con una conclusion ya hecha y con datos necesarios que serviran para poner en la informacion de la generacion de los pdf.
Como tambien se retorna la imagen generada en base64 para poder mostrarla en la pagina web.
