import { THIS_EXPR } from '@angular/compiler/src/output/output_ast';
import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { Reporte1 } from '../../models/Report';
import { AnalisisService } from '../../service/analisis.service'
import jsPDF from 'jspdf'
import autoTable from 'jspdf-autotable'

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
  /*REPORTES VARIBALES PARA QUE MUESTRE LOS CAMPOS */
  isReport: boolean = false;
  isReport1: boolean = false;
  isReport2: boolean = false;
  isReport3: boolean = false;
  isReport4: boolean = false;
  isReport5: boolean = false;
  isReport6: boolean = false;
  isReport7: boolean = false;
  isReport8: boolean = false;
  isReport9: boolean = false;
  isReport10: boolean = false;
  isReport11: boolean = false;
  isReport12: boolean = false;
  isReport13: boolean = false;
  isReport14: boolean = false;
  isReport15: boolean = false;
  isReport16: boolean = false;
  isReport17: boolean = false;
  isReport18: boolean = false;
  isReport19: boolean = false;
  isReport20: boolean = false;
  isReport21: boolean = false;
  isReport22: boolean = false;
  isReport23: boolean = false;
  isReport24: boolean = false;

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
    var17: '',
    var18: '',
    var19: '',
    var20: '',
    var21: '',
    NombreReport: ' ',
    NombreReport1: ' ',
    NombreReport2: ' ',
    Datos: '',
    grupo: '', 
    image64: '',
    image64_1: '',
    image64_2: '',
    conclusion:'vamo a ganar',
    conclusion1:'1',
    conclusion2:'2',
    report1x: [],
    report1y: [],
    rmse:'',
    r2:'',
    prediccion:'',
    Grado:'',
    rmse_1:'',
    r2_1:'',
    rmse_2:'',
    r2_2:'',
    prediccion1:'',
    Grado1:'',
    Grado2:'',
    modelo:'',
    modelo1:'',
    Formula:'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAPkAAADGCAYAAAAQYyboAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAE0WSURBVHhe7d3ll23HdTb6/CX5km/JCI1xE2fc68SJk9h5zTHltRRbtmUxMzMzM4PFzMzMzIxHzHykuutXR0+7tL27z2npULdrjjF7rVVcteYz5yxYu/+sfFa+QJ999ln59NNPJ3gu/qxz586LjBu8hadDICwHhl93n302t3wy99Py4itvlLEgb/lTPCTq3LnzIuIRzOHp0LRB3qlTS6PCF+609NBXB7n4zn+yPOFCzp1br4Qo184LnzPe0yGvahTk2DSgg7zzWP7s00HgBh78yPr86WARPvrgw/LJRx+XTz7+pHz6yQB4PIR3Xjj8ySeflI8//ngC7NMhqTvIO0+LA3LC5/r+e++X22+9rVx+6WXlysuvKDdef0Plm264sfNC4FtuvqU89thj5Z133ilzP/eYpkNeWwd552lxQD53sNqfDRb71ZdeLrvssGPZcL31yx677lYOP+TQcthBB5fDDj6k88Lgww4rl156aXnppZcWOshfAHJBU9LnL77znxIPfwYmbHMHkD//3PNli823KBecf0F55JFHymOPPloef+zxxc+PP16eePyJCX7yiSfKU08+NfP5qafKyy+/XD788MMK0um66+jzV/b5n2EK8Nnc8vHgiT3/6oKAvNOfHBEyAHdlWZ577rmy5ZZbljvvvHMe8IewWJzOC4cD7oz9tKkCHDcgH8p5/rUO8k5jqAW569NPP1223Xbbcu+9904I5ZICeQuG2cTp35emDvJO06UAyvWJwS3ecccdy/3337/ELfgoOGYDtX350v2SpbI/w1i1IB+GTZJOnSaIkAVQtnYeeuihstdee1WQC5/MXY+ATsbKck3alCG8DWvj3Ic9J2w2Ufo3ej8tkqWyPx3kneZDhCxgsnd73333lf322688/PDDNfzLgjx5sh/cPie/sDYuebHnhHUaoQ7yTtOhFlAAeMcdd5SDDjqorgInfLogT3zSyv/+++9XK25V2bP70XJHy0hYpxHqIO80XQqoPvroo3LTTTeVww8/vLz44osTQBvHLSBHuU1DcVixv/XWW6viAHbXBx54oLz11lt/lH5cGZ1GaCqQD85Rh3mnL1ALKlb2uuuuK8ccc0w9rCFsnBXHyTeOkyaW++abby4bbrhhOfroo8szzzxTLrzwwnLSSSdV8E9WZhvWaYQ6yDtNh1pgffDBB+Wqq64qJ5xwQj2wEYC3aRaEA1D5eQfXXHNN+fWvf13WXHPNcv3115czzjijnHbaaeX111//ApjHleG+0wh1kHeaDrXAAvJLLrmknHzyyRWAXxbkOPnee++9WubOO+9c1l577ToV4ClcccUVVQFMVn4H+RTUQd5pOtQCy3z5vPPOq1b2zTff/MJ213RZXtdXX321nHXWWeWCCy6oq/arr7562Xvvvcs999wzpRLpIJ+COsg7TYdaYLG6Z599duW33367grCNHwfIgHE0LgrCCTruv1V7rvrvfve7summm5Ynn3yylp86RstonzuNUAd5p+lQQIV9/nj66adX9xrgEw+IXOuAchw4w8JztbLuDLwFtwcffLACe//99y9HHnlktfApe7SclO9eXKcR6iDvNB0CooCM9WZ1r7zyygpQBGyssjgHZLjZtr5iqQPE0XvxyvA12S233FIX8pTh2CzrLm6yvLiDfArqIO80XQq4WPLf//735eqrr54AGbCyupdddlnZZJNNyu67716ef/75Gh4FMI4DVPN8zBPA4lK2q7pTTsJHgd9phDrIO02XAiouOpDbRgvoWFxfpFkR/9WvflXWX3/98uyzz06AOcC1H26xzv76nDlzKrsPs+T4lVdembiGX3vttXpVfyx8B/kU1EHeaboUkHOnjz/++LpABmwBOcD6YMUnqFtvvXU9DRer64p5Aaz9xhtvXFZdddWy+eab122zXXbZpey6667VA9htt92+cMXSWIjbaaed6uLcu+++O1FmB/kk1EHeaToUgGMW9dhjj61HWwNyzFpz2QFym222qaAPCF1ZcuD0s0b/9V//Vf78z/+8LLPMMrUsW3JOuF100UX1aisNuz/33HNrml/+8pfl3/7t38qJJ55Y60ndMxHk2jvKC50qwLE/HeQLjRbLy1sCpB8BMwvNLbdQBtgt0LnTQL7ddtv9EcgxoEuz7777lr/6q78q//mf/1lPtr3xxhv1kI15uSu3PuxZvH35n/70p/Woa7buUv5MG2dtbnmRtF+Rlf1ZTCCP0IfbsMnuRzlxLY2Ln4zb+IVBbdlhLy0CHSFMWHvf8mh4nhM2Gjd6betfFKRc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gagtL8BqwxPWAgvPj1LOaHn+3ZH/jHLPPfeUJ554ovbB/yXXTuFArK3CX3755XL55ZeXQw89tOy4447lmGOOKa+88kotJz/R3Gkpogpw7M/wvjvIvxwRcETIX3vttXL00UfX//y5/PLLl1122aXsueeeZbfddqv/+vdnP/tZOfbYY8ubb7458b+/r7766nL22WeX+++/vwI+AASYAFHZ0rf/m6wF+IKAS7nKUYaysPrUe/zxx9e27r///uX2228vTz75ZLnwwgvr/yUX7z+YygfkwrVZP9ddd936b43zX1U6LWXUQb5wKJYRCAj7VVddVf/F77LLLlsuvfTSahH9R1DgWG655SqQKIO33367xu+3334VNG+88UYFyocfflivAXkAHoAG6NMFecoKyNXD7b7ooouqkrnpppvq9dxzz63AffzxxyuQ99133/q/z+TRv5deeqm2/7zzzqtt17/0f0Ha0WkxUgU49qeD/EsTwY51JeivvvpqFf4f/OAHFdBAAVysICsOHOayQLTzzjuXU045pbrrQMSys5wPPfRQdZlZUO7/LbfcUt3igDzWPmDPfZ4n41jz1HXrrbdW5fPoo49WpXPnnXeWM888s9YJ0K5ALizeh7bfdttt5Ywzzih33313bWPKHVdnpyVIHeQLhyLMAEbYWUjz27XWWqtadCAynxX+wgsvVNADysUXX1w233zzctddd1XgAvUdd9xR9tprr7LNNttUwEl72GGHlbXXXruWGZBj9QGWOgOy3Ie1K+ndJw0AP/zww+WII44o6623XrniiiuqcqJwtNv6gTZz50877bSyxx57VEWg3RTDySefXL0Prj0PBPiVPU7JdFqC1EG+cCjCHJAHROeff375/ve/X0H0wAMP1DBgAwiAPvjgg8tWW21V3V3hwrj1LP2aa65ZLSXrb3GLMhBHUaSOgBwDHwXCrcYACcTcbp6BvAArD9aW5557rlx55ZVlpZVWKkcddVRVKNq8/fbbV08ibTWl0B6LiNrKsq+zzjplhx12qItv6qEQ0qYW4LjTEqQO8oVDEeaA3JXQc8F33XXX8r3vfa8CFkCBBniAEkC22267Oi8WDniu3PhNN920HHDAARVUXGXg405TBNKpRzkBOWCfeOKJdfFMuQFgmELheis/7ZRf3VtvvXWdNlAIp59+erXc6pJGm62mr7DCChXs5uI8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'
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
        case "2":
          console.log(this.Reporte);

          this.analisisService.AnalisisReporte2(this.Reporte).subscribe(
            (res) => {
              console.log(res);
              this.Reporte.image64 = 'data:image/png;base64,';
              this.Reporte.image64 += res.image64;
              this.Reporte.conclusion =  res.conclusion;
              this.Reporte.NombreReport = res.NombreReport;
              this.Reporte.r2 = res.r2;
              this.Reporte.rmse = res.rmse;
              this.Reporte.Grado = res.Grado;
              this.Reporte.prediccion =res.prediccion;
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
              this.Reporte.NombreReport = res.NombreReport;
              this.Reporte.r2 = res.r2;
              this.Reporte.rmse = res.rmse;
              this.Reporte.modelo= res.modelo;
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
              this.Reporte.NombreReport = res.NombreReport;
              this.Reporte.r2 = res.r2;
              this.Reporte.rmse = res.rmse;
              this.Reporte.Grado = res.Grado;
              this.Reporte.prediccion =res.prediccion;
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
              this.Reporte.NombreReport = res.NombreReport;
              this.Reporte.r2 = res.r2;
              this.Reporte.rmse = res.rmse;
              this.Reporte.Grado = res.Grado;
              this.Reporte.prediccion =res.prediccion;
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
              this.Reporte.NombreReport = res.NombreReport;
              this.Reporte.r2 = res.r2;
              this.Reporte.rmse = res.rmse;
              this.Reporte.modelo= res.modelo;
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
              this.Reporte.NombreReport = res.NombreReport;
              this.Reporte.r2 = res.r2;
              this.Reporte.rmse = res.rmse;
              this.Reporte.Grado = res.Grado;
              this.Reporte.prediccion =res.prediccion;
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
              this.Reporte.NombreReport = res.NombreReport;
              this.Reporte.r2 = res.r2;
              this.Reporte.rmse = res.rmse;
              this.Reporte.Grado = res.Grado;
              this.Reporte.prediccion =res.prediccion;
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
              this.Reporte.NombreReport = res.NombreReport;
              this.Reporte.r2 = res.r2;
              this.Reporte.rmse = res.rmse;
              this.Reporte.Grado= res.Grado;
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
              this.Reporte.conclusion = 'Conclusion 1:';
              this.Reporte.conclusion +=  res.conclusion;
              this.Reporte.var2 = this.Reporte.var8;
              this.Reporte.NombreReport = res.NombreReport;
              this.Reporte.r2 = res.r2;
              this.Reporte.rmse = res.rmse;
              this.Reporte.Grado = res.Grado
              this.analisisService.AnalisisReporte10(this.Reporte).subscribe(
                (res) => {
                  console.log(res);
                  this.Reporte.image64_1 = 'data:image/png;base64,';
                  this.Reporte.image64_1 += res.image64;
                  this.Reporte.conclusion1 = 'Conclusion 2: ';
                  this.Reporte.conclusion1 +=  res.conclusion;
                  this.Reporte.NombreReport1 = res.NombreReport;
                  this.Reporte.r2_1 = res.r2;
                  this.Reporte.rmse_1 = res.rmse;
                  this.Reporte.Grado1 = res.Grado
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
              this.Reporte.NombreReport = res.NombreReport;
              this.Reporte.r2 = res.r2;
              this.Reporte.rmse = res.rmse;
              this.Reporte.Grado= res.Grado;
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
              this.Reporte.NombreReport = res.NombreReport;
              this.Reporte.r2 = res.r2;
              this.Reporte.rmse = res.rmse;
              this.Reporte.Grado= res.Grado;
              this.analisisService.AnalisisReporte13_1(this.Reporte).subscribe(
                (res) => {
                  console.log(res);
                  this.Reporte.image64_1 = 'data:image/png;base64,';
                  this.Reporte.image64_1 += res.image64;
                  this.Reporte.conclusion1 = 'Conclusion de Confirmados por edad \n';
                  this.Reporte.conclusion1 +=  res.conclusion;
                  this.Reporte.NombreReport1 = res.NombreReport;
                  this.Reporte.r2_1 = res.r2;
                  this.Reporte.rmse_1 = res.rmse;
                  this.Reporte.Grado1= res.Grado;
                  this.analisisService.AnalisisReporte13_2(this.Reporte).subscribe(
                    (res) => {
                      console.log(res);
                      this.Reporte.image64_2 = 'data:image/png;base64,';
                      this.Reporte.image64_2 += res.image64;
                      this.Reporte.conclusion2 = 'Conclusion de Muertes por edad \n';
                      this.Reporte.conclusion2 +=  res.conclusion;
                      this.Reporte.NombreReport2 = res.NombreReport;
                      this.Reporte.r2_2 = res.r2;
                      this.Reporte.rmse_2 = res.rmse;
                      this.Reporte.Grado2= res.Grado;
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
              this.Reporte.NombreReport = res.NombreReport;
              this.Reporte.r2 = res.r2;
              this.Reporte.rmse = res.rmse;
              this.Reporte.Grado= res.Grado;
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
              this.Reporte.NombreReport = res.NombreReport;
              this.Reporte.r2 = res.r2;
              this.Reporte.rmse = res.rmse;
              this.Reporte.modelo= res.modelo;
            },
            (err) => {
              console.log(err)
              alert("hubo un error al generar el analisis revise bien la parametrizacion de variables")
             
            }
          );
          break;
        case "18":
          console.log(this.Reporte);

          console.log(this.Reporte);         
          this.analisisService.AnalisisReporte18(this.Reporte).subscribe(
            (res) => {
              console.log(res);
              this.Reporte.image64 = 'data:image/png;base64,';
              this.Reporte.image64 += res.image64;
              this.Reporte.conclusion = 'Conclusion Reporte 1 : \n';
              this.Reporte.conclusion +=  res.conclusion;
              this.Reporte.NombreReport = res.NombreReport;
              this.Reporte.r2 = res.r2;
              this.Reporte.rmse = res.rmse;
              this.Reporte.modelo= res.modelo;
              /*this.analisisService.AnalisisReporte181(this.Reporte).subscribe(
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
              );*/
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
              this.Reporte.NombreReport = res.NombreReport;
              this.Reporte.r2 = res.r2;
              this.Reporte.rmse = res.rmse;
              this.Reporte.Grado= res.Grado;
              this.Reporte.prediccion = res.prediccion;
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
              this.Reporte.NombreReport = res.NombreReport;
              this.Reporte.r2 = res.r2;
              this.Reporte.rmse = res.rmse;
              this.Reporte.Grado= res.Grado;
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
              this.Reporte.NombreReport = res.NombreReport;
              this.Reporte.r2 = res.r2;
              this.Reporte.rmse = res.rmse;
              this.Reporte.Grado = res.Grado;
              this.Reporte.prediccion = res.prediccion;
              this.analisisService.AnalisisReporte211(this.Reporte).subscribe(
                (res) => {
                  console.log(res);
                  this.Reporte.image64_1 = 'data:image/png;base64,';
                  this.Reporte.image64_1 += res.image64;
                  this.Reporte.conclusion1 = 'Conclusion Reporte 2:  \n';
                  this.Reporte.conclusion1 +=  res.conclusion;      
                  this.Reporte.NombreReport1 = res.NombreReport;
                  this.Reporte.r2_1 = res.r2;
                  this.Reporte.rmse_1 = res.rmse;
                  this.Reporte.Grado1 = res.Grado;
                  this.Reporte.prediccion1 = res.prediccion;            
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
              this.Reporte.NombreReport = res.NombreReport;
              this.Reporte.r2 = res.r2;
              this.Reporte.rmse = res.rmse;
              this.Reporte.modelo= res.modelo;
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
              this.Reporte.NombreReport = res.NombreReport;
              this.Reporte.r2 = res.r2;
              this.Reporte.rmse = res.rmse;
              this.Reporte.modelo= res.modelo;
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
              this.Reporte.conclusion = 'Conclusion 1:';
              this.Reporte.conclusion +=  res.conclusion;
              this.Reporte.NombreReport = res.NombreReport;
              this.Reporte.r2 = res.r2;
              this.Reporte.rmse = res.rmse;
              this.Reporte.Grado= res.Grado;
              this.analisisService.AnalisisReporte241(this.Reporte).subscribe(
                (res) => {
                  console.log(res);
                  this.Reporte.image64_1 = 'data:image/png;base64,';
                  this.Reporte.image64_1 += res.image64;
                  this.Reporte.conclusion1 = 'Conclusion 2: ';
                  this.Reporte.conclusion1 +=  res.conclusion;
                  this.Reporte.NombreReport = res.NombreReport;
                  this.Reporte.r2_1 = res.r2;
                  this.Reporte.rmse_1 = res.rmse;
                  this.Reporte.Grado1= res.Grado;
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
        case "25":
          console.log(this.Reporte);

          this.analisisService.AnalisisReporte25(this.Reporte).subscribe(
            (res) => {
              console.log(res);
              this.Reporte.image64 = 'data:image/png;base64,';
              this.Reporte.image64 += res.image64;
              this.Reporte.conclusion =  res.conclusion;
              this.Reporte.NombreReport = res.NombreReport;
              this.Reporte.r2 = res.r2;
              this.Reporte.rmse = res.rmse;
              this.Reporte.Grado= res.Grado;
              this.Reporte.prediccion = res.prediccion;
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
      console.log("Entramos");
      const doc = new jsPDF()
      autoTable(doc, { html: '#my-table' })
      autoTable(doc, {
        head: [['Carnet', 'Nombre','Curso']],
        body: [
          ['201403632', 'Jorge David Espina Molina','Organización de Lenguajes y Compiladores 2']
        ],
      })
      doc.setFont('times');
      if(this.isReport===true){ //TENDENCIA
        autoTable(doc, {
          //head: [['Tendencia de la infección por Covid-19 en un País']],
          head: [[this.Reporte.NombreReport]],
          body: [['RMSE:'+this.Reporte.rmse],['R2:'+this.Reporte.r2],['Grado de Polinomial:'+this.Reporte.Grado]],        
        })
        doc.addImage(this.Reporte.Formula, 'png', 20, 130, 80, 50)
        //doc.text(this.Reporte.NombreReport,35,50);
        //doc.text('Tendencia de la infección por Covid-19 en un País',25,50);
        doc.addImage(this.Reporte.image64, 'png', 20, 170, 140, 120)
        autoTable(doc, {
          head: [['Conclusion de analisis:']],
          body: [[this.Reporte.conclusion]],        
        })
      }else if(this.isReport1===true||this.isReport3===true||this.isReport4===true||this.isReport6===true||this.isReport7===true||this.isReport18===true||this.isReport24===true){//PREDICCION 
        autoTable(doc, {
          //head: [['Tendencia de la infección por Covid-19 en un País']],
          head: [[this.Reporte.NombreReport]],
          body: [['RMSE:'+this.Reporte.rmse],['R2:'+this.Reporte.r2],['Grado de Polinomial:'+this.Reporte.Grado],['Prediccion:'+this.Reporte.prediccion]],        
        })
        doc.addImage(this.Reporte.Formula, 'png', 20, 130, 80, 50)
        //doc.text(this.Reporte.NombreReport,35,50);
        //doc.text('Tendencia de la infección por Covid-19 en un País',25,50);
        doc.addImage(this.Reporte.image64, 'png', 20, 170, 140, 120)
        autoTable(doc, {
          head: [['Conclusion de analisis:']],
          body: [[this.Reporte.conclusion]],        
        })
        //doc.addPage()
      }else if(this.isReport2===true||this.isReport5===true||this.isReport16===true||this.isReport17===true||this.isReport21===true||this.isReport22===true){ // LINEAL
        autoTable(doc, {
          //head: [['Tendencia de la infección por Covid-19 en un País']],
          head: [[this.Reporte.NombreReport]],
          body: [['RMSE:'+this.Reporte.rmse],['R2:'+this.Reporte.r2],['Modelo:'+this.Reporte.modelo]],        
        })
        doc.addImage(this.Reporte.Formula, 'png', 20, 130, 80, 50)
        //doc.text(this.Reporte.NombreReport,35,50);
        //doc.text('Tendencia de la infección por Covid-19 en un País',25,50);
        doc.addImage(this.Reporte.image64, 'png', 20, 170, 140, 120)
        autoTable(doc, {
          head: [['Conclusion de analisis:']],
          body: [[this.Reporte.conclusion]],        
        })
      }else if(this.isReport8===true||this.isReport10===true||this.isReport14===true||this.isReport19===true){//ANALISIS POR POLINOMIAL SIN PREDICCION
        autoTable(doc, {
          head: [[this.Reporte.NombreReport]],
          body: [['RMSE:'+this.Reporte.rmse],['R2:'+this.Reporte.r2],['Grado de Polinomial:'+this.Reporte.Grado]],        
        })
        doc.addImage(this.Reporte.Formula, 'png', 20, 130, 70, 40)
        //doc.text(this.Reporte.NombreReport,35,50);
        //doc.text('Tendencia de la infección por Covid-19 en un País',25,50);
        doc.addImage(this.Reporte.image64, 'png', 20, 170, 140, 120)
        autoTable(doc, {
          head: [['Conclusion de analisis:']],
          body: [[this.Reporte.conclusion]],        
        })
      }else if(this.isReport9===true){//para dos paises analisis comparativo
        autoTable(doc, {
          head: [['Analisis Comparativo de vacunacion entre 2 paises']],
          body: [['RMSE:'+this.Reporte.rmse],['R2:'+this.Reporte.r2],['Grado de Polinomial:'+this.Reporte.Grado]],        
        })
        //doc.text(this.Reporte.NombreReport,35,50);
        //doc.text('Tendencia de la infección por Covid-19 en un País',25,50);
        doc.addImage(this.Reporte.image64, 'png', 20, 170, 140, 120)
        autoTable(doc, {
          head: [['Conclusion de analisis:']],
          body: [[this.Reporte.conclusion]],        
        })
        doc.addImage(this.Reporte.Formula, 'png', 50, 120, 80, 50)
        doc.addPage()
        autoTable(doc, {
          head: [[this.Reporte.NombreReport1]],
          body: [['RMSE:'+this.Reporte.rmse_1],['R2:'+this.Reporte.r2_1],['Grado de Polinomial:'+this.Reporte.Grado1]],        
        })
        //doc.text(this.Reporte.NombreReport,35,50);
        //doc.text('Tendencia de la infección por Covid-19 en un País',25,50);
        doc.addImage(this.Reporte.image64_1, 'png', 20, 130, 140, 120)
        autoTable(doc, {
          head: [['Conclusion de analisis:']],
          body: [[this.Reporte.conclusion1]],        
        })
      }else if(this.isReport12===true){ // analisis de 3 imagenes
        autoTable(doc, {
          head: [[this.Reporte.NombreReport]],
          body: [['RMSE:'+this.Reporte.rmse],['R2:'+this.Reporte.r2],['Grado de Polinomial:'+this.Reporte.Grado]],        
        })
        doc.addImage(this.Reporte.image64, 'png', 20, 170, 140, 120)
        autoTable(doc, {
          head: [['Conclusion de analisis:']],
          body: [[this.Reporte.conclusion]],        
        })
        doc.addImage(this.Reporte.Formula, 'png', 50, 120, 80, 50)
        doc.addPage()
        autoTable(doc, {
          head: [[this.Reporte.NombreReport1]],
          body: [['RMSE:'+this.Reporte.rmse_1],['R2:'+this.Reporte.r2_1],['Grado de Polinomial:'+this.Reporte.Grado1]],        
        })
        //doc.text(this.Reporte.NombreReport,35,50);
        //doc.text('Tendencia de la infección por Covid-19 en un País',25,50);
        doc.addImage(this.Reporte.image64_1, 'png', 20, 130, 140, 120)
        autoTable(doc, {
          head: [['Conclusion de analisis:']],
          body: [[this.Reporte.conclusion1]],        
        })
        doc.addPage()
        autoTable(doc, {
          head: [[this.Reporte.NombreReport2]],
          body: [['RMSE:'+this.Reporte.rmse_2],['R2:'+this.Reporte.r2_2],['Grado de Polinomial:'+this.Reporte.Grado2]],        
        })
        //doc.text(this.Reporte.NombreReport,35,50);
        //doc.text('Tendencia de la infección por Covid-19 en un País',25,50);
        doc.addImage(this.Reporte.image64_2, 'png', 20, 130, 140, 120)
        autoTable(doc, {
          head: [['Conclusion de analisis:']],
          body: [[this.Reporte.conclusion2]],        
        })

      }else if(this.isReport20===true){
        //console.log(this.Reporte)
        autoTable(doc, {
          head: [[this.Reporte.NombreReport]],
          body: [['RMSE:'+this.Reporte.rmse],['R2:'+this.Reporte.r2],['Grado de Polinomial:'+this.Reporte.Grado],['Prediccion:'+this.Reporte.prediccion]],        
        })
        //doc.text(this.Reporte.NombreReport,35,50);
        //doc.text('Tendencia de la infección por Covid-19 en un País',25,50);
        doc.addImage(this.Reporte.image64, 'png', 20, 170, 120, 100)
        autoTable(doc, {
          head: [['Conclusion de analisis:']],
          body: [[this.Reporte.conclusion]],        
        })
        doc.addImage(this.Reporte.Formula, 'png', 50, 140, 60, 30)
        doc.addPage()
        autoTable(doc, {
          head: [[this.Reporte.NombreReport1]],
          body: [['RMSE:'+this.Reporte.rmse_1],['R2:'+this.Reporte.r2_1],['Grado de Polinomial:'+this.Reporte.Grado1],['Prediccion:'+this.Reporte.prediccion1]],        
        })
        //doc.text(this.Reporte.NombreReport,35,50);
        //doc.text('Tendencia de la infección por Covid-19 en un País',25,50);
        doc.addImage(this.Reporte.image64_1, 'png', 20, 130, 140, 120)
        autoTable(doc, {
          head: [['Conclusion de analisis:']],
          body: [[this.Reporte.conclusion1]],        
        })
      }else if(this.isReport23===true){
        autoTable(doc, {
          head: [[this.Reporte.NombreReport]],
          body: [['RMSE:'+this.Reporte.rmse],['R2:'+this.Reporte.r2],['Grado de Polinomial:'+this.Reporte.Grado]],        
        })
        //doc.text(this.Reporte.NombreReport,35,50);
        //doc.text('Tendencia de la infección por Covid-19 en un País',25,50);
        doc.addImage(this.Reporte.image64, 'png', 20, 170, 120, 100)
        autoTable(doc, {
          head: [['Conclusion de analisis:']],
          body: [[this.Reporte.conclusion]],        
        })
        doc.addImage(this.Reporte.Formula, 'png', 50, 140, 60, 30)
        doc.addPage()
        autoTable(doc, {
          head: [[this.Reporte.NombreReport1]],
          body: [['RMSE:'+this.Reporte.rmse_1],['R2:'+this.Reporte.r2_1],['Grado de Polinomial:'+this.Reporte.Grado1]],        
        })
        //doc.text(this.Reporte.NombreReport,35,50);
        //doc.text('Tendencia de la infección por Covid-19 en un País',25,50);
        doc.addImage(this.Reporte.image64_1, 'png', 20, 130, 140, 120)
        autoTable(doc, {
          head: [['Conclusion de analisis:']],
          body: [[this.Reporte.conclusion1]],        
        })
      /*}else if(this.isReport1===true){
      }else if(this.isReport1===true){*/
      }
     
      //doc.text('Conclusion de analisis:',35,185);

      doc.save(this.Reporte.NombreReport+'.pdf')
  }
  limpiarParametrizacion(){
      this.isReport = false;
      this.isReport1 = false;
      this.isReport2 = false;
      this.isReport3 = false;
      this.isReport4 = false;
      this.isReport5 = false;
      this.isReport6 = false;
      this.isReport7 = false;
      this.isReport8 = false;
      this.isReport9 = false;
      this.isReport10 = false;
      this.isReport11 = false;
      this.isReport12 = false;
      this.isReport13 = false;
      this.isReport14 = false;
      this.isReport15 = false;
      this.isReport16 = false;
      this.isReport17 = false;
      this.isReport18 = false;
      this.isReport19 = false;
      this.isReport20 = false;
      this.isReport21 = false;
      this.isReport22 = false;
      this.isReport23 = false;
      this.isReport24 = false;
  }
  capturarCategorias() {  
    this.verSeleccionCategoria = this.categoriaSeleccionado;
    console.log(this.verSeleccionCategoria);
    this.limpiarParametrizacion();
    this.isComparation = false;
    this.isComparation1 = false;
    if(this.verSeleccionCategoria==="1"){
      this.isReport = true;
    }else if(this.verSeleccionCategoria==="2"){
      this.isReport1 = true;
    }else if(this.verSeleccionCategoria==="3"){
      this.isReport2 = true;
    }else if(this.verSeleccionCategoria==="4"){
      this.isReport3 = true;
    }else if(this.verSeleccionCategoria==="5"){
      this.isReport4 = true;
    }else if(this.verSeleccionCategoria==="6"){
      this.isReport5 = true;
    }else if(this.verSeleccionCategoria==="7"){
      this.isReport6 = true;
    }else if(this.verSeleccionCategoria==="8"){
      this.isReport7 = true;
    }else if(this.verSeleccionCategoria==="9"){
      this.isReport8 = true;
    }else if(this.verSeleccionCategoria==="10"){
      this.isReport9 = true;
      this.isComparation = true;
    }else if(this.verSeleccionCategoria==="11"){
      this.isReport10 = true;
    }else if(this.verSeleccionCategoria==="12"){
      this.isReport11 = true;
    }else if(this.verSeleccionCategoria==="13"){
      this.isReport12 = true;
      this.isComparation1 = true;
      this.isComparation = true;
    }else if(this.verSeleccionCategoria==="14"){
      this.isReport13 = true;
    }else if(this.verSeleccionCategoria==="15"){
      this.isReport14 = true;
    }else if(this.verSeleccionCategoria==="16"){
      this.isReport15 = true;
    }else if(this.verSeleccionCategoria==="17"){
      this.isReport16 = true;
    }else if(this.verSeleccionCategoria==="18"){
      this.isReport17 = true;
    }else if(this.verSeleccionCategoria==="19"){
      this.isReport18 = true;
    }else if(this.verSeleccionCategoria==="20"){
      this.isReport19 = true;
    }else if(this.verSeleccionCategoria==="21"){
      this.isReport20 = true;
      this.isComparation = true;
    }else if(this.verSeleccionCategoria==="22"){
      this.isReport21 = true;
    }else if(this.verSeleccionCategoria==="23"){
      this.isReport22 = true;
    }else if(this.verSeleccionCategoria==="24"){
      this.isReport23 = true;
      this.isComparation = true;
    }else if(this.verSeleccionCategoria==="25"){
      this.isReport24 = true;
    }else{
      this.isComparation = false;
      this.isComparation1 = false;
      this.isReport = true;
      this.isReport1 = true;
      this.isReport2 = true;
      this.isReport3 = true;
      this.isReport4 = true;
      this.isReport5 = true;
      this.isReport6 = true;
      this.isReport7 = true;
      this.isReport8 = true;
      this.isReport9 = true;
      this.isReport10 = true;
      this.isReport11 = true;
      this.isReport12 = true;
      this.isReport13 = true;
      this.isReport14 = true;
      this.isReport15 = true;
      this.isReport16 = true;
      this.isReport17 = true;
      this.isReport18 = true;
      this.isReport19 = true;
      this.isReport20 = true;
      this.isReport21 = true;
      this.isReport22 = true;
      this.isReport23 = true;
      this.isReport24 = true;
      
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
