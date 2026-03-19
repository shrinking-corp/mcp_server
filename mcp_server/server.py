import sys
import logging

from typing import Annotated, Literal
from pydantic import Field

from mcp.server.fastmcp import FastMCP
import io

sys.path.insert(0, "/app")  # /app is a package at the container root

logging.basicConfig(stream=sys.stderr, level=logging.INFO)
logger = logging.getLogger(__name__)

from app.main import process_puml
#from shrinking_algorithms.app.main import process_puml

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
        logger.info(f"Receiving file and sending to shrinking algorithms...")
        if algorithm == "kruskals":
            result = process_puml(file=f, algorithm="kruskals", settings="{}")
        elif algorithm == "evol":
            result = process_puml(file=f, algorithm="evol", settings="{\"iterations\": 5}")
        else:
            raise TypeError(f"Unknown algorithm: {algorithm}")
        logger.info("Shrinking completed successfully")
        if result is None:
            logger.info("Shrinking completed but returned no output.")
            return "Shrinking completed but returned no output."
        logger.info(f"Result: {result}")
        return str(result)
    except Exception as e:
        logger.error(f"Error processing file: {e}")
        return f"Error processing diagram: {str(e)}"

if __name__ == "__main__":
    mcp.run(transport="stdio")
