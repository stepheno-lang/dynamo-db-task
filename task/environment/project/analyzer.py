import json
import heapq


class DependencyAnalyzer:
    def __init__(self, graph_file, rules_file):
        with open(graph_file) as f:
            self.graph = json.load(f)

        with open(rules_file) as f:
            self.rules = json.load(f)

        self.nodes = {
            node["id"]: node
            for node in self.graph["nodes"]
        }

        self.adjacency = {}

        for edge in self.graph["edges"]:
            self.adjacency.setdefault(edge["from"], []).append(edge)

    def shortest_path(self):
        """
        BUGGY IMPLEMENTATION

        Computes the minimum-cost path while ignoring:
        - repository restrictions
        - minimum trust
        - optional dependency rules

        The participant must repair this logic.
        """
        start = self.graph["start"]
        target = self.graph["target"]

        pq = [(0, start, [start])]
        visited = {}

        while pq:
            cost, node, path = heapq.heappop(pq)

            if node == target:
                return cost, path

            if node in visited:
                continue

            visited[node] = True

            for edge in self.adjacency.get(node, []):
                heapq.heappush(
                    pq,
                    (
                        cost + edge["cost"],
                        edge["to"],
                        path + [edge["to"]],
                    ),
                )

        return None, []

    def run(self):
        cost, path = self.shortest_path()

        print("Selected path:")
        print(path)
        print("Cost:", cost)
        