"""MCP server for Google Analytics 4 (GA4)."""

import argparse
import asyncio
import logging
import os
from contextlib import asynccontextmanager
from typing import Any, Dict, List, Optional, Union

from dotenv import load_dotenv
from mcp.server.fastmcp import Context, FastMCP

from .ga4_client import GA4Client
from .tools import get_metadata, run_realtime_report, run_report

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("mcp-server-ga4")

# Load environment variables from .env file if it exists
load_dotenv()


@asynccontextmanager
async def lifespan(server: FastMCP):
    """
    Manage server lifecycle and resources.
    
    Args:
        server: The FastMCP server instance
    """
    # Initialize GA4 client
    property_id = os.environ.get("GA4_PROPERTY_ID")
    if property_id:
        logger.info(f"Using property ID from environment: {property_id}")
    else:
        logger.warning("No default property ID provided")
    
    ga4_client = GA4Client(default_property_id=property_id)
    
    try:
        # Verify authentication
        await ga4_client.verify_auth()
        logger.info("Google Analytics authentication successful")
        yield {"ga4_client": ga4_client}
    except Exception as e:
        logger.error(f"Error initializing GA4 client: {e}")
        # Still yield to allow operation with manual property IDs
        yield {"ga4_client": ga4_client}
    finally:
        # Clean up any resources
        await ga4_client.close()
        logger.info("GA4 client closed")


def create_server(property_id: Optional[str] = None) -> FastMCP:
    """
    Create and configure the MCP server.
    
    Args:
        property_id: Optional default GA4 property ID
    
    Returns:
        Configured FastMCP server
    """
    # Set property ID in environment if provided
    if property_id:
        os.environ["GA4_PROPERTY_ID"] = property_id
    
    # Create MCP server
    server = FastMCP(
        "GA4",
        dependencies=["google-analytics-data>=0.16.0", "mcp>=1.0.0"],
        lifespan=lifespan,
    )
    
    # Register tools
    server.tool()(run_report)
    server.tool()(run_realtime_report)
    server.tool()(get_metadata)
    
    return server


def main():
    """Main entry point for the MCP server."""
    parser = argparse.ArgumentParser(description="MCP server for Google Analytics 4")
    parser.add_argument(
        "--property-id",
        help="Default Google Analytics 4 property ID",
        default=os.environ.get("GA4_PROPERTY_ID"),
    )
    parser.add_argument(
        "--transport",
        help="Transport to use (stdio or sse)",
        choices=["stdio", "sse"],
        default="stdio",
    )
    parser.add_argument(
        "--port",
        help="Port for SSE transport",
        type=int,
        default=8000,
    )
    parser.add_argument(
        "--host",
        help="Host for SSE transport",
        default="localhost",
    )
    parser.add_argument(
        "--debug", 
        help="Enable debug logging", 
        action="store_true"
    )
    
    args = parser.parse_args()
    
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.setLevel(logging.DEBUG)
        logger.debug("Debug logging enabled")
    
    # Create server
    server = create_server(args.property_id)
    
    # Run with appropriate transport
    if args.transport == "stdio":
        logger.info("Starting server with stdio transport")
        server.run(transport="stdio")
    else:
        logger.info(f"Starting server with SSE transport on {args.host}:{args.port}")
        server.run(transport="sse", host=args.host, port=args.port)


if __name__ == "__main__":
    main()
