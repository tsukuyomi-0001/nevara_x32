use eventsource_stream::Eventsource;
use futures_util::StreamExt;
use reqwest::{self, Client};
use owo_colors::OwoColorize;
use std::io::{self, Write};

mod schema;
mod components;

const API_URL: &str = "http://localhost:8000";

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>>{
    let client = Client::new();
    components::decorator::print_initial_logo();

    loop {
        let mut input = components::decorator::input("User: ")?;
        input = input.trim().to_string();
        if input.is_empty() { continue; }

        if input.starts_with("/") {
            let command = components::supportives::parse_slash_commands(&input);
            if command.name.eq_ignore_ascii_case("exit") { break; }
            if command.name.eq_ignore_ascii_case("list_files")  { components::endpoints::list_files(&client, API_URL).await? }
            if command.name.eq_ignore_ascii_case("remove_file") { components::endpoints::remove_files(&command.arguments, &client, API_URL).await? }
            if command.name.eq_ignore_ascii_case("upload_file") { components::endpoints::upload_files(command.arguments[0].clone(), &client, API_URL).await? }

            continue;
        }


        print!("{} ", "Nevara: ".bold().bright_blue());
        io::stdout().flush()?;

        let response = components::endpoints::invoke_agent(&input, &client, "invoke_v2", API_URL).await?;

        if !response.status().is_success() {
            eprintln!("\n{} {}\n", "HTTP error:".bold().bright_red(), response.status());
            continue;
        }

        let mut stream = response.bytes_stream().eventsource();

        while let Some(event_result) = stream.next().await {
            let event = match event_result {
                Ok(event) => event,
                Err(error) => {
                    eprintln!("\n{} {error}", "SSE error:".bold().bright_red());
                    break;
                }
            };

            let data: schema::AgentEvent = match serde_json::from_str(&event.data) {
                Ok(data) => data,
                Err(error) => {
                    eprintln!("\n{}: {}", "Invalid event JSON:".bold().bright_red(), error);
                    continue;
                }
            };

            if !data.tool.is_empty() { 
                println!("\n{} {} | {} {}", 
                    "[Tool Call]".bright_green(), 
                    data.tool.bold().white(), 
                    "Parameters:".bright_green(), 
                    data.parameter.bold().bright_black()
                ); 
            }

            if !data.chunk.is_empty() { print!("{}", data.chunk); io::stdout().flush()?; }

            if data.end { println!("\n{}\n", "[Agent Finished]".bold().bright_black()); break; }
        }
    }

    Ok(())
}
