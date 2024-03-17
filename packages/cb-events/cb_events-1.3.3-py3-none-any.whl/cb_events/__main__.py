"""The main module for the event poller.

This module is the entry point for the event poller. It fetches events from the
Chaturbate API and logs them to the console.

Example:
    The module can be run as follows::

        $ python -m cb_events
"""

import asyncio
import os

from dotenv import load_dotenv

from cb_events.exceptions import BaseURLError
from cb_events.poller import CBAPIPoller

load_dotenv(override=True)


async def main() -> None:
    """Run the event poller."""
    url = os.environ.get("BASE_URL")
    if not url:
        error_msg = "Please set the BASE_URL environment variable with the correct URL."
        raise BaseURLError(error_msg)


    async with CBAPIPoller(url) as poller:
        await poller.fetch_events()


if __name__ == "__main__":
    asyncio.run(main())
