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
		let city = "";
		chartData.push(['Restaurant Type', 'Below Avg Hygiene','Above Avg Hygiene' ]);
		let lowerThanAv : Array<any>= [];
		if(newAuthoritiesLowerThanAvgStats.length != 0) {
		  lowerThanAv = newAuthoritiesLowerThanAvgStats[0].lowerThanAvgList;
		}
		lowerThanAv.sort((n1,n2) => {
			if(n1.hygiene > n2.hygiene){
			  return -1;
			}else{
			  return 1;
			}
		  })

		for (let p=0; p<lowerThanAv.length; p++) {
			let categoryData = [];
			categoryData.push(lowerThanAv[p].category);
			categoryData.push(lowerThanAv[p].hygiene);
			categoryData.push(100 - lowerThanAv[p].hygiene);
			chartData.push(categoryData)
		}


		this.options = {
			width: 1300,
			height: 300,
			colors: ['#9e0707','#079e3e'],
			legend: { position: 'top', alignment: 'center' },
			vAxis: {title: 'Percentage', minValue: 0, maxValue: 100, format: '#\'%\''},
			chartArea:{right: '16%',height: "70%" },
			isStacked: true
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
