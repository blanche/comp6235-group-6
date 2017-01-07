/**
 * Created by ayoung on 21/11/16.
 */
import {Component, OnInit} from '@angular/core';
import {DataService} from "../data-services/data.service";
import {CATGORIESLIST} from "./categoryNames";

@Component({
    // moduleId: module.id,
    selector: 'category',
    templateUrl:'./category.component.html',
    styleUrls: ['./category.component.css'],
})

export class CategoryComponent implements OnInit {

    public selectedCategory : string;
    public categoriesList : Array<string>;




    constructor(private dataService: DataService) {

    };

    ngOnInit(): void {
        this.categoriesList = CATGORIESLIST;
        this.selectedCategory = CATGORIESLIST[0];
    }

    getCategorySpecific(): void{
        if(this.categoriesList.indexOf(this.selectedCategory) > 0) {

        }
    }

}
