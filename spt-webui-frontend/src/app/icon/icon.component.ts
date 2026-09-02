import { Component, input } from '@angular/core';

@Component({
    selector: 'app-icon',
    imports: [],
    templateUrl: './icon.component.html',
    styleUrl: './icon.component.sass'
})
export class IconComponent {
	ariaLabel = input<string>("")
}
