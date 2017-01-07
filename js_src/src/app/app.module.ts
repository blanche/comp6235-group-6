import {NgModule} from '@angular/core';
import {BrowserModule}  from '@angular/platform-browser';
import {AppComponent} from './app.component';
import {DataService} from './data-services/data.service'
import {HttpModule} from "@angular/http";
import {OverviewComponent} from "./overview/overview.component";
import {Ng2AutoCompleteModule } from 'ng2-auto-complete';
import {FormsModule} from "@angular/forms";
import {MdRadioModule} from "@angular2-material/radio";
import { MdUniqueSelectionDispatcher } from '@angular2-material/core';

//Council imports
import {CouncilComponent} from "./council-specific/council.component";
import {CouncilPriceScatterComponent} from "./council-specific/council.scatterprice.component";
import {WordCloudComponent} from "./council-specific/word-cloud/council.wordcloud.component";
import {PdfChartComponent} from "./council-specific/council-pdf/council.pdf.council";
import {CouncilCorrelationComponent} from "./council-specific/council.correlation.component";
import {CouncilCategoryStatsComponent} from "./council-specific/council.categorystats.component";
import {CouncilLowerThanAvgStats} from "./council-specific/council.lowerThanAvgStats.component";
//Category Imports
import {CategoryComponent} from "./category-specific/category.component";
import {TopBottomFiveGraphComponent} from "./category-specific/top_bottom_five/category.topbottomfive.component";

@NgModule({
    imports: [
        BrowserModule,
        HttpModule,
        Ng2AutoCompleteModule,
        FormsModule,
        MdRadioModule
    ],
    declarations: [
        AppComponent,
        OverviewComponent,
        CouncilComponent,
        CouncilPriceScatterComponent,
        WordCloudComponent,
        PdfChartComponent,
        CouncilCorrelationComponent,
        CouncilCategoryStatsComponent,
        CouncilLowerThanAvgStats,
        CategoryComponent,
        TopBottomFiveGraphComponent
    ],
    bootstrap: [AppComponent],
    entryComponents: [AppComponent],
    providers: [DataService, MdUniqueSelectionDispatcher]
})
export class AppModule { }
