import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { PrincipalComponent } from './componente/principal/principal.component';

const routes: Routes = [ {
  
  path: 'Principal',
  component: PrincipalComponent,
},
{ path: '', redirectTo: '/Principal', pathMatch: 'full' },];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule {

 }
