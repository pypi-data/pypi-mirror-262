from typing import Dict, Union
import types_custom.tokens as t 

#SupportedTokens = Union['WETH', 'USDT', 'AAVE', 'TUSD', 'DAI', 'WBTC']

pairs: Dict[str, t.Token] = {
    'WETH': t.Token(name='WETH', address='0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2', decimals=18, amounts_in=[5, 1]),
    'USDT': t.Token(name='USDT', address='0xdac17f958d2ee523a2206206994597c13d831ec7', decimals=6, amounts_in=[1000, 1]),
    'AAVE': t.Token(name='AAVE', address='0x7Fc66500c84A76Ad7e9c93437bFc5Ac33E2DDaE9', decimals=18, amounts_in=[10, 1]),
    'TUSD': t.Token(name='TUSD', address='0x0000000000085d4780B73119b644AE5ecd22b376', decimals=18, amounts_in=[1000, 1]),
    'DAI': t.Token(name='DAI', address='0x6B175474E89094C44Da98b954EedeAC495271d0F', decimals=18, amounts_in=[1000, 1]),
    'WBTC': t.Token(name='WBTC', address='0x2260fac5e5542a773aa44fbcfedf7c193bc2c599', decimals=8, amounts_in=[0.01, 1])
}
