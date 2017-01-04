/**
 * Created by ayoung on 03/01/17.
 */


import {Component, OnInit} from '@angular/core';
import * as d3 from 'd3';
import {DataService} from "../../data-services/data.service";

declare var cloundLib:any;
declare var cloundLibLoaded:any;


@Component({
  selector: 'wordcloud',
  template: `
        <div id="wordCloud"></div>
       `
})


export class WordCloudComponent implements OnInit {

  private data:Array<any>;
  private d3:any;
  private cloundLib:any;
  private cloundLibLoaded:any;
  private width:any;
  private height:any;

  //d3 components

  private svg:any;
  private wordType:string;


  constructor(private dataService:DataService) {
    this.wordType = "adjList";
    this.data = [];
    this.d3 = d3;
    if (cloundLibLoaded) {
      this.cloundLib = cloundLib;
    }
    dataService.newCouncilWordDataAnnounced$.subscribe(
      councilWordData => this.drawGraph(councilWordData)
    );
  };

  ngOnInit() {
    if (cloundLibLoaded) {
      this.cloundLib = cloundLib;
    }
  }


  public drawGraph(councilWordData:any):void {
    let wordList:Array<any> = new Array();

    if (councilWordData.length == 0) {
      wordList = [{"text":"Loading", "size":100}]
    } else {
        for (let idx in councilWordData[0][this.wordType]) {
          let wordObj = councilWordData[0][this.wordType][idx];
          let occurance : any = (Math.sqrt(wordObj[1]));
          if(occurance > 20){
            occurance = occurance/2;
          }
          occurance = occurance * 3;
          let wordText : any = wordObj[0];
          wordList.push({"size":occurance, "text":wordText})
      }
    }

    var d3 = this.d3;
    var fill = d3.scaleOrdinal(this.d3.schemeCategory10);
    var layout = this.cloundLib()
      .size([450, 350])
      .words(wordList)
      .padding(1)
      .rotate(function () {
        return ~~(Math.random() * 2) * 90;
      })
      .font("Impact")
      .fontSize(function (d) {
        return d.size;
      })
      .on("end", draw);

    layout.start();

    function draw(words) {
      console.log("draw");
      d3.select("wordCloud svg").remove();
      d3.select("wordCloud").append("svg")
        .attr("width", layout.size()[0])
        .attr("height", layout.size()[1])
        .append("g")
        .attr("transform", "translate(" + layout.size()[0] / 2 + "," + layout.size()[1] / 2 + ")")
        .selectAll("text")
        .data(words)
        .enter()
        .append("text")
        .style("font-size", function (d) {
          return d.size + "px";
        })
        .style("font-family", "Impact")
        .style("fill", function (d, i) {
          return fill(i);
        })
        .attr("text-anchor", "middle")
        .attr("transform", function (d) {
          return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
        })
        .text(function (d) {
          return d.text;
        });
    }
  }


}
