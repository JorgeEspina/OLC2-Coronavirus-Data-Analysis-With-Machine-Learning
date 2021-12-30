import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Reporte1 } from '../models/Report';

@Injectable({
  providedIn: 'root'
})
export class AnalisisService {

  constructor(private http: HttpClient) {}

  // Subir para analisis 
  Carga(config:FormData): Observable<any> {
    //console.log(config);
    return this.http.post('http://127.0.0.1:5000/Carga_Reporte',config);
  }
  // Analisis de Reportes
  AnalisisReporte1(reporte1:Reporte1): Observable<Reporte1> {
    return this.http.post('http://127.0.0.1:5000/Analisis_Reporte1',reporte1);
  }
  AnalisisReporte2(reporte2:Reporte1): Observable<Reporte1> {
    return this.http.post('http://127.0.0.1:5000/Analisis_Reporte2',reporte2);
  }
  AnalisisReporte3(reporte3:Reporte1): Observable<Reporte1> {
    return this.http.post('http://127.0.0.1:5000/Analisis_Reporte3',reporte3);
  }
  AnalisisReporte4(reporte4:Reporte1): Observable<Reporte1> {
    return this.http.post('http://127.0.0.1:5000/Analisis_Reporte4',reporte4);
  }
  AnalisisReporte5(reporte5:Reporte1): Observable<Reporte1> {
    return this.http.post('http://127.0.0.1:5000/Analisis_Reporte5',reporte5);
  }
}
