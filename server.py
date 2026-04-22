import logging

from typing import Annotated, Literal
from networkx import algorithms
from pydantic import Field

from fastmcp import FastMCP
import io

from shrinking_algorithms.main import process_puml
from shrinking_algorithms.algorithms.types import AlgorithmType

from configs.configs import EvolConfig, KruskalConfig

mcp = FastMCP("shrinking-algorithm")

# def process_puml(content: str, algorithm_type: AlgorithmType, settings: dict):
@mcp.tool(
    annotations={
        "readOnlyHint": True
    }
)
def shrink_diagram(
        puml_string: Annotated[str, Field(
            description="The PlantUML diagram content as a string. "
                        "Paste the full .puml file contents here."
        )],
        algorithm: Annotated[Literal["kruskals", "evol", "preprocess"], Field(
            description="Algorithm to use for shrinking:\n"
                        "- 'kruskals': Graph-based reduction, fast and deterministic, best for large diagrams\n"
                        "- 'evol': Evolutionary optimization, slower but may yield better results, runs 5 iterations\n"
                        "- 'preprocess': Do not run any shrinking algorithm, only apply preprocessing steps"
        )],
        preprocess_steps: Annotated[
            list[
                Literal[
                    "remove_empty_classes",
                    "remove_isolated_classes",
                    "remove_leaf_classes",
                    "remove_low_degree_classes",
                    "remove_random_classes",
                    "remove_getters_and_setters",
                    "remove_public_methods",
                    "remove_private_methods",
                    "remove_protected_methods",
                    "remove_package_methods",
                    "remove_random_methods",
                    "remove_public_attributes",
                    "remove_private_attributes",
                    "remove_protected_attributes",
                    "remove_package_attributes",
                    "remove_random_attributes",
                    "remove_random_edges",
                ]
            ],
            Field(
                default_factory=list,
                description=(
                    "Optional preprocessing steps to apply before shrinking. "
                    "Steps are executed in the order provided."
                )
            )
        ],
        algorithm_config: Annotated[EvolConfig | KruskalConfig | None, Field(
            description="Optional configuration for the specified algorithm:\n"
                        "- 'EvolConfig': pass when using 'evol' algorithm\n"
                        "- 'KruskalConfig': pass when using 'kruskals' algrithm\n"
                        "- 'None': No algorithm configuration needed"
        )] = None

) -> str:
    """Shrinks a PlantUML diagram using the specified algorithm. Provide the raw PlantUML string content."""

    try:
        f = io.StringIO(puml_string)

        logging.info(f"Receiving file and sending to shrinking algorithms...")
        if algorithm == "kruskals":
            if algorithm_config is not None and not isinstance(algorithm_config, KruskalConfig):
                raise TypeError(f"Invalid algorithm configuration for 'kruskals': {algorithm_config}")

            result = process_puml(content=puml_string, algorithm_type=AlgorithmType.KRUSKAL, settings={})
        elif algorithm == "evol":
            if algorithm_config is not None and not isinstance(algorithm_config, EvolConfig):
                raise TypeError(f"Invalid algorithm configuration: {algorithm_config}")

            result = process_puml(content=puml_string, algorithm_type=AlgorithmType.EVOLUTION, settings={})
        elif algorithm == "preprocess":
            if algorithm_config is not None:
                raise TypeError(f"Invalid algorithm configuration: {algorithm_config}")

            result = process_puml(content=puml_string, algorithm_type=AlgorithmType.PREPROCESS_ONLY, settings={})
        else:
            raise TypeError(f"Unknown algorithm: {algorithm}")

        logging.info("Shrinking completed successfully")
        if result is None:
            logging.info("Shrinking completed but returned no output.")
            return "Shrinking completed but returned no output."
        logging.info(f"Result: {result}")
        return str(result)
    except Exception as e:
        logging.error(f"Error processing file: {e}")
        return f"Error processing diagram: {str(e)}"

if __name__ == "__main__":
    mcp.run(transport="stdio")
