/**
 * Created by UOzbulak on 03/01/16.
 */

import {Component, Input, OnChanges, SimpleChange} from '@angular/core';
import {DataService} from "../data-services/data.service";
import {GoogleChartComponent} from "../google-chart/google-chart";

declare var google:any;
declare var googleLoaded:any;

   @Component({
       selector : 'councilcategorystats',
       template:  `<div id="councilcategorystats" style="width: 690px; height: 300px;"></div>`
   })

export class CouncilCategoryStatsComponent extends GoogleChartComponent{

    private options : any;
    private data : any;
    private chart : any;

    constructor(private dataService: DataService) {
            super();
            dataService.newAuthoritiesCategoryData$.subscribe(
                newAuthoritiesCategoryData => this.update(newAuthoritiesCategoryData)
            );
    };	
	
    public update(newAuthoritiesCategoryData: any) {

		let chartData=[];
		let city = ""
		chartData.push(['Restaurant Type', 'Hygiene', 'Google', 'Yelp'])
		for (let i=0; i<newAuthoritiesCategoryData.length; i++ ){
			for (let p=0; p<newAuthoritiesCategoryData[i].categoryResults.length; p++ ){
				let categoryData = []
				categoryData.push(newAuthoritiesCategoryData[i].categoryResults[p].category)
				categoryData.push(newAuthoritiesCategoryData[i].categoryResults[p].hygieneMean)
				categoryData.push(newAuthoritiesCategoryData[i].categoryResults[p].googleMean)
				categoryData.push(newAuthoritiesCategoryData[i].categoryResults[p].yelpMean)
				chartData.push(categoryData)
			}
		}
        this.options = {
			width: 690,
			height: 300,
			colors: ['#1CBCA9', '#4285F4','#D9252E'],
			chartArea: {width: "80%", height: "80%"},
			legend: { position: 'top', alignment: 'center' },
			vAxis: {title: 'Rating'}
        };
          setTimeout(() =>
            {
				if ("visualization" in google) {
				this.data = google.visualization.arrayToDataTable(chartData);
				this.chart = this.createColumn(document.getElementById('councilcategorystats'));
				this.chart.draw(this.data, this.options);
				}
			}
			, 1000);
	}
}
