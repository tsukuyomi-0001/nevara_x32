use serde::Deserialize;

#[derive(Debug, Deserialize)]
pub struct AgentEvent {
    #[serde(default)]
    pub chunk: String,

    #[serde(default)]
    pub end: bool,

    #[serde(default)]
    pub tool: String,

    #[serde(default)]
    pub parameter: serde_json::Value
}