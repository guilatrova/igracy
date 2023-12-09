from __future__ import annotations

import inspect

from gpokeapi.clients.api import PokeApi

if __name__ == "__main__":
    api_class = PokeApi

    inspect.signature(api_class.__)
