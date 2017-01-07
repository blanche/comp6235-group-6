/**
 * Created by ayoung on 03/01/17.
 */

import {Component, Input, OnChanges, SimpleChange} from '@angular/core';
import {GoogleChartComponent} from "../../google-chart/google-chart";
import {DataService} from "../../data-services/data.service";

declare var google:any;
declare var googleLoaded:any;

   @Component({
      selector : 'topbottomcategories',
      templateUrl:'./category.topbottomfive.html',
      styleUrls: ['./category.topbottomfive.css']
   })


export class TopBottomFiveGraphComponent extends GoogleChartComponent{

    private options : any;
    private data : any;
    private chart : any;
    private dataServiceInstance:  DataService;
    @Input() topBottomCategory:string;

    constructor(private dataService: DataService) {
            super();
            this.dataServiceInstance = dataService;
            this.topBottomCategory = "hygiene";
            dataService.newCategoryBestStatsAnnounced$.subscribe(
                topBottomData => this.update(topBottomData)
            );
    };

    public topBottomRedraw(event):void{
        this.update(this.dataServiceInstance.getCurrentBestWorseCategory())
    }

    private update(topBottomData:any) : void{
      setTimeout(() =>{
          this.drawTopChart(topBottomData);
          this.drawBottomChart(topBottomData);
      },800)
    }

     private drawTopChart(datat:any){
       let topArray: Array<any> = [["Council", "Rating"]];
          if(datat.length != 0) {
              for (let i=0; i<5; i++) {
                topArray.push(
                  [datat[0][this.topBottomCategory]["top"][i][0],
                   datat[0][this.topBottomCategory]["top"][i][1][this.topBottomCategory]]
                );
              }
          }
          let topDataArray = google.visualization.arrayToDataTable(topArray);
          let options = {
              title: "Top and bottom rated councils",
              width: 400,
              height: 300,
              bar: {groupWidth: "95%"},
              legend: { position: "none" },
              hAxis: {
                viewWindow: {
                  min: 0,
                  max: 5
                },
                ticks: [0, 1, 2, 3, 4, 5]
              }
          };

          let topChart = this.createBarChart(document.getElementById('topCategories'));
          topChart.draw(topDataArray, options);
     }

     private drawBottomChart(datab:any){
       let topArray: Array<any> = [["Council", "Rating"]];
          if(datab.length != 0) {
              for (let i=0; i<5; i++) {
                topArray.push(
                  [datab[0][this.topBottomCategory]["bottom"][4-i][0],
                   datab[0][this.topBottomCategory]["bottom"][4-i][1][this.topBottomCategory]]
                );
              }
          }
          let topDataArray = google.visualization.arrayToDataTable(topArray);
          let options = {
              width: 400,
              height: 300,
              bar: {groupWidth: "95%"},
              legend: { position: "none" },
              hAxis: {
                viewWindow: {
                  min: 0,
                  max: 5
                },
                ticks: [0, 1, 2, 3, 4, 5]
              }
          };

          let topChart = this.createBarChart(document.getElementById('bottomCategories'));
          topChart.draw(topDataArray, options);
     }



}
