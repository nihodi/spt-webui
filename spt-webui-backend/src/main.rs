extern crate dotenv;

mod entities;

use crate::entities::prelude::*;
use dotenv::dotenv;
use rocket::{get, launch, State};
use rocket_okapi::{openapi, openapi_get_routes, swagger_ui::*};
use std::collections::HashMap;
use std::string::String;
use std::time::Duration;
use rocket::serde::json::Json;
use sea_orm::{ConnectOptions, Database, DatabaseConnection};
use crate::entities::users;

#[openapi(tag = "Users")]
#[get("/")]
async fn index(
    db: &State<DatabaseConnection>
) -> Json<users::Model> {
    let user = Users::find()
        .one(db as &DatabaseConnection)
        .await
        .unwrap()
        .unwrap();


    Json(user)
}

#[launch]
async fn launch() -> _ {
    dotenv().ok();

    let env: HashMap<String, String> = HashMap::from_iter(std::env::vars());

    let mut opts = ConnectOptions::new(env.get("DATABASE_URL").expect("DATABASE_URL not set").to_string());
    opts.connect_timeout(Duration::from_secs(5));

    let db = Database::connect(opts).await.expect("Could not connect to database.");

    rocket::build()
        .manage(db)
        .mount(
            "/",
            openapi_get_routes![
                index,
            ]
        )

        .mount(
            "/swagger-ui/",
            make_swagger_ui(&SwaggerUIConfig {
                url: "../openapi.json".to_owned(),
                ..Default::default()
            }),
        )
}
