import { Injectable } from '@angular/core';
import { BehaviorSubject, map, Observable } from "rxjs";
import { UserData } from "../api-services/models";
import { HttpClient, HttpErrorResponse } from "@angular/common/http";
import { environment } from "../../environments/environment";

@Injectable({
	providedIn: 'root'
})
export class AuthService {

	private userDataSource: BehaviorSubject<UserData | null> = new BehaviorSubject<UserData | null>(null);
	private isLoadingSource: BehaviorSubject<boolean> = new BehaviorSubject<boolean>(false);

	currentUserData$ = this.userDataSource.asObservable();
	isLoggedIn$ = this.userDataSource.pipe(map((v) => v !== null));

	isLoading$ = this.isLoadingSource.asObservable();

	refreshLoginState(): void {
		if (this.isLoadingSource.getValue())
			return;

		this.isLoadingSource.next(true);

		this.httpClient.get<UserData>(`${environment.api_prefix}/users/me`).subscribe({
			next: userData => {
				this.isLoadingSource.next(false);

				this.userDataSource.next(userData);
			},
			error: (err: HttpErrorResponse) => {
				this.isLoadingSource.next(false);

				if (err.status === 401) {
					this.userDataSource.next(null);
					return;
				}

				console.error("something went wrong. (this should be shown to the user hopefully)")

			}
		});
	}

	logOut(): Observable<void> {
		return this.httpClient.post<void>(`${environment.api_prefix}/logout`, null)
			.pipe(
				map((v) => {
					this.refreshLoginState();
					return v;
				})
			);
	}

	constructor(
		private httpClient: HttpClient
	) {
		this.refreshLoginState();
	}
}
