use anyhow::{Result, anyhow};
use aoc25::day_input;

type Bank = Vec<u8>;

fn main() -> Result<()> {
    let input = day_input!("03");
    let banks = parse_input(input)?;
    println!("part one: {}", part_one(&banks)?);
    println!("part two: {}", part_two(&banks)?);
    Ok(())
}

fn parse_input(input: &str) -> Result<Vec<Bank>> {
    input
        .lines()
        .map(|line| {
            line.chars()
                .map(|c| Ok(c.to_digit(10).ok_or(anyhow!("invalid character"))? as u8))
                .collect::<Result<Bank>>()
        })
        .collect::<Result<Vec<Bank>>>()
}

fn part_one(banks: &[Bank]) -> Result<usize> {
    banks.iter().map(|bank| greedy(bank, 0, 2)).sum()
}

fn part_two(banks: &[Bank]) -> Result<usize> {
    banks.iter().map(|bank| greedy(bank, 0, 12)).sum()
}

fn greedy(bank: &Bank, start_idx: usize, n: usize) -> Result<usize> {
    if n == 0 {
        return Ok(0);
    }
    let stop_idx = bank.len() - n + 1;
    let seq = &bank[start_idx..stop_idx];
    let (mut max_idx, max_val) = seq
        .iter()
        .copied()
        .enumerate()
        .max_by_key(|(i, v)| (*v, std::cmp::Reverse(*i))) // prefer earlier index on tie
        .ok_or(anyhow!("no maximum value found"))?;
    max_idx += start_idx;
    let term = max_val as usize * 10usize.pow((n - 1) as u32);
    Ok(term + greedy(bank, max_idx + 1, n - 1)?)
}
