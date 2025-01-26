from typing import Any
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings
from src.config.types import Rpc, SolanaPrivateKey
from solana.rpc.async_api import AsyncClient
from solders.keypair import Keypair
from jupiter_python_sdk.jupiter import Jupiter
from pydantic_core import ErrorDetails
from pydantic import ValidationError


class SolanaSettings(BaseSettings):
    private_key: SolanaPrivateKey = Field(validation_alias="SOLANA_PRIVATE_KEY")

    def __init__(self, **data: Any) -> None:
        super().__init__(**data)


class SolanaConfig(BaseModel):
    rpc: Rpc
    solana_settings: SolanaSettings

    def __init__(self, **data: Any) -> None:
        # if the connection is not configured, return none
        try:
            data["solana_settings"] = SolanaSettings()
            super().__init__(**data)
        except Exception as e:
            if isinstance(e, ValidationError):
                errors: list[ErrorDetails] = e.errors()
                for error in errors:
                    print(
                        f'{error.get("msg")}. Invalid Field(s): {".".join(map(str, error.get("loc", [])))}'
                    )
            return

    def get_client(self) -> AsyncClient:
        conn = AsyncClient(self.rpc)
        return conn

    def get_wallet(self) -> Keypair:
        return self.solana_settings.private_key

    def get_jupiter(self) -> Jupiter:
        jupiter = Jupiter(
            async_client=self.get_client(),
            keypair=self.get_wallet(),
            quote_api_url="https://quote-api.jup.ag/v6/quote?",
            swap_api_url="https://quote-api.jup.ag/v6/swap",
            open_order_api_url="https://jup.ag/api/limit/v1/createOrder",
            cancel_orders_api_url="https://jup.ag/api/limit/v1/cancelOrders",
            query_open_orders_api_url="https://jup.ag/api/limit/v1/openOrders?wallet=",
            query_order_history_api_url="https://jup.ag/api/limit/v1/orderHistory",
            query_trade_history_api_url="https://jup.ag/api/limit/v1/tradeHistory",
        )
        return jupiter

    def format_txid_to_scanner_url(self, txid: str) -> str:
        return f"https://explorer.solana.com/tx/{txid}"

    def to_json(self) -> dict[str, Any]:
        # we need to manually serialize the keypair
        wallet = str(self.get_wallet().pubkey())
        return {
            "rpc": self.rpc,
            "solana_settings": {"public_key": wallet},
        }
