/**
 * Created by ayoung on 21/11/16.
 */
import {Component, OnInit} from '@angular/core';
import {DataService} from "../data-services/data.service";
import {COUNCILNAMES} from "./councilNames.Array";



@Component({
    // moduleId: module.id,
    selector: 'council',
    templateUrl:'/src/app/council-specific/council.component.html',
    styleUrls: ['src/app/council-specific/council.component.css'],
})

export class CouncilComponent implements OnInit {

    public authRatingsData : any;
    public selectedCouncil : string;
    public councilList : Array<string>;


    constructor(private dataService: DataService) { 
        dataService.newAuthoritesDataAnnounced$.subscribe(
            newAuthoritiesData => this.authRatingsData=newAuthoritiesData
        );
    };

    ngOnInit(): void {
        this.councilList = COUNCILNAMES;
        this.selectedCouncil = COUNCILNAMES[14];
    }

    getAuthorityData(): void{
        this.dataService.getDataForAuthority(this.selectedCouncil)
    }

}
