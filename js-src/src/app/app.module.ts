import {NgModule} from '@angular/core';
import {BrowserModule}  from '@angular/platform-browser';
import {AppComponent} from './app.component';
import {DataService} from './data-services/data.service'
import {OverviewComponent} from './overview/overview.component'
import {HttpModule} from "@angular/http";
import {ScatterChartComponent} from "./council-specific/overview.scatter.component";
import {Ng2AutoCompleteModule} from "ng2-auto-complete/dist/index";
import {CouncilComponent} from "./council-specific/council.component";
import {NgbModule} from "@ng-bootstrap/ng-bootstrap";

@NgModule({
    imports: [
        BrowserModule,
        HttpModule,
        Ng2AutoCompleteModule,
        NgbModule
    ],
    declarations: [
        AppComponent,
        OverviewComponent,
        ScatterChartComponent,
        CouncilComponent,
    ],
    bootstrap: [AppComponent],
    providers: [DataService]
})
export class AppModule { }
