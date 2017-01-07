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
/**
 * Created by ayoung on 21/11/16.
 */
var core_1 = require('@angular/core');
var data_service_1 = require("../data-services/data.service");
var councilNames_Array_1 = require("./councilNames.Array");
var CouncilComponent = (function () {
    function CouncilComponent(dataService) {
        var _this = this;
        this.dataService = dataService;
        dataService.newAuthoritesDataAnnounced$.subscribe(function (newAuthoritiesData) { return _this.authRatingsData = newAuthoritiesData; });
    }
    ;
    CouncilComponent.prototype.ngOnInit = function () {
        this.councilList = councilNames_Array_1.COUNCILNAMES;
        this.selectedCouncil = councilNames_Array_1.COUNCILNAMES[14];
    };
    CouncilComponent.prototype.getAuthorityData = function () {
        this.dataService.getDataForAuthority(this.selectedCouncil);
    };
    CouncilComponent = __decorate([
        core_1.Component({
            // moduleId: module.id,
            selector: 'council',
            templateUrl: '/src/app/council-specific/category.component.html',
            styleUrls: ['src/app/council-specific/category.component.css'],
        }), 
        __metadata('design:paramtypes', [data_service_1.DataService])
    ], CouncilComponent);
    return CouncilComponent;
}());
exports.CouncilComponent = CouncilComponent;
//# sourceMappingURL=council.component.js.map
