import { Component, input, ChangeDetectionStrategy } from '@angular/core';

@Component({
    selector: 'app-icon',
    imports: [],
    templateUrl: './icon.component.html',
    changeDetection: ChangeDetectionStrategy.Eager,
    styleUrl: './icon.component.sass'
})
export class IconComponent {
	ariaLabel = input<string>("")
}
