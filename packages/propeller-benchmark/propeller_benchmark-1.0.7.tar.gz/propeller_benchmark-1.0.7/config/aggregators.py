import types_custom.apiKeys as ak
import types_custom.dex as d
import os
import dotenv as de

de.load_dotenv()

SupportedAggregators = {
    '1Inch': 1,
    'propeller': 2,
    'enso': 3,
    'barterswap': 4,
    '0x': 5,
    'hashflow': 6,
    'odos': 7
}

dexes = {
    '1Inch': d.Dex(
        apiInput={
            'url': 'https://api.1inch.dev/swap/v5.2/1/swap/',
            'tokenInParameter': 'src',
            'tokenOutParameter': 'dst',
            'amountInParameter': 'amount',
            'requestMethod': 'GET',
            'slippage': {
                'parameter': 'slippage',
                'value': 0
            },
            'apiKey': {
                'place': ak.ApiKeyPlace.HEADER_AUTHORIZATION,
                'value': 'Bearer ' + 'kMdQbEaGJNk9lhAwsIjRhgEG1m3E29t7'#os.environ.get('ONEINCH_API_KEY', '') #(ak.validatedENV.ONEINCH_API_KEY or '')
            },
            'maxApiRequestsPerInstance': 100,
            'additionalBodyParameters': {
                'chain': 1,
                'includeGas': "True",
                'includeProtocols': "True",
                'disableEstimate': "True",
                'from': '0x1111111111111111111111111111111111111111'
            }
        },
        apiOutput={
            'amountOutParameter': 'toAmount',
            'gasCostParameter': 'tx/gas',
            'routesParameter': 'protocols/0',
            'callDataParameter': 'tx/data',
            'gasPriceParameter': 'tx/gasPrice'
        }
    ),
    'propeller': d.Dex(
        apiInput={
            'url': 'https://api.propellerheads.xyz/v2/solver/solve/',
            'tokenInParameter': '',
            'tokenOutParameter': '',
            'amountInParameter': '',
            'requestMethod': 'POST',
            'slippage': {
                'parameter': 'slippage',
                'value': 0
            },
            'jsonBody': """
                {
                    "orders": [
                        {
                            "sell_token": "__tokenIn__",
                            "buy_token": "__tokenOut__",
                            "sell_amount": "__amountIn__"
                        }
                    ]
                }""",
            'maxApiRequestsPerInstance': 100,
            'additionalBodyParameters': {
                'blockchain': 'ethereum',
                'return_routes': "True"
            }
        },
        apiOutput={
            'amountOutParameter': 'solutions/0/orders/0/buy_amount',
            'gasCostParameter': 'solutions/0/gas',
            'routesParameter': 'routes',
            'callDataParameter': 'solutions/0/call_data'
        }
    ),
    'enso':d.Dex(
        apiInput={
            'url': 'https://api.enso.finance/api/v1/shortcuts/route',
            'tokenInParameter': 'tokenIn',
            'tokenOutParameter': 'tokenOut',
            'amountInParameter': 'amountIn',
            'requestMethod': 'GET',
            'maxApiRequestsPerInstance': 100,
            'slippage': {
                'parameter': 'slippage',
                'value': 0
            },
            'additionalBodyParameters': {
                'fromAddress': '0x1111111111111111111111111111111111111111',
                'receiver': '0x1111111111111111111111111111111111111111',
                'spender': '0x1111111111111111111111111111111111111111',
                'routingStrategy': 'router',
                'priceImpact': 'true',
                'chainId': '1'
            }
        },
        apiOutput={
            'amountOutParameter': 'amountOut',
            'gasCostParameter': 'gas',
            'routesParameter': 'route',
            'callDataParameter': 'tx/data'
        }
    ), 
    'barterswap':d.Dex(
        apiInput={
            'url': "https://api.barterswap.xyz/swap",
            'tokenInParameter': "source",
            'tokenOutParameter': "target",
            'amountInParameter': "amount",
            'requestMethod': "POST",
            'maxApiRequestsPerInstance': 100,
            'additionalBodyParameters': {
                'typeFilter': "BalancerV2", #[
                #     "BalancerV2",
                #     "BancorV3",
                #     "CurveV1",
                #     "CurveV2",
                #     "DodoV1",
                #     "DodoV2",
                #     "DssPsm",
                #     "EthWethBridge",
                #     "Integral",
                #     "Kyber",
                #     "Maverick",
                #     "OSwap",
                #     "UniswapV2",
                #     "UniswapV3",
                #     "Wsteth",
                #     "CroDefi",
                #     "Shiba",
                #     "Sushi",
                #     "SushiV3",
                #     "PancakeV3",
                #     "SolidlyV3",
                # ],
                'recipient': "0x335d7d5df1bf7c81ca5ab77398a787128ed31264",
                'deadline': "0", 
            },
        },
        apiOutput={
            'amountOutParameter': "route/outputAmount",
            'gasCostParameter': "route/gasEstimation",
            'routesParameter': "route/route",
            # 'callDataParameter': "data",
        },
    ), 
    'zero_x':d.Dex(
        apiInput={
            'url': 'https://api.0x.org/swap/v1/quote',
            'tokenInParameter': 'sellToken',
            'tokenOutParameter': 'buyToken',
            'amountInParameter': 'sellAmount',
            'requestMethod': 'GET',
            'slippage': {
                'parameter': 'slippagePercentage',
                'value': 0
            },
            'apiKey': {
                'place': ak.ApiKeyPlace.ZERO_EX,
                'value': '184c6db8-bcef-49e4-b339-11ededf1a8f4'#os.environ.get('ZERO_EX_API_KEY', '') #ak.validatedENV.ZERO_EX_API_KEY or ''
            },
            'maxApiRequestsPerInstance': 100
            # '1Inch gasCost is not properly returned in solve API if wallet is not connected and has funds. TODO'
        },
        apiOutput={
            'amountOutParameter': 'buyAmount',
            'gasCostParameter': 'estimatedGas',
            'routesParameter': 'orders',
            'callDataParameter': 'data',
            'gasPriceParameter': 'gasPrice'
        }
    ),
    'hashflow':d.Dex(
        apiInput={
            'url': 'https://api.hashflow.com/taker/v3/rfq',
            'tokenInParameter': '',
            'tokenOutParameter': '',
            'amountInParameter': '',
            'requestMethod': 'POST',
            'apiKey': {
                'place': ak.ApiKeyPlace.HEADER_AUTHORIZATION,
                'value': 'acx1eWY3UoInQU9F7KDOtizCJVXYaqnN'#os.environ.get('HASHFLOW_API_KEY', '') #ak.validatedENV.HASHFLOW_API_KEY or ''
            },
            'maxApiRequestsPerInstance': 100,
            'jsonBody': """
            {
            "baseChain": {
                "chainType": "evm",
                "chainId": 1
            },
            "quoteChain": {
                "chainType": "evm",
                "chainId": 1
            },
            "rfqs": [
                {
                "trader": "0x1111111111111111111111111111111111111111",
                "effectiveTrader": "0x1111111111111111111111111111111111111111",
                "baseToken": "__tokenIn__",
                "baseTokenAmount": "__amountIn__",
                "quoteToken": "__tokenOut__"
                }
            ]
            }""",
            'additionalBodyParameters': {
                'source': "caddi",
                'calldata': True,
            },
        },
        apiOutput={
            'amountOutParameter': 'quotes/0/quoteData/quoteTokenAmount',
            'callDataParameter': 'quotes/0/calldata'
        }
    ), 
    'odos':d.Dex(
        apiInput={
            'url': 'https://api.odos.xyz/sor/quote/v2',
            'tokenInParameter': '',
            'tokenOutParameter': '',
            'amountInParameter': '',
            'requestMethod': 'POST',
            'maxApiRequestsPerInstance': 100,
            'slippage': {
                'parameter': 'slippageLimitPercent',
                'value': 1
            },
            'jsonBody': """
            {
            "inputTokens": [
                {
                    "amount": "__amountIn__",
                    "tokenAddress": "__tokenIn__"
                }
            ],
            "outputTokens": [
                {
                    "proportion": 1,
                    "tokenAddress": "__tokenOut__"
                }
            ]
            }""",
            'additionalBodyParameters': {
                'chainId': 1,
                'compact': "True",
                'disableRFQs': "False",
                'userAddr': "0x1111111111111111111111111111111111111111"
            }
        },
        apiOutput={
            'amountOutParameter': 'outAmounts/0',
            'gasCostParameter': 'gasEstimate'
        }
    )
}
