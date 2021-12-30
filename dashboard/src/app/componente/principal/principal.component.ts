import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { Reporte1 } from '../../models/Report';
import { AnalisisService } from '../../service/analisis.service'
@Component({
  selector: 'app-principal',
  templateUrl: './principal.component.html',
  styleUrls: ['./principal.component.css']
})
export class PrincipalComponent implements OnInit {
  // para selecion de tipo
  categoriaSeleccionado: string = null;
  verSeleccionCategoria: string = null;
  Reporte: Reporte1 = {
    var1: '',
    var2: '',
    var3: '',
    var4: '',
    var5: '',
    var6: '',
    var7: '',
    var8: '',
    Datos: '', 
    image64: '',
    conclusion:'vamo a ganar',
    report1x: [],
    report1y: []
  };
  constructor(private router: Router,private activedRoute: ActivatedRoute,private analisisService: AnalisisService) { }

  ngOnInit(): void {
  }
  public async changeListener(files1: FileList){
    //console.log(files1);
    if(files1 && files1.length > 0) {
      let file : File = files1.item(0); 
        console.log(file.name);
        //console.log(file.size);
        //console.log(file.type);
        let reader: FileReader = new FileReader();
        reader.readAsText(file);
        reader.onload = (e) => {
           let Datos: string = reader.result as string;
           //console.log(Datos);
           this.Reporte.Datos = Datos;           
        }
     }
    const f = new FormData();
    for(let i =0; i<files1.length;i++){
      f.append("files",files1[i]);
    }
    try {      
      this.analisisService.Carga(f).subscribe(
        (res) => {
          console.log(res);
          //this.Reporte.image64 = 'data:image/png;base64,';
          //this.Reporte.image64 += res.image64;
        },
        (err) => {
          console.log(err)
          alert('Hubo un error al cargar el archivo');
          location.reload();

        }
      );
    } catch (error) {
      alert(
        'error al generar reporte '
      );
    }
  }

  public async Analisis(){
         
    try {  
      switch (this.verSeleccionCategoria) {
        case "1":
          console.log("entramos bien al que seleccionamos 1");
          /*let valoresx: number[] = [];
          let valoresy: number[] = [];
          let dias = parseInt(this.Reporte.var2);
          for (let i = 0; i < dias; i++) {
            valoresx.push(i);
          }
          //console.log(valoresx)
          this.Reporte.report1x =  valoresx;
          /* split para obtener datos del pais */
         /* var salto = this.Reporte.Datos.split(this.Reporte.var1); 
          //console.log(salto.length)
          //for (let i = 0; i <= salto.length; i++) {
            var pais = salto[1]; 
            var valor =  dias + 3          
            let infectados = pais.split(",",valor);
            //console.log(infectados)
            for (let j = 3; j < infectados.length; j++) {      
                console.log(infectados[j]) 
                var valy = Number(infectados[j]);
                valoresy.push(valy);
                /*if((j<(dias+3))===true){
                console.log(infectados[j])
                //valoresy.push(infectados[i]);
              }  */            
            //}
          //}
         // this.Reporte.report1y= valoresy;
          console.log(this.Reporte);

          this.analisisService.AnalisisReporte1(this.Reporte).subscribe(
            (res) => {
              console.log(res);
              this.Reporte.image64 = 'data:image/png;base64,';
              this.Reporte.image64 += res.image64;
              this.Reporte.conclusion =  res.conclusion;
            },
            (err) => {
              console.log(err)
              alert("hubo un error al generar el analisis revise bien la parametrizacion de variables")
             
            }
          );
          break;
        case "2":
          console.log(this.Reporte);

          this.analisisService.AnalisisReporte2(this.Reporte).subscribe(
            (res) => {
              console.log(res);
              this.Reporte.image64 = 'data:image/png;base64,';
              this.Reporte.image64 += res.image64;
              this.Reporte.conclusion =  res.conclusion;
            },
            (err) => {
              console.log(err)
              alert("hubo un error al generar el analisis revise bien la parametrizacion de variables")
             
            }
          );
          break;
        case "3":
          console.log(this.Reporte);

          this.analisisService.AnalisisReporte3(this.Reporte).subscribe(
            (res) => {
              console.log(res);
              this.Reporte.image64 = 'data:image/png;base64,';
              this.Reporte.image64 += res.image64;
              this.Reporte.conclusion =  res.conclusion;
            },
            (err) => {
              console.log(err)
              alert("hubo un error al generar el analisis revise bien la parametrizacion de variables")
             
            }
          );
          break;
        case "4":
          console.log(this.Reporte);

          this.analisisService.AnalisisReporte4(this.Reporte).subscribe(
            (res) => {
              console.log(res);
              this.Reporte.image64 = 'data:image/png;base64,';
              this.Reporte.image64 += res.image64;
              this.Reporte.conclusion =  res.conclusion;
            },
            (err) => {
              console.log(err)
              alert("hubo un error al generar el analisis revise bien la parametrizacion de variables")
             
            }
          );
          break;
        case "5":
          console.log(this.Reporte);

          this.analisisService.AnalisisReporte5(this.Reporte).subscribe(
            (res) => {
              console.log(res);
              this.Reporte.image64 = 'data:image/png;base64,';
              this.Reporte.image64 += res.image64;
              this.Reporte.conclusion =  res.conclusion;
            },
            (err) => {
              console.log(err)
              alert("hubo un error al generar el analisis revise bien la parametrizacion de variables")
             
            }
          );
          break;
        case "6":
        
          break;
        case "7":
        
          break;
        case "8":
        
          break;
        case "9":
        
          break;
        case "10":
        
          break;
        case "11":
        
          break;
        case "12":
        
          break;
        case "13":
        
          break;
        case "14":
        
          break;
        case "15":
        
          break;
        case "16":
        
          break;

        case "17":
        
          break;
        case "18":
        
          break;
        case "19":
        
          break;
        case "20":
        
          break;

        case "21":
        
         break;
        case "22":
        
         break;
        case "23":
        
          break;
        case "24":
      
          break;
        case "25":
      
        break;
    
        default:
          break;
      } 
    } catch (error) {
      alert(
        'error al generar analisis '
      );
    }
  }
  ReportePDF(){

  }
  capturarCategorias() {  
    this.verSeleccionCategoria = this.categoriaSeleccionado;
    console.log(this.verSeleccionCategoria);
    /*if(this.verSeleccionCategoria == "Todas Categorias"){
      this.isLoggedProveedor = false;
      this.isLoggedCliente = false;
    }else if(this.verSeleccionCategoria == "Proveedor"){
      this.isLoggedProveedor = false;
      this.isLoggedCliente = true;
    }else if(this.verSeleccionCategoria == "Cliente"){
      this.isLoggedCliente = false;
      this.isLoggedProveedor = true;
    }*/
  }
}
