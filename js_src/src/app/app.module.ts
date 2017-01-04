import {NgModule} from '@angular/core';
import {BrowserModule}  from '@angular/platform-browser';
import {AppComponent} from './app.component';
import {DataService} from './data-services/data.service'
import {HttpModule} from "@angular/http";
import {OverviewComponent} from "./overview/overview.component";
import {Ng2AutoCompleteModule } from 'ng2-auto-complete';
import {FormsModule} from "@angular/forms";
import {CouncilComponent} from "./council-specific/council.component";
import {ScatterChartComponent} from "./council-specific/council.scatter.component";
import {CouncilPriceScatterComponent} from "./council-specific/council.scatterprice.component";
import {WordCloudComponent} from "./council-specific/word-cloud/council.wordcloud.component";
import {PdfChartComponent} from "./council-specific/council-pdf/council.pdf.council";
import {CouncilCorrelationComponent} from "./council-specific/council.correlation.component";
import {CouncilCategoryStatsComponent} from "./council-specific/council.categorystats.component";

@NgModule({
    imports: [
        BrowserModule,
        HttpModule,
        Ng2AutoCompleteModule,
        FormsModule,
    ],
    declarations: [
        AppComponent,
        OverviewComponent,
        CouncilComponent,
        ScatterChartComponent,
        CouncilPriceScatterComponent,
        WordCloudComponent,
        PdfChartComponent,
		CouncilCorrelationComponent,
		CouncilCategoryStatsComponent,
    ],
    bootstrap: [AppComponent],
    entryComponents: [AppComponent],
    providers: [DataService]
})
export class AppModule { }
