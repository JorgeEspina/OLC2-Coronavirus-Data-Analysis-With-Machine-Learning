import { THIS_EXPR } from '@angular/compiler/src/output/output_ast';
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
  isComparation: boolean = false;
  isComparation1: boolean = false;
  Reporte: Reporte1 = {
    var1: '',
    var2: '',
    var3: '',
    var4: '',
    var5: '',
    var6: '',
    var7: '',
    var8: '',
    var9: '',
    var10: '',
    var11: '',
    var12: '',
    var13: '',
    var14: '',
    var15: '',
    var16: '',
    Datos: '',
    grupo: '', 
    image64: '',
    image64_1: '',
    image64_2: '',
    conclusion:'vamo a ganar',
    conclusion1:'1',
    conclusion2:'2',
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
          console.log(this.Reporte);

          this.analisisService.AnalisisReporte6(this.Reporte).subscribe(
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
        case "7":
          console.log(this.Reporte);

          this.analisisService.AnalisisReporte7(this.Reporte).subscribe(
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
        case "8":
          console.log(this.Reporte);

          this.analisisService.AnalisisReporte8(this.Reporte).subscribe(
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
        case "9":
          console.log(this.Reporte);

          this.analisisService.AnalisisReporte9(this.Reporte).subscribe(
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
        case "10":
          console.log(this.Reporte);
          this.analisisService.AnalisisReporte10(this.Reporte).subscribe(
            (res) => {
              console.log(res);
              this.Reporte.image64 = 'data:image/png;base64,';
              this.Reporte.image64 += res.image64;
              this.Reporte.conclusion = 'Conclusion del '+ this.Reporte.var2+' ';
              this.Reporte.conclusion +=  res.conclusion;
              this.Reporte.var2 = this.Reporte.var8;
              this.analisisService.AnalisisReporte10(this.Reporte).subscribe(
                (res) => {
                  console.log(res);
                  this.Reporte.image64_1 = 'data:image/png;base64,';
                  this.Reporte.image64_1 += res.image64;
                  this.Reporte.conclusion1 = 'Conclusion de '+ this.Reporte.var8 + ' ';
                  this.Reporte.conclusion1 +=  res.conclusion;
                },
                (err) => {
                  console.log(err)
                  alert("hubo un error al generar el analisis revise bien la parametrizacion de variables")
                 
                }
              );
            },
            (err) => {
              console.log(err)
              alert("hubo un error al generar el analisis revise bien la parametrizacion de variables")
             
            }
          );
          break;
        case "11":
          console.log(this.Reporte);

          this.analisisService.AnalisisReporte11(this.Reporte).subscribe(
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
        case "12":
          console.log(this.Reporte);

          this.analisisService.AnalisisReporte12(this.Reporte).subscribe(
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
        case "13":
          console.log(this.Reporte);         
          this.Reporte.grupo  =  '50';           
          this.analisisService.AnalisisReporte13(this.Reporte).subscribe(
            (res) => {
              console.log(res);
              this.Reporte.image64 = 'data:image/png;base64,';
              this.Reporte.image64 += res.image64;
              this.Reporte.conclusion = 'Conclusion de Muertes y Confirmados \n';
              this.Reporte.conclusion +=  res.conclusion;
              this.analisisService.AnalisisReporte13_1(this.Reporte).subscribe(
                (res) => {
                  console.log(res);
                  this.Reporte.image64_1 = 'data:image/png;base64,';
                  this.Reporte.image64_1 += res.image64;
                  this.Reporte.conclusion1 = 'Conclusion de Confirmados por edad \n';
                  this.Reporte.conclusion1 +=  res.conclusion;
                  this.analisisService.AnalisisReporte13_2(this.Reporte).subscribe(
                    (res) => {
                      console.log(res);
                      this.Reporte.image64_2 = 'data:image/png;base64,';
                      this.Reporte.image64_2 += res.image64;
                      this.Reporte.conclusion2 = 'Conclusion de Muertes por edad \n';
                      this.Reporte.conclusion2 +=  res.conclusion;
                    },
                    (err) => {
                      console.log(err)
                      alert("hubo un error al generar el analisis revise bien la parametrizacion de variables")
                     
                    }
                  );
                },
                (err) => {
                  console.log(err)
                  alert("hubo un error al generar el analisis revise bien la parametrizacion de variables")
                 
                }
              );
            },
            (err) => {
              console.log(err)
              alert("hubo un error al generar el analisis revise bien la parametrizacion de variables")
             
            }
          );
          break;
        case "14":
          console.log(this.Reporte);

          this.analisisService.AnalisisReporte14(this.Reporte).subscribe(
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
        case "15":
          console.log(this.Reporte);

          this.analisisService.AnalisisReporte15(this.Reporte).subscribe(
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
        case "16":
          console.log(this.Reporte);

          this.analisisService.AnalisisReporte16(this.Reporte).subscribe(
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

        case "17":
          console.log(this.Reporte);

          this.analisisService.AnalisisReporte17(this.Reporte).subscribe(
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
        case "18":
          console.log(this.Reporte);

          this.analisisService.AnalisisReporte18(this.Reporte).subscribe(
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
        case "19":
          console.log(this.Reporte);

          this.analisisService.AnalisisReporte19(this.Reporte).subscribe(
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
        case "20":
          console.log(this.Reporte);

          this.analisisService.AnalisisReporte20(this.Reporte).subscribe(
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

        case "21":
          console.log(this.Reporte);         
          this.analisisService.AnalisisReporte21(this.Reporte).subscribe(
            (res) => {
              console.log(res);
              this.Reporte.image64 = 'data:image/png;base64,';
              this.Reporte.image64 += res.image64;
              this.Reporte.conclusion = 'Conclusion Reporte 1 : \n';
              this.Reporte.conclusion +=  res.conclusion;
              this.analisisService.AnalisisReporte211(this.Reporte).subscribe(
                (res) => {
                  console.log(res);
                  this.Reporte.image64_1 = 'data:image/png;base64,';
                  this.Reporte.image64_1 += res.image64;
                  this.Reporte.conclusion1 = 'Conclusion Reporte 2:  \n';
                  this.Reporte.conclusion1 +=  res.conclusion;                  
                },
                (err) => {
                  console.log(err)
                  alert("hubo un error al generar el analisis revise bien la parametrizacion de variables")
                 
                }
              );
            },
            (err) => {
              console.log(err)
              alert("hubo un error al generar el analisis revise bien la parametrizacion de variables")
             
            }
          );
          break;
        case "22":
          console.log(this.Reporte);

          this.analisisService.AnalisisReporte22(this.Reporte).subscribe(
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
        case "23":
          console.log(this.Reporte);

          this.analisisService.AnalisisReporte23(this.Reporte).subscribe(
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
        case "24":
          console.log(this.Reporte);

          this.analisisService.AnalisisReporte24(this.Reporte).subscribe(
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
        case "25":
          console.log(this.Reporte);

          this.analisisService.AnalisisReporte25(this.Reporte).subscribe(
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
    if(this.verSeleccionCategoria==="10"){
      this.isComparation = true;
    }else if(this.verSeleccionCategoria==="13" ){
      this.isComparation1 = true;
      this.isComparation = true;
    }else if(this.verSeleccionCategoria==="21" ){
      this.isComparation = true;
    }else{
      this.isComparation = false;
      this.isComparation1 = false;
    }
    /*if(this.verSeleccionCategoria==="13" ){
      this.isComparation1 = true;
      this.isComparation = true;
    }else{
      this.isComparation = false;
      this.isComparation1 = false;
    }*/
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
