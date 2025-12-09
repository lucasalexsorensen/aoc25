use anyhow::{Result, anyhow};
use aoc25::day_input;

fn main() -> Result<()> {
    let input = day_input!("02");
    let parsed = parse_input(input)?;

    println!("part one: {}", part_one(&parsed));
    println!("part two: {}", part_two(&parsed));
    Ok(())
}

type ParsedInput = Vec<(usize, usize)>;

fn parse_input(input: &str) -> Result<ParsedInput> {
    input
        .split(',')
        .map(|p| {
            let (start, end) = p.split_once('-').ok_or(anyhow!("invalid input"))?;
            Ok((start.parse()?, end.parse()?))
        })
        .collect()
}

fn part_one(input: &ParsedInput) -> usize {
    let sequences: Vec<_> = (2..=10)
        .skip(2)
        .flat_map(|seq_len| generate_repeated_patterns(seq_len, true))
        .collect();
    solve(sequences, input)
}

fn part_two(input: &ParsedInput) -> usize {
    let sequences: Vec<_> = (2..=10)
        .flat_map(|seq_len| generate_repeated_patterns(seq_len, false))
        .collect();
    solve(sequences, input)
}

fn solve(mut sequences: Vec<usize>, input: &ParsedInput) -> usize {
    sequences.sort_unstable();
    sequences.dedup();
    input
        .iter()
        .map(|(start, end)| {
            let smallest_idx = sequences.partition_point(|x| x < start);
            let biggest_idx = sequences.partition_point(|x| x <= end);
            sequences[smallest_idx..biggest_idx].iter().sum::<usize>()
        })
        .sum()
}

fn generate_repeated_patterns(seq_len: usize, force_twice: bool) -> impl Iterator<Item = usize> {
    let half = seq_len / 2;
    let start = if force_twice { half } else { 1 };

    (start..=half)
        .filter(move |&pattern_len| seq_len.is_multiple_of(pattern_len))
        .flat_map(move |pattern_len| geometric_series(seq_len, pattern_len))
}

fn geometric_series(seq_len: usize, pattern_len: usize) -> impl Iterator<Item = usize> {
    let factor = (10usize.pow(seq_len as u32) - 1) / (10usize.pow(pattern_len as u32) - 1);
    let start_n = 10usize.pow((pattern_len - 1) as u32);
    let stop_n = 10usize.pow(pattern_len as u32);
    (start_n..stop_n).map(move |n| n * factor)
}
