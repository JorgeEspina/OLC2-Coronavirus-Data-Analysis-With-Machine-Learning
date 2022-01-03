import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Reporte1 } from '../models/Report';
import { getUrl } from '../../assets/env';

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
  AnalisisReporte6(reporte6:Reporte1): Observable<Reporte1> {
    return this.http.post('http://127.0.0.1:5000/Analisis_Reporte6',reporte6);
  }
  AnalisisReporte7(reporte7:Reporte1): Observable<Reporte1> {
    return this.http.post('http://127.0.0.1:5000/Analisis_Reporte7',reporte7);
  }
  AnalisisReporte8(reporte8:Reporte1): Observable<Reporte1> {
    return this.http.post('http://127.0.0.1:5000/Analisis_Reporte8',reporte8);
  }
  AnalisisReporte9(reporte9:Reporte1): Observable<Reporte1> {
    return this.http.post('http://127.0.0.1:5000/Analisis_Reporte9',reporte9);
  }
  AnalisisReporte10(reporte10:Reporte1): Observable<Reporte1> {
    return this.http.post('http://127.0.0.1:5000/Analisis_Reporte10',reporte10);
  }
  AnalisisReporte11(reporte11:Reporte1): Observable<Reporte1> {
    return this.http.post('http://127.0.0.1:5000/Analisis_Reporte11',reporte11);
  }
  AnalisisReporte12(reporte12:Reporte1): Observable<Reporte1> {
    return this.http.post('http://127.0.0.1:5000/Analisis_Reporte12',reporte12);
  }
  AnalisisReporte13(reporte13:Reporte1): Observable<Reporte1> {
    return this.http.post('http://127.0.0.1:5000/Analisis_Reporte13',reporte13);
  }
  AnalisisReporte13_1(reporte13:Reporte1): Observable<Reporte1> {
    return this.http.post('http://127.0.0.1:5000/Analisis_Reporte13_1',reporte13);
  }
  AnalisisReporte13_2(reporte13:Reporte1): Observable<Reporte1> {
    return this.http.post('http://127.0.0.1:5000/Analisis_Reporte13_2',reporte13);
  }
  AnalisisReporte14(reporte14:Reporte1): Observable<Reporte1> {
    return this.http.post('http://127.0.0.1:5000/Analisis_Reporte14',reporte14);
  }
  AnalisisReporte15(reporte15:Reporte1): Observable<Reporte1> {
    return this.http.post('http://127.0.0.1:5000/Analisis_Reporte15',reporte15);
  }
  AnalisisReporte16(reporte16:Reporte1): Observable<Reporte1> {
    return this.http.post('http://127.0.0.1:5000/Analisis_Reporte16',reporte16);
  }
  AnalisisReporte17(reporte17:Reporte1): Observable<Reporte1> {
    return this.http.post('http://127.0.0.1:5000/Analisis_Reporte17',reporte17);
  }
  AnalisisReporte18(reporte18:Reporte1): Observable<Reporte1> {
    return this.http.post('http://127.0.0.1:5000/Analisis_Reporte18',reporte18);
  }
  AnalisisReporte181(reporte18:Reporte1): Observable<Reporte1> {
    return this.http.post('http://127.0.0.1:5000/Analisis_Reporte181',reporte18);
  }
  AnalisisReporte19(reporte19:Reporte1): Observable<Reporte1> {
    return this.http.post('http://127.0.0.1:5000/Analisis_Reporte19',reporte19);
  }
  AnalisisReporte20(reporte20:Reporte1): Observable<Reporte1> {
    return this.http.post('http://127.0.0.1:5000/Analisis_Reporte20',reporte20);
  }
  AnalisisReporte21(reporte21:Reporte1): Observable<Reporte1> {
    return this.http.post('http://127.0.0.1:5000/Analisis_Reporte21',reporte21);
  }
  AnalisisReporte211(reporte21:Reporte1): Observable<Reporte1> {
    return this.http.post('http://127.0.0.1:5000/Analisis_Reporte211',reporte21);
  }
  AnalisisReporte22(reporte22:Reporte1): Observable<Reporte1> {
    return this.http.post('http://127.0.0.1:5000/Analisis_Reporte22',reporte22);
  }
  AnalisisReporte23(reporte23:Reporte1): Observable<Reporte1> {
    return this.http.post('http://127.0.0.1:5000/Analisis_Reporte23',reporte23);
  }
  AnalisisReporte24(reporte24:Reporte1): Observable<Reporte1> {
    return this.http.post('http://127.0.0.1:5000/Analisis_Reporte24',reporte24);
  }
  AnalisisReporte241(reporte24:Reporte1): Observable<Reporte1> {
    return this.http.post('http://127.0.0.1:5000/Analisis_Reporte241',reporte24);
  }
  AnalisisReporte25(reporte25:Reporte1): Observable<Reporte1> {
    return this.http.post('http://127.0.0.1:5000/Analisis_Reporte25',reporte25);
  }
  
}
