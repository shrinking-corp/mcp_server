import logging

from typing import Annotated, Literal
from pydantic import Field

from mcp.server.fastmcp import FastMCP
import io

from shrinking_algorithms import process_puml

mcp = FastMCP("shrinking-algorithm")

@mcp.tool()
def shrink_diagram(
        puml_string: Annotated[str, Field(
            description="The PlantUML diagram content as a string. "
                        "Paste the full .puml file contents here."
        )],
        algorithm: Annotated[Literal["kruskals", "evol"], Field(
            description="Algorithm to use for shrinking:\n"
                        "- 'kruskals': Graph-based reduction, fast and deterministic, best for large diagrams\n"
                        "- 'evol': Evolutionary optimization, slower but may yield better results, runs 5 iterations"
        )]
) -> str:
    """Shrinks a PlantUML diagram using the specified algorithm. Provide the raw PlantUML string content."""
    try:
        f = io.StringIO(puml_string)
        logging.info(f"Receiving file and sending to shrinking algorithms...")
        if algorithm == "kruskals":
            result = process_puml(file=f, algorithm="kruskals", settings="{}")
        elif algorithm == "evol":
            result = process_puml(file=f, algorithm="evol", settings="{\"iterations\": 5}")
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
