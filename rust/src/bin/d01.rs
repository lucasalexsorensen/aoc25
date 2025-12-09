use anyhow::Result;
use aoc25::day_input;

fn main() -> Result<()> {
    let input = day_input!("01");
    println!("part one: {}", part_one(input)?);
    println!("part two: {}", part_two(input)?);
    Ok(())
}

fn parse_input(input: &str) -> Result<Vec<i32>> {
    input
        .lines()
        .map(|line| {
            let (direction, steps) = line.split_at(1);
            let steps = steps.parse::<i32>()?;
            match direction {
                "L" => Ok(-steps),
                "R" => Ok(steps),
                _ => Err(anyhow::anyhow!("invalid direction: {}", direction)),
            }
        })
        .collect()
}

fn part_one(input: &str) -> Result<usize> {
    let mut result = 0;
    let mut pos = 50;
    let steps = parse_input(input)?;
    for step in steps {
        pos += step;
        result += (pos % 100 == 0) as usize;
    }
    Ok(result)
}

fn part_two(input: &str) -> Result<usize> {
    let steps = parse_input(input)?;
    let mut result = 0;
    let mut pos = 50;
    for step in steps {
        // if step is going backwards, we need to correct for this by "aligning" to the right edge of the circle
        let fixed_pos = if step >= 0 { pos } else { (100 - pos) % 100 };
        result += (fixed_pos + step.abs()) / 100;
        pos += step;
        pos = pos.rem_euclid(100); // rem_reuclid is equivalent to python's modulo
    }
    Ok(result as usize)
}
