
import {Injectable}     from '@angular/core';
import {Http, Response} from '@angular/http';
import {Observable}     from 'rxjs/Observable';
import {BehaviorSubject} from "rxjs/Rx";

@Injectable()
export class DataService {
    private dataUrl = 'http://localhost:5000/api/v1/';  // URL to web API

    constructor(private http:Http) {
    }
	
	// Observable Data Category
	private categoryStatsData = new BehaviorSubject(Array());
	public newCategoryDataAnnounced$ = this.categoryStatsData.asObservable();
	
    // Observable Data AuthoritesData
    private authoritesData = new BehaviorSubject(Array());
    public newAuthoritesDataAnnounced$ = this.authoritesData.asObservable();

    //Observable Data CouncilStats
    private authoritesStatsData = new BehaviorSubject(Array());
    public newAuthoritesStatsDataAnnounced$ = this.authoritesStatsData.asObservable();

    //Observable Data CouncilWords
    private councilWordData = new BehaviorSubject(Array());
    public newCouncilWordDataAnnounced$ = this.councilWordData.asObservable();

    public getCurrentCouncilWordData(){
        return this.councilWordData.getValue();
    }

    //Observable PDF Council
    private councilPdfData= new BehaviorSubject(Array());
    public newCouncilPdfDataAnnounced$ = this.councilPdfData.asObservable();

	//Observable Data CouncilCategoryStats
    private authoritiesCategoryData = new BehaviorSubject(Array());
    public newAuthoritiesCategoryData$ = this.authoritiesCategoryData.asObservable();

	//Observable Data CouncilLowerThanAvgStats
    private authoritiesLowerThanAvgStats = new BehaviorSubject(Array());
    public newAuthoritiesLowerThanAvgStats$ = this.authoritiesLowerThanAvgStats.asObservable();

  	//Observable Data CategorySpecific Best And Worse Areas
    private categoryBestStats = new BehaviorSubject(Array());
    public newCategoryBestStatsAnnounced$ = this.categoryBestStats.asObservable();

    public getCurrentBestWorseCategory(){
        return this.categoryBestStats.getValue();
    }

	public getDataForAuthority(authorityName:string): void {
		var query = this.dataUrl  + 'overall?hygiene.LocalAuthorityName=' + authorityName;
		this._getData(query).subscribe(
			((res : any) =>
		 {
			 let data = this.extractData(res);
			 this.authoritesData.next(data)
		 }).bind(this)

		);
	}

	public getAuthorityStatsData(authorityName:string):void{
	 var query = this.dataUrl + "councilstats/" + authorityName;
	this._getData(query).subscribe(
			((res : any) =>
		 {
			 let data = this.extractData(res);
			 this.authoritesStatsData.next(data)
		 }).bind(this)
		);
	}

	public getCategoryStats():void{
	 var query = this.dataUrl + "categorystats/";
	this._getData(query).subscribe(
			((res : any) =>
		 {
			 let data = this.extractData(res);
			 this.categoryStatsData.next(data)
		 }).bind(this)
		);
	}
	
	public getCouncilPdfData(authorityName:string):void{
	 var query = this.dataUrl + "councilPdf/" + authorityName;
	 this._getData(query).subscribe(
			((res : any) =>
		 {
			 let data = this.extractData(res);
			 this.councilPdfData.next(data)
		 }).bind(this)
		);
	}


	public getCouncilWordData(authorityName:string): void {
	  var query = this.dataUrl  + 'councilwords/' + authorityName;
	  this._getData(query).subscribe(
		  ((res : any) =>
	   {
		   let data = this.extractData(res);
		   this.councilWordData.next(data)
	   }).bind(this)
	  );
	}

	public getAuthorityCategoryData(authorityName:string):void{
	 var query = this.dataUrl + "councilcategorystats/" + authorityName;
	this._getData(query).subscribe(
			((res : any) =>
		 {
			 let data = this.extractData(res);
			 this.authoritiesCategoryData.next(data)
		 }).bind(this)
		);
	}

	public getAuthorityLowerThanAvgData(authorityName:string):void{
	 var query = this.dataUrl + "councillowerthanavg/" + authorityName;
	  this._getData(query).subscribe(
			((res : any) =>
		 {
			 let data = this.extractData(res);
			 this.authoritiesLowerThanAvgStats.next(data)
		 }).bind(this)
		);
	}

  public getCategoryTopBottomFive(categoryName:string):void{
    var query = this.dataUrl + "categoriestopbottom/" + categoryName;
	  this._getData(query).subscribe(
			((res : any) =>
		 {
			 let data = this.extractData(res);
			 this.categoryBestStats.next(data)
		 }).bind(this)
		);
	}


    private _getData(query:string): Observable<any> {
        return this.http.get(query)
    }

    private extractData(res:Response) {
        let body = res.json();
        let properJsonBody:Array<any> = [];
        if(typeof(body)=="object"){
          for (let item in body) {
              properJsonBody.push(JSON.parse(body[item]));
          }
        }else{
           properJsonBody.push(JSON.parse(body));
        }
        return properJsonBody
    }

    private handleError(error:Response | any) {
        let errMsg:string;
        if (error instanceof Response) {
            const body = error.json() || '';
            const err = body.error || JSON.stringify(body);
            errMsg = `${error.status} - ${error.statusText || ''} ${err}`;
        } else {
            errMsg = error.message ? error.message : error.toString();
        }
        console.error(errMsg);
        return Observable.throw(errMsg);
    }
}
