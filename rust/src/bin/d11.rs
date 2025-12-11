use std::collections::HashMap;

use aoc25::day_input;
use itertools::Itertools;

fn main() {
    let input = day_input!("11");
    let graph = parse_input(input);
    println!("part one: {}", part_one(&graph));
    println!("part two: {}", part_two(&graph));
}

type Node = &'static str;
type Graph = HashMap<Node, Vec<Node>>;
type Cache = HashMap<(Node, Node), usize>;

fn parse_input(input: &'static str) -> Graph {
    input
        .lines()
        .map(|line| {
            let mut parts = line.split(' ');
            let to = parts.next().unwrap().strip_suffix(':').unwrap();
            (to, parts.collect())
        })
        .chain(vec![("out", vec![])])
        .collect()
}

fn n_paths(graph: &Graph, node: &'static str, target: &'static str, cache: &mut Cache) -> usize {
    if cache.contains_key(&(node, target)) {
        return *cache.get(&(node, target)).unwrap();
    }

    let result = (node == target) as usize
        + graph[node]
            .iter()
            .map(|n| n_paths(graph, n, target, cache))
            .sum::<usize>();

    cache.insert((node, target), result);
    result
}

fn part_one(graph: &Graph) -> usize {
    n_paths(graph, "you", "out", &mut HashMap::new())
}

fn part_two(graph: &Graph) -> usize {
    let paths = [["svr", "fft", "dac", "out"], ["svr", "dac", "fft", "out"]];
    paths
        .iter()
        .map(|path| {
            path.iter()
                .tuple_windows()
                .map(|(a, b)| n_paths(graph, a, b, &mut HashMap::new()))
                .product::<usize>()
        })
        .sum()
}
