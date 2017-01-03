/**
 * Created by ayoung on 03/01/17.
 */


import {Component, OnInit} from '@angular/core';
import * as d3 from 'd3';
import {DataService} from "../../data-services/data.service";

declare var cloundLib:any;
declare var cloundLibLoaded:any;



@Component({
  selector : 'wordcloud',
  template:  `
        <div id="wordCloud" style="width: 500; height: 500px;"></div>
       `
})




export class WordCloudComponent implements OnInit{

  private data: Array<any>;
  private d3 : any;
  private cloundLib: any;
  private cloundLibLoaded: any;
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
    if(cloundLibLoaded) {
      this.cloundLib = cloundLib;
      this.drawGraph();
    }
  };

  ngOnInit(){
      if(cloundLibLoaded) {
        this.cloundLib = cloundLib;
        this.drawGraph();

      }
  }


  public drawGraph():void{
    var d3 = this.d3;
    var fill = d3.scaleOrdinal(this.d3.schemeCategory10);
    var layout = this.cloundLib()
        .size([500, 500])
        .words([
          "Hello", "world", "normally", "you", "want", "more", "words",
          "than", "this"].map(function(d) {
          return {text: d, size: 10 + Math.random() * 90, test: "haha"};
        }))
        .padding(5)
        .rotate(function() { return ~~(Math.random() * 2) * 90; })
        .font("Impact")
        .fontSize(function(d) { return d.size; })
        .on("end", draw);

    layout.start();

    function draw(words) {
      console.log("draw");
       d3.select("wordCloud").append("svg")
          .attr("width", layout.size()[0])
          .attr("height", layout.size()[1])
        .append("g")
          .attr("transform", "translate(" + layout.size()[0] / 2 + "," + layout.size()[1] / 2 + ")")
        .selectAll("text")
          .data(words)
        .enter()
          .append("text")
          .style("font-size", function(d) {
            return d.size + "px";
          })
          .style("font-family", "Impact")
          .style("fill", function(d, i) {
            return fill(i);
          })
          .attr("text-anchor", "middle")
          .attr("transform", function(d) {
            return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
          })
          .text(function(d) { return d.text; });
    }
  }



}
