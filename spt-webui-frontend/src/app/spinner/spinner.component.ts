import { Component, ChangeDetectionStrategy } from '@angular/core';
import { NgOptimizedImage } from "@angular/common";

@Component({
    selector: 'app-spinner',
    imports: [
        NgOptimizedImage
    ],
    templateUrl: './spinner.component.html',
    changeDetection: ChangeDetectionStrategy.Eager,
    styleUrl: './spinner.component.sass'
})
export class SpinnerComponent {

}
