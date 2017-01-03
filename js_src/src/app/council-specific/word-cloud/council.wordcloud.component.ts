/**
 * Created by ayoung on 03/01/17.
 */
/**
 * Created by ayoung on 17/12/16.
 */
/**
 * Created by ayoung on 01/12/16.
 */

import {Component} from '@angular/core';
import * as d3 from 'd3';
import {DataService} from "../../data-services/data.service";

@Component({
  selector : 'wordcloud',
  template:  `
        <div id="pricescatter" style="width: 900px; height: 500px;"></div>
       `
})

export class WordCloudComponent{

  private data: Array<any>;
  private d3 : any;
  private margin: any;
  private width :any;
  private height : any;

  //d3 components
  private xScale : any;
  private yScale : any;
  private svg :any;


  constructor(private dataService: DataService) {
    this.data = [];
    this.d3 = d3;
  };



}
