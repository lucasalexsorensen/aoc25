use anyhow::{Result, anyhow};
use aoc25::utils::load::load_input;

fn main() -> Result<()> {
    let input = load_input(7)?;

    let (part_one, part_two) = solve(&input).ok_or(anyhow!("no solution"))?;
    println!("part one: {}", part_one);
    println!("part two: {}", part_two);

    Ok(())
}

fn solve(input: &str) -> Option<(u64, u64)> {
    let width = input.lines().next()?.len();
    let mut counts = vec![0u64; width];
    counts[width / 2] = 1;

    let mut p1_result = 0;

    for line in input.lines().skip(2).step_by(2) {
        let mut new_counts = counts.clone();

        for (i, (count, _)) in counts
            .iter()
            .zip(line.chars())
            .enumerate()
            .filter(|(_, (count, c))| **count != 0 && *c == '^')
        {
            p1_result += 1;
            new_counts[i] = 0;
            new_counts[i - 1] += count;
            new_counts[i + 1] += count;
        }

        counts = new_counts;
    }

    Some((p1_result, counts.iter().sum()))
}
