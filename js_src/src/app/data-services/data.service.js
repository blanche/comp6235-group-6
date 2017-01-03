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
var http_1 = require('@angular/http');
var Observable_1 = require('rxjs/Observable');
var Rx_1 = require("rxjs/Rx");
var DataService = (function () {
    function DataService(http) {
        this.http = http;
        this.dataUrl = 'http://localhost:5000/api/v1/overall'; // URL to web API
        // Observable Data
        this.authoritesData = new Rx_1.BehaviorSubject(Array());
        // Observable Data
        this.newAuthoritesDataAnnounced$ = this.authoritesData.asObservable();
    }
    DataService.prototype.announceDataSourceAvailible = function (data) {
        this.authoritesData = data;
    };
    DataService.prototype.getDataForAuthority = function (authorityName) {
        var _this = this;
        var query = this.dataUrl + '?hygiene.LocalAuthorityName=' + authorityName;
        this._getData(query).subscribe((function (res) {
            var data = _this.extractData(res);
            _this.authoritesData.next(data);
        }).bind(this));
    };
    DataService.prototype._getDataForAuthority = function (query) {
        return this.http.get(query);
    };
    DataService.prototype.extractData = function (res) {
        console.log("HERE");
        var body = res.json();
        var properJsonBody = [];
        for (var item in body) {
            properJsonBody.push(JSON.parse(body[item]));
        }
        return properJsonBody;
    };
    DataService.prototype.handleError = function (error) {
        var errMsg;
        if (error instanceof http_1.Response) {
            var body = error.json() || '';
            var err = body.error || JSON.stringify(body);
            errMsg = error.status + " - " + (error.statusText || '') + " " + err;
        }
        else {
            errMsg = error.message ? error.message : error.toString();
        }
        console.error(errMsg);
        return Observable_1.Observable.throw(errMsg);
    };
    DataService = __decorate([
        core_1.Injectable(), 
        __metadata('design:paramtypes', [http_1.Http])
    ], DataService);
    return DataService;
}());
exports.DataService = DataService;
//# sourceMappingURL=data.service.js.map
