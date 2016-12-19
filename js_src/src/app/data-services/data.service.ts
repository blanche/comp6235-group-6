
import {Injectable}     from '@angular/core';
import {Http, Response} from '@angular/http';
import {Observable}     from 'rxjs/Observable';
import {BehaviorSubject} from "rxjs/Rx";

@Injectable()
export class DataService {
    private dataUrl = 'http://localhost:5000/api/v1/overall';  // URL to web API
    
    constructor(private http:Http) {
    }

    // Observable Data
    private authoritesData = new BehaviorSubject(Array());
    

    // Observable Data
    public newAuthoritesDataAnnounced$ = this.authoritesData.asObservable();
  

    announceDataSourceAvailible(data: any) {
        this.authoritesData = data;
    }

     getDataForAuthority(authorityName:string): void {
        var query = this.dataUrl  + '?hygiene.LocalAuthorityName=' + authorityName;
        this._getDataForAuthority(query).subscribe(
            ((res : any) =>
         {
             let data = this.extractData(res);
             this.authoritesData.next(data)
         }).bind(this)

        );
    }


    private _getDataForAuthority(query:string): Observable<any> {
        return this.http.get(query)
    }

    private extractData(res:Response) {
        console.log("HERE");
        let body = res.json();
        let properJsonBody:Array<any> = [];
        for (let item in body) {
            properJsonBody.push(JSON.parse(body[item]));
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