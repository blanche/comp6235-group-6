/**
 * Created by ayoung on 21/11/16.
 */
import {Component, OnInit} from '@angular/core';
import {DataService} from "../data-services/data.service";


@Component({
    // moduleId: module.id,
    selector: 'overview',
    templateUrl:'./overview.component.html',
    styleUrls: ['./overview.component.css'],
})

export class OverviewComponent implements OnInit {

    public authRatingsData : any;


    constructor(private dataService: DataService) { 
        dataService.newAuthoritesDataAnnounced$.subscribe(
            newAuthoritiesData => this.authRatingsData=newAuthoritiesData
        );
    };

    ngOnInit(): void {

    }

    getAuthorityData(): void{
        this.dataService.getDataForAuthority("Southampton")
    }

}
