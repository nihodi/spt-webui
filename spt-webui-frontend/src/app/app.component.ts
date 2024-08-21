import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { HeaderComponent } from "./header/header.component";
import { NotificationListComponent } from "./notification-list/notification-list.component";


@Component({
	selector: 'app-root',
	standalone: true,
	imports: [RouterOutlet, HeaderComponent, NotificationListComponent],
	templateUrl: './app.component.html',
	styleUrl: './app.component.sass'
})
export class AppComponent {


}
