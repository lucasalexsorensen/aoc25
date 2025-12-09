use anyhow::Result;
use aoc25::utils::load::load_input;

use std::collections::HashMap;

type ParsedInput = HashMap<(i32, i32), char>;

fn main() -> Result<()> {
    let input = load_input(4)?;
    let parsed = parse_input(&input);
    println!("part one: {}", part_one(&parsed)?);
    println!("part two: {}", part_two(&parsed)?);
    Ok(())
}

fn parse_input(input: &str) -> ParsedInput {
    input
        .lines()
        .enumerate()
        .flat_map(|(r, line)| {
            line.trim()
                .chars()
                .enumerate()
                .map(move |(c, char)| ((r as i32, c as i32), char))
        })
        .collect()
}

const DIRS: [(i32, i32); 8] = [
    (-1, -1),
    (-1, 0),
    (-1, 1),
    (0, -1),
    (0, 1),
    (1, -1),
    (1, 0),
    (1, 1),
];

fn part_one(grid: &ParsedInput) -> Result<usize> {
    let before = count(grid);
    let after = count(&remove_accessible(grid));
    Ok(after - before)
}

fn part_two(grid: &ParsedInput) -> Result<usize> {
    let mut result = 0;
    let mut grid = grid.clone();
    loop {
        let before = count(&grid);
        grid = remove_accessible(&grid);
        let after = count(&grid);
        if after == before {
            break;
        }
        result += after - before;
    }
    Ok(result)
}

fn count(grid: &ParsedInput) -> usize {
    grid.values().filter(|&v| *v == '.').count()
}

fn remove_accessible(grid: &ParsedInput) -> ParsedInput {
    let mut new_grid = grid.clone();
    let new_entries = grid
        .iter()
        .filter(|(_, char)| **char == '@')
        .filter(|(pos, _)| {
            let n_adjacent = DIRS
                .iter()
                .filter(|(dr, dc)| {
                    let new_pos = (pos.0 + dr, pos.1 + dc);
                    grid.get(&new_pos).unwrap_or(&'.') == &'@'
                })
                .count();
            n_adjacent < 4
        })
        .map(|(pos, _)| (*pos, '.'));
    new_grid.extend(new_entries);
    new_grid
}
