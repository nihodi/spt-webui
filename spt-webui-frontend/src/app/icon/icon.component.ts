import { Component, input } from '@angular/core';

@Component({
	selector: 'app-icon',
	standalone: true,
	imports: [],
	templateUrl: './icon.component.html',
	styleUrl: './icon.component.sass'
})
export class IconComponent {
	ariaLabel = input<string>("")
}
