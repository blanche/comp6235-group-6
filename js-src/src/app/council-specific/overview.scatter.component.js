/**
 * Created by ayoung on 01/12/16.
 */
"use strict";
var __extends = (this && this.__extends) || function (d, b) {
    for (var p in b) if (b.hasOwnProperty(p)) d[p] = b[p];
    function __() { this.constructor = d; }
    d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
};
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
var core_1 = require('@angular/core');
var data_service_1 = require("../data-services/data.service");
var google_chart_1 = require("../google-chart/google-chart");
var ScatterChartComponent = (function (_super) {
    __extends(ScatterChartComponent, _super);
    function ScatterChartComponent(dataService) {
        var _this = this;
        _super.call(this);
        this.dataService = dataService;
        this.chartData = [
            ['Hygine Rating', 'Google Rating'],
            [0, 70],
        ];
        dataService.newAuthoritesDataAnnounced$.subscribe(function (newAuthoritiesData) { return _this.update(newAuthoritiesData); });
    }
    ;
    ScatterChartComponent.prototype.drawGraph = function () {
        console.log("Drawing Scatter Grath");
        this.data = [
            ['Hygine Rating', 'Google Rating'],
            [0, 70],
        ];
    };
    ;
    ScatterChartComponent.prototype.update = function (newAuthoritiesData) {
        this.options = {
            title: 'Hygine vs Google Ratings',
            hAxis: { title: 'Hygine Rating', minValue: 0, maxValue: 5 },
            vAxis: { title: 'Google Rating', minValue: 0, maxValue: 5 },
            legend: 'none'
        };
        var chartData = [];
        chartData.push(['Hygine Rating', 'Google Rating']);
        chartData.push([4, 4]);
        for (var i = 0; i < newAuthoritiesData.length; i++) {
            if ("google" in newAuthoritiesData[i]) {
                if (newAuthoritiesData[i].google.rating != "NONE") {
                    var hygieneReview = newAuthoritiesData[i].hygiene.RatingValue;
                    var googleReview = newAuthoritiesData[i].google.rating;
                    chartData.push([hygieneReview, googleReview]);
                }
            }
        }
        if ("visualization" in window.google) {
            this.data = google.visualization.arrayToDataTable(chartData);
            this.chart = this.createScatterPlot(document.getElementById('chartscatter'));
            this.chart.draw(this.data, this.options);
        }
    };
    ScatterChartComponent = __decorate([
        core_1.Component({
            selector: 'scatter',
            template: "\n        <h2>Distribution Gooogle To Hygine</h2>\n        <div id=\"chartscatter\" style=\"width: 900px; height: 500px;\"></div>\n       "
        }), 
        __metadata('design:paramtypes', [data_service_1.DataService])
    ], ScatterChartComponent);
    return ScatterChartComponent;
}(google_chart_1.GoogleChartComponent));
exports.ScatterChartComponent = ScatterChartComponent;
//# sourceMappingURL=overview.scatter.component.js.map