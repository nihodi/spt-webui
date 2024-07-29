import { HttpInterceptorFn } from '@angular/common/http';

export const authInterceptor: HttpInterceptorFn = (req, next) => {

	const auth = req.clone({
		withCredentials: true
	});

	return next(auth);
};
