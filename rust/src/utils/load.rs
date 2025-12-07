use anyhow::Result;

pub fn load_input(day: usize) -> Result<String> {
    let base_path = if cfg!(feature = "test") {
        "../test-data"
    } else {
        "../data"
    };
    let path = format!("{base_path}/d{day:02}.txt");
    let input = std::fs::read_to_string(&path)?;
    Ok(input)
}
