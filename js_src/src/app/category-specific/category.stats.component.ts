/**
 * Created by UOzbulak on 03/01/16.
 */

import {Component, Input, OnChanges, SimpleChange} from '@angular/core';
import {DataService} from "../data-services/data.service";
import {GoogleChartComponent} from "../google-chart/google-chart";

declare var google:any;
declare var googleLoaded:any;

   @Component({
       selector : 'categorystats',
       template:  `<div id="categorystats" style="width: 1400px; height: 350px;"></div>`
   })

export class CategoryStats extends GoogleChartComponent{

    private options : any;
    private data : any;
    private chart : any;

    constructor(private dataService: DataService) {
            super();
            dataService.newCategoryDataAnnounced$.subscribe(
                newCategoryDataAnnounced => this.update(newCategoryDataAnnounced)
            );
    };

    public update(newCategoryDataAnnounced: any) {
		console.log(newCategoryDataAnnounced)
		
		let chartData=[];
		chartData.push(['Restaurant Type', 'Hygiene', 'Google', 'Yelp'])
		for (let i=0; i<newCategoryDataAnnounced.length; i++ ){
			let categoryData = []
			categoryData.push(newCategoryDataAnnounced[i].category)
			categoryData.push(newCategoryDataAnnounced[i].hygieneMean)
			categoryData.push(newCategoryDataAnnounced[i].googleMean)
			categoryData.push(newCategoryDataAnnounced[i].yelpMean)
			chartData.push(categoryData)
		}

		this.options = {
			width: 1400,
			height: 350,
			legendTextStyle: {color:'#FFFFFF'},
			colors: ['#1CBCA9', '#4285F4','#D9252E'],
			chartArea: {width: "80%", height: "80%"},
			legend: { position: 'top', alignment: 'center' },
			vAxis: {title: 'Average Rating', textStyle: { color: '#FFFFFF' }, gridlines: {color: "#FFFFFF"}, titleTextStyle: {color: '#FFFFFF'}},
			fill:'transparent',
			backgroundColor: "transparent",
			hAxis: {color: '#FFFFFF', textStyle: { color: '#FFFFFF' }, gridlines: {color: "#FFFFFF"}}
        };
		
		  setTimeout(() =>
			{
				if ("visualization" in google) {
				this.data = google.visualization.arrayToDataTable(chartData);
				this.chart = this.createColumn(document.getElementById('categorystats'));
				this.chart.draw(this.data, this.options);
				}
			}
			, 1000);
		
	}
}
