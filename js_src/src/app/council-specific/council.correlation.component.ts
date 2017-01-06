/**
 * Created by UOzbulak on 03/01/16.
 */

import {Component, Input, OnChanges, SimpleChange} from '@angular/core';
import {DataService} from "../data-services/data.service";
import {GoogleChartComponent} from "../google-chart/google-chart";

declare var google:any;
declare var googleLoaded:any;

   @Component({
       selector : 'correlation',
       template:  `<div id="barChart" style="width: 400px; height: 300px;"></div>`
   })

export class CouncilCorrelationComponent extends GoogleChartComponent{

    private options : any;
    private data : any;
    private chart : any;

    constructor(private dataService: DataService) {
            super();
            dataService.newAuthoritesStatsDataAnnounced$.subscribe(
                newAuthoritiesStatsData => this.update(newAuthoritiesStatsData)
            );
    };	
	
    public update(newAuthoritiesStatsData: any) {

		let chartData  : any = [];
        chartData.push(['Element', 'Correlation Coefficient', { role: 'style' }, { role: 'annotation' } ]);
		
		let city = ""
		for (let i=0; i<newAuthoritiesStatsData.length; i++ ){
			city = newAuthoritiesStatsData[i].LocalAuthorityName
			chartData.push(['Google', newAuthoritiesStatsData[i].googleCorrelationHygene, '#4285F4', 'Google' ]);
			chartData.push(['Yelp', newAuthoritiesStatsData[i].justEatCorrelationHygene, '#D9252E', 'Yelp' ]);
			chartData.push(['JustEat', newAuthoritiesStatsData[i].yelpCorrelationHygene, '#FF9E16', 'JustEat' ]);
		}
		
        this.options = {
			hAxis: {title: 'Correlation Coefficient', minValue: -0.2, maxValue: 0.2},
			vAxis: { minValue: -0.3, maxValue: 0.3},
			legend: 'none',
			width: 400,
			height: 300,
			chartArea: {width: "95%", height: "80%"},
        };

          setTimeout(() =>
            {
				if ("visualization" in google) {
				this.data = google.visualization.arrayToDataTable(chartData);
				this.chart = this.createBarChart(document.getElementById('barChart'));
				this.chart.draw(this.data, this.options);
				}
			}
			, 1000);
	}
}
