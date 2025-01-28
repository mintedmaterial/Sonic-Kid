from typing import Any, List
from nest.core import Module
import logging
from .allora import AlloraModule
from .solana import SolanaModule
from .twitter import TwitterModule

logger = logging.getLogger(__name__)


# imports
IMPORTS: List[Any] = [SolanaModule, TwitterModule, AlloraModule]

# controllers
CONTROLLERS: List[Any] = []

# providers
PROVIDERS: List[Any] = []

# exports
EXPORTS: List[Any] = []


@Module(
    imports=IMPORTS,
    controllers=CONTROLLERS,
    providers=PROVIDERS,
    exports=EXPORTS,
)
class ConnectionsModule:
    pass
