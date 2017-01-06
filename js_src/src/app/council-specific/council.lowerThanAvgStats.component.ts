/**
 * Created by UOzbulak on 03/01/16.
 */

import {Component, Input, OnChanges, SimpleChange} from '@angular/core';
import {DataService} from "../data-services/data.service";
import {GoogleChartComponent} from "../google-chart/google-chart";

declare var google:any;
declare var googleLoaded:any;

   @Component({
       selector : 'councillowerthanavg',
       template:  `<div id="councillowerthanavg" style="width: 1200px; height: 300px;"></div>`
   })

export class CouncilLowerThanAvgStats extends GoogleChartComponent{

    private options : any;
    private data : any;
    private chart : any;

    constructor(private dataService: DataService) {
            super();
            dataService.newAuthoritiesLowerThanAvgStats$.subscribe(
                newAuthoritiesLowerThanAvgStats => this.update(newAuthoritiesLowerThanAvgStats)
            );
    };	
	
    public update(newAuthoritiesLowerThanAvgStats: any) {

		let chartData=[];
		let city = ""
		chartData.push(['Restaurant Type', 'Hygiene', { role: 'style' } ])
		console.log(newAuthoritiesLowerThanAvgStats)
		
		for (let i=0; i<newAuthoritiesLowerThanAvgStats.length; i++ ){
			for (let p=0; p<newAuthoritiesLowerThanAvgStats[i].lowerThanAvgList.length; p++ ){
				let categoryData = []
				categoryData.push(newAuthoritiesLowerThanAvgStats[i].lowerThanAvgList[p].category)
				categoryData.push(newAuthoritiesLowerThanAvgStats[i].lowerThanAvgList[p].hygiene)
				categoryData.push(' \'stroke-color: #7a2f84; stroke-width: 2; \' ')
				chartData.push(categoryData)
			}
		}
		
        this.options = {
			width: 1300,
			height: 300,
			colors: ['#7a2f84'],
			legend: { position: 'none' },
			vAxis: {title: 'Percentage', minValue: 0, maxValue: 100, format: '#\'%\''},
			chartArea:{right: '16%',height: "70%" }
        };
          setTimeout(() =>
            {
				if ("visualization" in google) {
				this.data = google.visualization.arrayToDataTable(chartData);
				this.chart = this.createColumn(document.getElementById('councillowerthanavg'));
				this.chart.draw(this.data, this.options);
				}
			}
			, 1000);
	}
}
