use poem::listener::TcpListener;
use poem::{EndpointExt, Route, Server};
use poem_openapi::{OpenApiService};
use serde::Deserialize;

mod api;


#[derive(Deserialize, Clone)]
pub(crate) struct SptWebuiSettings {
    discord_client_id: u64,
	discord_redirect_uri: String,
}


#[tokio::main]
async fn main() -> Result<(), std::io::Error> {
    let settings = std::fs::read_to_string("./settings.json").expect("Could not load settings file!");
    let settings: SptWebuiSettings = serde_json::from_str(&settings.as_str()).expect("Could not parse settings file!");

    let api_service =
        OpenApiService::new((api::auth::AuthApi), "Hello World", "1.0");


    let ui = api_service.swagger_ui();
    let app = Route::new().nest("/", api_service.data(settings)).nest("/docs", ui);

    Server::new(TcpListener::bind("localhost:8000"))
        .run(app)
        .await?;

    Ok(())
}
