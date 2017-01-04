/**
 * Created by ayoung on 01/12/16.
 */

import { Component, OnInit} from '@angular/core';
declare var google:any;
declare var googleLoaded:any;

@Component({
  selector: 'chart'
})
export class GoogleChartComponent implements OnInit {

  constructor(){
      console.log("Here is GoogleChartComponent")
  }

  getGoogle() {
      return google;
  }
  ngOnInit() {
    console.log('ngOnInit');
    if(!googleLoaded) {
        googleLoaded = true;
        google.charts.load('current', {'packages':['corechart']});
        google.charts.setOnLoadCallback(function(){console.log("LOADED GOOGLE")})
     }
  }

    drawGraph(){
        console.log("DrawGraph base class!!!! ");
    }


    createScatterPlot(element:any):any {
        console.log(google);
        if("visualization" in google) {
            return new google.visualization.ScatterChart(element);
        }
    }

    createLinePlot(element:any):any {
      if("visualization" in google) {
            return new google.visualization.LineChart(element);
        }
    }
	
	createColumn(element:any):any {
		if("visualization" in google) {
			setTimeout(() => {}, 3000);
			return new google.visualization.ColumnChart(element);
		}
    }
	
	createBarChart(element:any):any {
        if("visualization" in google) {
			setTimeout(() => {}, 3000);
            return new google.visualization.BarChart(element);
        }
    }
}
