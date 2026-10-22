pub mod decorator {
    use std::io::{self, Write};
    use owo_colors::OwoColorize;

    pub fn print_initial_logo() {
        // println!("╭──────────────────────────────╮");
        // println!("│        AGENT CLIENT          │");
        // println!("│       Rust • Local API       │");
        // println!("╰──────────────────────────────╯");
        // let font = FIGfont::standard().unwrap();
        // let figure = font.convert("Nevara");
        // if let Some(ascii_art) = figure {
            // println!("{}", ascii_art.to_string().bright_cyan())
        // }

        let logo = include_str!("figlet.txt");
        println!("{}", logo.bright_black().bold());
        println!("Type '/exit' to quit.\n");
    }

    pub fn input<S>(placeholder: S) -> Result<String, Box<dyn core::error::Error>>
    where 
        S: Into<Option<&'static str>>
    {
        let mut input = String::new();
        if let Some(value) = placeholder.into() {
            print!("{}", value.bright_cyan().bold());
            io::stdout().flush()?;
        }
        io::stdin().read_line(&mut input)?;
        
        return Ok(input)
    }
}

pub mod supportives {
    use std::path::PathBuf;
    pub fn expand_path(input: &str) -> Result<PathBuf, Box<dyn std::error::Error>> {
        let input = input.trim();
        let expanded = if input == "~" {
            std::env::var_os("HOME")
                .map(PathBuf::from)
                .ok_or("HOME environment variable is not set")?    
        } else if let Some(rest) = input.strip_prefix("~/") {
            let home = std::env::var_os("HOME")
                .ok_or("HOME environment variable is not set")?;

            PathBuf::from(home).join(rest)
        } else {
            PathBuf::from(input)
        };

        Ok(std::fs::canonicalize(expanded)?)
    }

    #[derive(Debug)]
    pub struct SlashCommand {
        pub name: String,
        pub arguments: Vec<String>
    }

    pub fn parse_slash_commands(input_command: &str) -> SlashCommand {
        let processed_input = input_command.trim();
        let command_splits: Vec<String> = processed_input.split_whitespace().map(|s| s.to_string()).collect();
        let mut name = command_splits[0].clone().to_ascii_lowercase();
        name.replace_range(0..1, "");
        let arguments = if command_splits.len() > 1 { 
                command_splits[1..command_splits.len()].to_vec() 
            } else {
                Vec::new()
            };

        return SlashCommand { name: name, arguments: arguments }
    }
}

pub mod endpoints {
    use reqwest::{Client, Response, multipart};

    pub async fn invoke_agent(message: &String, client: &Client, endpoint: &str, api_url: &str) -> Result<Response, Box<dyn std::error::Error>> {
        let response = client
            .post(format!("{}/{endpoint}", api_url))
            .query(&[("message", message)])
            .header("Accept", "text/event-stream")
            .send()
            .await?;

        Ok(response)
    }

    pub async fn upload_files(input_path: String, client: &Client, api_url: &str) -> Result<(), Box<dyn std::error::Error>> {
        let path = crate::components::supportives::expand_path(&input_path)?;

        if !path.is_file() {
            return Err(format!("Not a regular file: {}", path.display()).into());
        }

        let filename = path
            .file_name()
            .ok_or("Could not determine filename")?
            .to_string_lossy()
            .into_owned();

        println!("Uploading: {}", path.display());

        // Stream the file instead of reading it entirely into memory.
        let part = multipart::Part::file(&path)
            .await?
            .file_name(filename);

        let form = multipart::Form::new().part("file", part);

        let response = client
            .post(format!("{}/upload", api_url))
            .multipart(form)
            .send()
            .await?;

        let status = response.status();
        let body = response.text().await?;

        if !status.is_success() {
            return Err(format!("Upload failed ({status}): {body}").into());
        }

        println!("Upload successful!");
        println!("{body}");

        Ok(())
    }

    pub async fn list_files(client: &Client, api_url: &str) -> Result<(), Box<dyn std::error::Error>> {
        let response = client
            .get(format!("{}/get_uploads", api_url))
            .send()
            .await?;

        let data = response.text().await?;
        println!("{}", data);
        Ok(())
    }

    pub async fn remove_files(file: &Vec<String>, client: &Client, api_url: &str) -> Result<(), Box<dyn std::error::Error>> {
        for i in file {
            let response = client
                .post(format!("{}/remove_upload", api_url))
                .query(&[("file", i)])
                .send()
                .await?;
            let message = response.text().await?;
            println!("{}\n", message);
        }
        Ok(())
    }
}