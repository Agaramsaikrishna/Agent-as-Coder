
"""
State Graph Definition Module

This module defines the execution workflow for the agent system using a state graph architecture. 
The workflow manages test planning and execution for an automated testing framework.

Modules used:
- langgraph.graph.StateGraph: Base class for state-based graph implementation
- src.nodes: Contains core workflow components (plan_generate, execute_test)
- state.AgentState: Custom state class defining workflow data structure

Workflow Overview:
1. START → plan_generate (Plan test strategy)
2. plan → execute_test (Run test execution)
3. test → Conditional (Based on decide_next)
   - If requires replanning → back to plan
   - If complete → FINISH

The graph forms a feedback loop for iterative test planning and execution.
"""

from langgraph.graph import StateGraph, START, END
from src.state import AgentState
from src.nodes import plan_generate, execute_test, decide_next

def build_graph():
    """
    Build and configure the state graph workflow.
    
    Returns:
        Compiled LangGraph graph ready for execution
    """
    graph = StateGraph(AgentState)
    
    # Register core workflow nodes
    graph.add_node("plan", plan_generate)    # Plans test strategy and test steps
    graph.add_node("test", execute_test)     # Executes test plan and collects results
    
    # Set workflow entry point at planning phase
    graph.set_entry_point("plan")
    
    # Define workflow structure
    graph.add_edge(START, "plan")          # Initial edge from START node
    graph.add_edge("plan", "test")         # Plan → Execute sequence
    graph.add_conditional_edges(
        "test", 
        decide_next,                      # Conditional routing logic
        {"plan": "plan", "end": END}       # Route to planning or end workflow
    )
    
    # Return compiled graph ready for execution
    return graph.compile()



