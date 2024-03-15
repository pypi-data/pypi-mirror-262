import json
import base64
from config.pairs import pairs
from config.aggregators import dexes
from typing import Dict, TypeVar, Union
from types_custom.dex import Dex, StoredDex
from types_custom.apiRequests import ApiRequestOutputValues, ApiRequestInputValues
from types_custom.tokens import Token
import requests
import src.api as api
T = TypeVar('T')

class ToolStorage:
    def __init__(self, selected_dexes: Dict[str, Dex], selected_tokens: Dict[str, Token]):
        self.stored_dexes_data: Dict[str, StoredDex] = {}
        self.selected_dexes = selected_dexes
        self.selected_tokens = selected_tokens

        for dex_name in selected_dexes.keys():
            self._create_stored_dex(dex_name)

    def _create_stored_dex(self, dex_name: str):
        self.stored_dexes_data[dex_name] = {
            'totalRequests': 0,
            'succeededRequests': 0,
            'failedRequests': 0,
            'swaps': {}
        }
    
    def get_dex_property(self, dex_name: str, property: str) -> Union[int, Dict, None]:
            stored_dex = self.stored_dexes_data.get(dex_name)
            if stored_dex:
                return stored_dex.get(property)
            return None

    def increase_succeeded_requests(self, dex_name: str):
        if dex_name in self.stored_dexes_data:
            self.stored_dexes_data[dex_name]['succeededRequests'] += 1

    def increase_total_requests(self, dex_name: str):
        if dex_name in self.stored_dexes_data:
            self.stored_dexes_data[dex_name]['totalRequests'] += 1

    def save_dex_request_output(self, dex_name: str, pair_key: str, data: ApiRequestOutputValues):
        stored_dex = self.stored_dexes_data.get(dex_name)
        if stored_dex:
            stored_dex_swaps = stored_dex['swaps']
            if pair_key not in stored_dex_swaps:
                stored_dex_swaps[pair_key] = []
            stored_dex_swaps[pair_key].append(data)

    async def generate_json(self) -> Dict[str, StoredDex]:
        self.update_failed_requests()
        output: Dict[str, StoredDex] = {}
        for dex_name in self.selected_dexes:
            output[dex_name] = self.stored_dexes_data[dex_name]
        
        return output
        
    async def convert_to_csv(self):
        json_data = await self.generate_json()

        csv_rows = []

        csv_headers = [
            'requestId',
            'DEX',
            'PAIR',
            'amountIn',
            'amountOut',
            'requestStartTimestamp',
            'requestReturnedTimestamp',
            'timestampElapsedBetweenRequestAndResponse',
            'gasCostTokenOut',
            'gasCostUSD',
            'callData',
            'hops',
            'rawRoutes'
        ]

        csv_rows.append(','.join(csv_headers))

        response = await self.get_eth_and_gas_price(json_data)
        eth_price = response['ethPrice']
        gas_price = response['gasPrice']
        eth_price_usd = float(eth_price) / 10 ** 6
        eth_price_usd = round(eth_price_usd, 2)

        for dex_name, dex_output in json_data.items():
            for pair_name, swaps in dex_output['swaps'].items():
                in_token_name, out_token_name = pair_name.split('-')
                in_token_decimals = self.selected_tokens[in_token_name].decimals
                out_token_decimals = self.selected_tokens[out_token_name].decimals

                for swap in swaps:
                    gas_cost_usd = 0
                    gas_cost_token_out = 0
                    if hasattr(swap, 'gasCost'):
                        if swap.gasCost != None:
                            gas_cost_formatted = float(swap.gasCost) / 10 ** 9
                            gas_price = float(gas_price)
                            gas_cost_usd = round((gas_cost_formatted * eth_price_usd * gas_price) / 10 ** 9, 2)
                            
                            token_out_price_usd = '0'
                            try:
                                if 'USD' in out_token_name:
                                    gas_cost_token_out = gas_cost_usd
                                else:
                                    token_out_price_usd = await self.retrieve_token_out_price_usd(out_token_name, json_data)
                                    gas_cost_token_out = str(float(gas_cost_usd) / float(token_out_price_usd))
                            except Exception as e:
                                print(f"Impossible to retrieve information about {out_token_name} price in USD")
                                print(e)

                    if hasattr(swap, 'callData'):
                        call_data = swap.callData
                    else:
                        call_data = 'N/A'
                    if hasattr(swap, 'routes'):
                        routes = swap.callData
                    else:
                        routes = 'N/A'

                    call_data_str = call_data if call_data is not None else ""
                    routes_str = base64.b64encode(json.dumps(routes).encode()).decode() if routes is not None else ""             
                    csv_rows.append(
                        ','.join([
                            str(swap.requestId),
                            dex_name,
                            pair_name,
                            str(float(swap.amountIn) / 10 ** in_token_decimals),
                            str(float(swap.amountOut) / 10 ** out_token_decimals),
                            str(swap.requestStartTimestamp),
                            str(swap.requestReturnedTimestamp),
                            str(swap.timestampElapsedBetweenRequestAndResponse),
                            str(gas_cost_token_out),
                            str(gas_cost_usd),
                            call_data_str,
                            str(swap.hopsLength),
                            routes_str
                        ])
                    )

        return '\r\n'.join(csv_rows)

    def update_failed_requests(self):
        for dex_name in self.selected_dexes.keys():
            self.stored_dexes_data[dex_name]['failedRequests'] = (
                self.stored_dexes_data[dex_name]['totalRequests'] - self.stored_dexes_data[dex_name]['succeededRequests']
            )


    def valid_gas_price(self, swap: ApiRequestOutputValues, pair_name: str):
        valid_gas_price = False
        gas_price = 0
        eth_price = 0
        #swap.get may not work 
        if pair_name == 'WETH-USDT' and swap.amountIn == '1000000000000000000' and hasattr(swap, 'gasPrice') and swap.gasPrice != '0':
            gas_price = float(swap.gasPrice)
            eth_price = float(swap.amountOut)
            valid_gas_price = True

        return {'validGasPrice': valid_gas_price, 'gasPrice': gas_price, 'ethPrice': eth_price}

    async def get_eth_and_gas_price(self, json_data: Dict[str, StoredDex]) -> dict:
        for dex_name, dex_output in json_data.items():
            for pair_name, swaps in dex_output['swaps'].items():
                for swap in swaps:
                    response = self.valid_gas_price(swap, pair_name)
                    if response['validGasPrice']:
                        return {'gasPrice': response['gasPrice'], 'ethPrice': response['ethPrice']}

        swap = await self.get_gas_and_eth_price_from_1inch()
        return {'gasPrice': swap['tx']['gasPrice'], 'ethPrice': swap['toAmount']}

    async def retrieve_token_out_price_usd(self, out_token_name: str, json_data: Dict[str, StoredDex]) -> str:
        token_out_price_usd = '0'
        for dex_name, dex_output in json_data.items():
            for pair_name, swaps in dex_output['swaps'].items():
                for swap in swaps:
                    if pair_name == f"{out_token_name}-USDT":
                        token_out_price_usd = str(float(swap.amountOut) / 10 ** 6)
                        return token_out_price_usd
        
        swap_1inch = await self.get_gas_and_eth_price_from_1inch(out_token_name)
        return str(float(swap_1inch['toAmount']) / 10 ** 6)


    async def get_gas_and_eth_price_from_1inch(self, token_in: str = 'WETH'):
        request_body = ApiRequestInputValues(tokenIn=pairs[token_in], tokenOut=pairs['USDT'], amountIn='1000000000000000000')
        
        req = api.construct_api_request(
            dexes['1Inch'],
            '1Inch',
            request_body
        )
        if req:
            response = requests.get(req['url'], params=req['params'], headers=req['headers'])
            if response.status_code == 200:
                return response.json()

