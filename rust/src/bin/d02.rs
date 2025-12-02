use anyhow::Result;

fn main() -> Result<()> {
    let input = if cfg!(feature = "test") {
        include_str!("../../../test-data/d02.txt")
    } else {
        include_str!("../../../data/d02.txt")
    };

    println!("part one: {}", part_one(input)?);
    println!("part two: {}", part_two(input)?);
    Ok(())
}

fn parse_input(input: &str) -> Result<Vec<(usize, usize)>> {
    input
        .split(',')
        .map(|s| {
            let (start, end) = s.split_once('-').ok_or(anyhow::anyhow!("invalid input"))?;
            Ok((start.parse()?, end.parse()?))
        })
        .collect()
}

fn solver(input: &str, pattern: regress::Regex) -> Result<usize> {
    let parsed = parse_input(input)?;

    let mut result = 0;
    for (start, end) in parsed {
        result += (start..(end + 1))
            .filter(|i| pattern.find(i.to_string().as_str()).is_some())
            .sum::<usize>();
    }

    Ok(result)
}

fn part_one(input: &str) -> Result<usize> {
    solver(input, regress::Regex::new(r"^([0-9]+)\1$")?)
}

fn part_two(input: &str) -> Result<usize> {
    solver(input, regress::Regex::new(r"^([0-9]+)\1{1,}$")?)
}
