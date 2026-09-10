from backend.app.services.orchestration.graph import build_prism_graph


def main():
    graph = build_prism_graph()

    initial_state = {
        "source_id": "test-source",
        "query": "How many customers were affected?",
        "requested_outputs": ["linkedin"],
    }

    result = graph.invoke(initial_state)

    print("LangGraph orchestration successful.")
    print(f"Source ID: {result['source_id']}")
    print(f"Query: {result['query']}")
    print(f"Requested outputs: {result['requested_outputs']}")


if __name__ == "__main__":
    main()