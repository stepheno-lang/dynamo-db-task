from analyzer import DependencyAnalyzer


def main():
    analyzer = DependencyAnalyzer(
        "/app/data/graph.json",
        "/app/data/rules.json",
    )

    analyzer.run()


if __name__ == "__main__":
    main()