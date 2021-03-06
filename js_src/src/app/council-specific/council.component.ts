/**
 * Created by ayoung on 21/11/16.
 */
import {Component, OnInit} from '@angular/core';
import {DataService} from "../data-services/data.service";
import {COUNCILNAMES} from "./councilNames.Array";

@Component({
    // moduleId: module.id,
    selector: 'council',
    templateUrl:'./council.component.html',
    styleUrls: ['./council.component.css'],
})

export class CouncilComponent implements OnInit {

    public authStatsData : any;
    public selectedCouncil : string;
    public councilList : Array<string>;


    public setDefaultStats(): void{
        this.authStatsData = {
            hygieneMean:0,
            hygieneStdev:0,
            hygieneMode:0,
			hygieneMedian:0,
            googleMean:0,
            googleStdev:0,
            googleMode:0,
			googleMedian:0,
            yelpMean:0,
            yelpStdev:0,
            yelpMode:0,
			yelpMedian:0
        };
    }

    constructor(private dataService: DataService) {
        this.setDefaultStats();
        dataService.newAuthoritesStatsDataAnnounced$.subscribe(
          newAuthoritiesStatsData => this.updateStatsData(newAuthoritiesStatsData)
        );
    };

    public updateStatsData(data:any):void{
      if (data.length != 0) {
          this.authStatsData = data[0]
      }
    }

    ngOnInit(): void {
        this.councilList = COUNCILNAMES;
        this.selectedCouncil = COUNCILNAMES[13];
    }

    getAuthorityData(): void{
        if(this.councilList.indexOf(this.selectedCouncil) > -1) {
          this.dataService.getAuthorityStatsData(this.selectedCouncil);
          this.dataService.getCouncilWordData(this.selectedCouncil);
          this.dataService.getAuthorityCategoryData(this.selectedCouncil);
          this.dataService.getAuthorityLowerThanAvgData(this.selectedCouncil);
          this.dataService.getCouncilPdfData(this.selectedCouncil);
		  this.dataService.getCategoryStats();
        }
    }
}
