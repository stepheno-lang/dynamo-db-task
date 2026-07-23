import json
import heapq
from pathlib import Path

if Path("/app").exists():
    BASE = Path("/app")
else:
    BASE = Path(__file__).resolve().parents[1]

GRAPH_FILE = BASE / "environment/data/graph.json"
RULES_FILE = BASE / "environment/data/rules.json"
OUTPUT_DIR = BASE / "output"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def load():
    graph = json.loads(GRAPH_FILE.read_text())
    rules = json.loads(RULES_FILE.read_text())
    return graph, rules


def edge_is_valid(edge, nodes, rules):
    if edge["optional"] and not rules["allow_optional"]:
        return False

    target = nodes[edge["to"]]

    if target["repo"] not in rules["allowed_repositories"]:
        return False

    if target["trust"] < rules["minimum_trust"]:
        return False

    if edge["requires_repo"] != target["repo"]:
        return False

    if target["trust"] < edge["min_trust"]:
        return False

    return True


def shortest_path(graph, rules):
    nodes = {n["id"]: n for n in graph["nodes"]}

    adjacency = {}

    for edge in graph["edges"]:
        if edge_is_valid(edge, nodes, rules):
            adjacency.setdefault(edge["from"], []).append(edge)

    start = graph["start"]
    target = graph["target"]

    pq = [(0, start, [start])]
    visited = {}

    while pq:
        cost, node, path = heapq.heappop(pq)

        if node == target:
            return cost, path

        if node in visited and visited[node] <= cost:
            continue

        visited[node] = cost

        for edge in adjacency.get(node, []):
            heapq.heappush(
                pq,
                (
                    cost + edge["cost"],
                    edge["to"],
                    path + [edge["to"]],
                ),
            )

    return None, []


def main():
    graph, rules = load()

    nodes = {n["id"]: n for n in graph["nodes"]}

    total_cost, ids = shortest_path(graph, rules)

    path = [
        {
            "package": nodes[node]["package"],
            "version": nodes[node]["version"],
        }
        for node in ids
    ]

    summary = {
        "total_cost": total_cost,
        "path_length": len(path),
        "valid": total_cost is not None,
    }

    validation = {
        "constraints_satisfied": total_cost is not None,
        "minimum_cost": total_cost is not None,
    }

    (OUTPUT_DIR / "path.json").write_text(json.dumps(path, indent=2))
    (OUTPUT_DIR / "summary.json").write_text(json.dumps(summary, indent=2))
    (OUTPUT_DIR / "validation.json").write_text(json.dumps(validation, indent=2))


if __name__ == "__main__":
    main()