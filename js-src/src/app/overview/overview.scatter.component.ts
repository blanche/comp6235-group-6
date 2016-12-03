/**
 * Created by ayoung on 01/12/16.
 */

import {Component, Input, OnChanges, SimpleChange} from '@angular/core';
import {DataService} from "../data-services/data.service";
import {GoogleChartComponent} from "../google-chart/google-chart";

   @Component({
       selector : 'scatter',
       template:  `
        <h2> Scatter Chart</h2>
        <div id="chartscatter" style="width: 900px; height: 500px;"></div>
       `
   })


export class ScatterChartComponent extends GoogleChartComponent{

    private options : any;
    private data : any;
    private chart : any;

    constructor(private dataService: DataService) {
            super();
            dataService.newAuthoritesDataAnnounced$.subscribe(
                newAuthoritiesData => this.update(newAuthoritiesData)
            );
    };

    drawGraph(){
        console.log("Drawing Scatter Grath");
        this.data = [
          ['Hygine Rating', 'Google Rating'],
            [0, 70],
        ];
        
    };


    public chartData =  [
        ['Hygine Rating', 'Google Rating'],
        [0, 70],
    ];

    public update(newAuthoritiesData: any) {

        this.options = {
          title: 'Hygine vs Google Ratings',
          hAxis: {title: 'Hygine Rating', minValue: 0, maxValue: 5},
          vAxis: {title: 'Google Rating', minValue: 0, maxValue: 5},
          legend: 'none'
        };

        let chartData  : any = [];
        chartData.push(['Hygine Rating', 'Google Rating']);
        chartData.push([4, 4]);
        for (let i=0; i<newAuthoritiesData.length; i++ ){
            if("google" in newAuthoritiesData[i]){
                if(newAuthoritiesData[i].google.rating != "NONE") {
                        let hygieneReview = newAuthoritiesData[i].hygiene.RatingValue;
                        let googleReview = newAuthoritiesData[i].google.rating;
                        chartData.push([hygieneReview, googleReview])
                }
            }
        }
        if("visualization" in window.google) {
            this.data =  google.visualization.arrayToDataTable(chartData);
            this.chart = this.createScatterPlot(document.getElementById('chartscatter'));
            this.chart.draw(this.data, this.options);
        }
    }

}