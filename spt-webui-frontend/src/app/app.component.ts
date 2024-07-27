import { Component, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { SptWebUiApiWrapperService } from "./api-services/spt-web-ui-api-wrapper.service";
import { JsonPipe } from "@angular/common";

@Component({
	selector: 'app-root',
	standalone: true,
	imports: [RouterOutlet, JsonPipe],
	templateUrl: './app.component.html',
	styleUrl: './app.component.scss'
})
export class AppComponent {

	loadedData = signal(null);

	constructor(private apiWrapper: SptWebUiApiWrapperService) {
		this.apiWrapper.getPlaybackState().subscribe({
			next: value => {
				this.loadedData.set(value);
			}
		});

	}
}
