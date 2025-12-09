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
    let sequences = (2..=10)
        .skip(2)
        .flat_map(|seq_len| generate_repeated_patterns(seq_len, true));
    solve(sequences, input)
}

fn part_two(input: &ParsedInput) -> usize {
    let sequences = (2..=10).flat_map(|seq_len| generate_repeated_patterns(seq_len, false));
    solve(sequences, input)
}

fn solve(sequences: impl Iterator<Item = usize>, input: &ParsedInput) -> usize {
    let mut seq_v = sequences.collect::<Vec<_>>();
    seq_v.sort_unstable();
    seq_v.dedup();
    input
        .iter()
        .map(|(start, end)| {
            let smallest_idx = seq_v.partition_point(|x| x < start);
            let biggest_idx = seq_v.partition_point(|x| x <= end);
            seq_v[smallest_idx..biggest_idx].iter().sum::<usize>()
        })
        .sum()
}

fn generate_repeated_patterns(seq_len: usize, force_twice: bool) -> impl Iterator<Item = usize> {
    let half = seq_len / 2;
    let start = if force_twice { half } else { 1 };

    let pattern_lens =
        (start..=half).filter(move |&pattern_len| seq_len.is_multiple_of(pattern_len));

    pattern_lens.flat_map(move |pattern_len| geometric_series(seq_len, pattern_len))
}

fn geometric_series(seq_len: usize, pattern_len: usize) -> impl Iterator<Item = usize> {
    let factor = (10usize.pow(seq_len as u32) - 1) / (10usize.pow(pattern_len as u32) - 1);
    let start_n = 10usize.pow((pattern_len - 1) as u32);
    let stop_n = 10usize.pow(pattern_len as u32);
    (start_n..stop_n).map(move |n| n * factor)
}
