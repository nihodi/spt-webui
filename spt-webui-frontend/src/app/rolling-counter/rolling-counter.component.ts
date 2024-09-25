import { Component, effect, input } from '@angular/core';

@Component({
	selector: 'app-rolling-counter',
	standalone: true,
	imports: [],
	templateUrl: './rolling-counter.component.html',
	styleUrl: './rolling-counter.component.sass'
})
export class RollingCounterComponent {
	value = input.required<number>();

	time = input<number>(2_000);

	format = input<(value: number) => string>((value: number) => String(value));

	protected currentValue: number = 0;

	private interval: number | null = null;

	constructor() {
		effect(() => {
			this.currentValue = 0;
			let newValue = this.value();

			const timeStartedCounting = Date.now();

			if (this.interval !== null)
				clearInterval(this.interval);

			this.interval = setInterval(() => {
				this.currentValue = Math.floor(newValue * (1 - Math.pow(1 - ((Date.now() - timeStartedCounting) / this.time()), 3)));

				if (Date.now() - timeStartedCounting > this.time()) {
					clearInterval(this.interval!);
					this.currentValue = newValue;
				}
			}, 16);
		});
	}
}
