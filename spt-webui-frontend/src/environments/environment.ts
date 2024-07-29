export interface Environment {
	api_prefix: string;
	base_href?: string;
}

export const environment: Environment = {
	api_prefix: "http://localhost:8000",
}
