"use strict";
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
var platform_browser_1 = require('@angular/platform-browser');
var app_component_1 = require('./app.component');
var data_service_1 = require('./data-services/data.service');
var overview_component_1 = require('./overview/overview.component');
var http_1 = require("@angular/http");
var overview_scatter_component_1 = require("./council-specific/overview.scatter.component");
var index_1 = require("ng2-auto-complete/dist/index");
var council_component_1 = require("./council-specific/council.component");
var ng_bootstrap_1 = require("@ng-bootstrap/ng-bootstrap");
var AppModule = (function () {
    function AppModule() {
    }
    AppModule = __decorate([
        core_1.NgModule({
            imports: [
                platform_browser_1.BrowserModule,
                http_1.HttpModule,
                index_1.Ng2AutoCompleteModule,
                ng_bootstrap_1.NgbModule
            ],
            declarations: [
                app_component_1.AppComponent,
                overview_component_1.OverviewComponent,
                overview_scatter_component_1.ScatterChartComponent,
                council_component_1.CouncilComponent,
            ],
            bootstrap: [app_component_1.AppComponent],
            providers: [data_service_1.DataService]
        }), 
        __metadata('design:paramtypes', [])
    ], AppModule);
    return AppModule;
}());
exports.AppModule = AppModule;
//# sourceMappingURL=app.module.js.map