use anyhow::{Result, anyhow};
use aoc25::utils::load::load_input;

fn main() -> Result<()> {
    let input = load_input(5)?;
    let (ranges, ingredients) = parse_input(&input)?;
    println!("part one: {}", part_one(&ranges, &ingredients));
    println!("part two: {}", part_two(ranges)?);
    Ok(())
}

type Range = std::ops::Range<usize>;
fn parse_input(input: &str) -> Result<(Vec<Range>, Vec<usize>)> {
    let (ranges_part, ingredients_part) = input
        .split_once("\n\n")
        .ok_or(anyhow!("invalid chunk separator"))?;

    let ranges = ranges_part
        .lines()
        .map(|line| {
            let (a, b) = line.split_once('-').ok_or(anyhow!("invalid input"))?;
            Ok(a.parse()?..b.parse()?)
        })
        .collect::<Result<_>>()?;

    let ingredients = ingredients_part
        .lines()
        .map(|line| Ok(line.parse()?))
        .collect::<Result<_>>()?;

    Ok((ranges, ingredients))
}

fn part_one(ranges: &[Range], ingredients: &[usize]) -> usize {
    ingredients
        .iter()
        .filter(|&i| ranges.iter().any(|r| r.contains(i)))
        .count()
}

fn part_two(mut ranges: Vec<Range>) -> Result<usize> {
    ranges.sort_by_key(|r| r.start);

    let mut merged_ranges = vec![ranges[0].clone()];

    for r in ranges.iter().skip(1) {
        let last_range = merged_ranges.last().unwrap();
        if last_range.end >= r.start {
            *merged_ranges.last_mut().unwrap() = std::ops::Range {
                start: last_range.start,
                end: last_range.end.max(r.end),
            };
        } else {
            merged_ranges.push(r.clone());
        }
    }

    Ok(merged_ranges.iter().map(|r| r.end - r.start).sum())
}
