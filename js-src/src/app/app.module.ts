import {NgModule} from '@angular/core';
import {BrowserModule}  from '@angular/platform-browser';
import {AppComponent} from './app.component';
import {DataService} from './data-services/data.service'
import {OverviewComponent} from './overview/overview.component'
import {HttpModule} from "@angular/http";
import {GoogleChart} from './directives/angular2-google-chart.directive';
import {ScatterChartComponent} from "./overview/overview.scatter.component";

@NgModule({
    imports: [
        BrowserModule,
        HttpModule
    ],
    declarations: [
        AppComponent,
        OverviewComponent,
        ScatterChartComponent,
    ],
    bootstrap: [AppComponent],
    providers: [DataService]
})
export class AppModule { }
