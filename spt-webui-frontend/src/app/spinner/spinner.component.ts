import { Component } from '@angular/core';
import { NgOptimizedImage } from "@angular/common";

@Component({
  selector: 'app-spinner',
  standalone: true,
	imports: [
		NgOptimizedImage
	],
  templateUrl: './spinner.component.html',
  styleUrl: './spinner.component.sass'
})
export class SpinnerComponent {

}
