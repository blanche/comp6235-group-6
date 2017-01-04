/**
 * Created by ayoung on 03/01/17.
 */
/**
 * Created by ayoung on 01/12/16.
 */

import {Component, Input, OnChanges, SimpleChange} from '@angular/core';
import {GoogleChartComponent} from "../../google-chart/google-chart";
import {DataService} from "../../data-services/data.service";

declare var google:any;
declare var googleLoaded:any;

   @Component({
       selector : 'pdfcouncil',
       template:  `
        <h2>Distribution</h2>
        <div id="pdfcouncil" style="width: 900px; height: 500px;"></div>
       `
   })


export class PdfChartComponent extends GoogleChartComponent{

    private options : any;
    private data : any;
    private chart : any;

    constructor(private dataService: DataService) {
            super();
            dataService.newCouncilPdfDataAnnounced$.subscribe(
                newPfdData => this.update(newPfdData)
            );
    };


    private createData(pdfData:any){
      let dataPdf: Array<any> = [["Value", "Google", "Yelp", "Hygiene"]];

      let googleCount :number = 0;
      let yelpCount:number = 0;
      let hygieneCount:number = 0;

      for(let rating in pdfData[0].google){
        if(rating!=null){googleCount = pdfData[0].google[rating] + googleCount}
      }

      for(let rating in pdfData[0].yelp){
        if(rating!=null){yelpCount = pdfData[0].yelp[rating] + yelpCount}
      }

      for(let rating in pdfData[0].hygiene){
        if(rating!=null){hygieneCount = pdfData[0].hygiene[rating] + hygieneCount}
      }



      for(let i=1; i<=50; i++){
          let key = i/10;
          let googleData = pdfData[0].google[key];
          if(i%10 == 0){
              let yelpData = pdfData[0].yelp[key.toFixed(1)];
              let hygieneData = pdfData[0].hygiene[key];
              dataPdf.push([i/10, this.getWeightedValue(googleData,googleCount),
                this.getWeightedValue(yelpData, yelpCount), this.getWeightedValue(hygieneData, hygieneCount)])
          }else{
             dataPdf.push([i/10, this.getWeightedValue(googleData, googleCount), null, null])
          }
      }
      return dataPdf
    }

    private getWeightedValue(value:any, weight:any):any{
        if(value){
          return value/weight;
        }else{
           return null;
        }
   }

    public update(pdfData: any) {
        let chartData = [];
        if(pdfData.length!=0) {
            chartData = this.createData(pdfData);
        }else{return}
        this.options = {
            title: 'Distribution of ratings',
            curveType: 'function',
            interpolateNulls: true,
            legend: { position: 'bottom' },
            width: 400,
            height: 400,
            vAxes: {
              0: {title: 'Percentage'},
              1: {title: 'Rating'}
            },
        };

        setTimeout(() => {
           if ("visualization" in google) {
               this.data = google.visualization.arrayToDataTable(chartData);
               this.chart = this.createLinePlot(document.getElementById('pdfcouncil'));
               this.chart.draw(this.data, this.options);
           }}, 1000);
    }

}
