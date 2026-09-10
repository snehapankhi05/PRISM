from langgraph.graph import END, StateGraph

from backend.app.services.orchestration.controls_node import controls_node
from backend.app.services.orchestration.knowledge import knowledge_node
from backend.app.services.orchestration.runtime import PRISMRuntime
from backend.app.services.orchestration.state import PRISMState
from backend.app.services.orchestration.generation import generation_node
from backend.app.services.orchestration.guardrails import guardrails_node

def prepare_node(state: PRISMState) -> PRISMState:
    return state


def build_prism_graph(runtime: PRISMRuntime):

    def knowledge(state: PRISMState) -> PRISMState:
        return knowledge_node(
            state,
            db=runtime.db,
            knowledge_service=runtime.knowledge_service,
        )

    def controls(state: PRISMState) -> PRISMState:
        return controls_node(
            state,
            control_resolver=runtime.control_resolver,
        )

    def generation(state: PRISMState) -> PRISMState:
        return generation_node(
            state,
            specialist_registry=runtime.specialist_registry,
            output_repository=runtime.output_repository,
            provenance_service=runtime.provenance_service,
            db=runtime.db,
        )
    def guardrails(state: PRISMState) -> PRISMState:
        return guardrails_node(
            state,
            basic_guardrail=runtime.basic_guardrail,
            factual_guardrail=runtime.factual_guardrail,
            llm_guardrail=runtime.llm_guardrail,
            revision_service=runtime.revision_service,
        )
    graph = StateGraph(PRISMState)

    graph.add_node("prepare", prepare_node)
    graph.add_node("knowledge", knowledge)
    graph.add_node("controls", controls)
    graph.add_node("generation", generation)
    graph.add_node("guardrails", guardrails)
    graph.set_entry_point("prepare")

    graph.add_edge("prepare", "knowledge")
    graph.add_edge("knowledge", "controls")
    graph.add_edge("controls", "generation")
    graph.add_edge("generation", "guardrails")
    graph.add_edge("guardrails", END)

    return graph.compile()