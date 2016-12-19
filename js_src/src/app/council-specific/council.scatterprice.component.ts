/**
 * Created by ayoung on 17/12/16.
 */
/**
 * Created by ayoung on 01/12/16.
 */

import {Component} from '@angular/core';
import * as d3 from 'd3';
import {DataService} from "../data-services/data.service";

@Component({
  selector : 'price',
  template:  `
        <h2>Distribution Price To Hygine</h2>
        <div id="pricescatter" style="width: 900px; height: 500px;"></div>
       `
})

export class CouncilPriceScatterComponent{

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
    dataService.newAuthoritesDataAnnounced$.subscribe(
      newAuthoritiesData => this.update(newAuthoritiesData)
    );
  };

  private update(unCleanData: any):void{
    this.cleanData(unCleanData);
    if(this.data.length > 1) {
      this.setup();
      this.setUpScales();
      this.makeSvg();
      this.scaleData();
      this.addData();
      this.addAxis();
    }
  }

  private cleanData(unCleanData: any): void{
    let p: number[] = [];
    let h: number[] = [];
    for(let k in unCleanData){
      if("yelp" in unCleanData[k]) {
        if (unCleanData[k].yelp.price != null) {

          let adjustedp : number;
          if(p.indexOf(unCleanData[k].yelp.price)>0){
            adjustedp = unCleanData[k].yelp.price+0.05;
          }else{
            adjustedp = unCleanData[k].yelp.price;
          }
          p.push(adjustedp);

          let adjustedh : number;
          if(h.indexOf(unCleanData[k].hygiene.RatingValue)>0){
            adjustedh = unCleanData[k].hygiene.RatingValue+0.05;
          }else{
            adjustedh = unCleanData[k].hygiene.RatingValue+0.05;
          }
          h.push(adjustedh);




          this.data.push({
            "price": adjustedp,
            "hygiene": adjustedh
          })
        }
      }

    }
  }

  private setup(): void{
    this.margin = {top: 80, right: 15, bottom: 60, left: 50};
    this.width = 500 - this.margin.left - this.margin.right;
    this.height = 500 - this.margin.top - this.margin.bottom;
  }


  private setUpScales(): void{
    this.xScale = d3.scaleLinear().range([0, this.width]);
    this.yScale = d3.scaleLinear().range([this.height, 0]);
  }



  private makeSvg(): void{
    this.svg = d3.select("div#pricescatter svg").remove();
    this.svg = d3.select("#pricescatter").append("svg")
      .attr("width", this.width + this.margin.left + this.margin.right)
      .attr("height", this.height + this.margin.top + this.margin.bottom)
      .append("g")
      .attr("transform",
        "translate(" + this.margin.left + "," + this.margin.top + ")");
  }


  private scaleData():void{
    this.xScale.domain([0, d3.max(this.data, function(d) { return d.hygiene; })]);
    this.yScale.domain([0, d3.max(this.data, function(d) { return d.price; })]);
  }


  private addData():void{
    let xScale = this.xScale;
    let yScale = this.yScale;
    this.svg.selectAll("dot")
      .data(this.data)
      .enter().append("circle")
      .attr("r", 5)
      .attr("cx", function(d) {return xScale(d.hygiene);})
      .attr("cy", function(d) {return yScale(d.price);})
      .style("fill", "blue");
  }

  private addAxis():void{
    this.svg.append("g")
      .attr("transform", "translate(0," + this.height + ")")
      .call(d3.axisBottom(this.xScale));

    this.svg.append("g")
      .call(d3.axisLeft(this.yScale));

    //Y axis lable
    this.svg.append("text")
      .attr("transform", "rotate(-90)")
      .attr("y", 0 - this.margin.left)
      .attr("x",0 - (this.height / 2))
      .attr("dy", "1em")
      .style("text-anchor", "middle")
      .text("Price");

    this.svg.append("text")
      .attr("transform",
            "translate(" + (this.width/2) + " ," +
                           (this.height + this.margin.top + 20) + ")")
      .style("text-anchor", "middle")
      .text("Hygeine");



  }



}
