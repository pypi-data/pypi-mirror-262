import requests
from types_custom.tokens import Token
from types_custom.dex import Dex
import types_custom.apiRequests as ar
from config.aggregators import SupportedAggregators
from typing import List, Dict, Union
import src.tool_storage as ts
import src.api as api
import time
import asyncio
from aiohttp import ClientSession, ClientTimeout

async def request_quote(tool_storage: ts.ToolStorage, pairs: List[str], amounts: List[int], new_tokens: List[Union[str, str, int, List[int]]] = []):
    for new_token in new_tokens:
        tool_storage.selected_tokens[new_token[0]] = Token(name=new_token[0], address=new_token[1], decimals=new_token[2], amounts_in=new_token[3])    

    valid_pairs = []
    for pair in pairs:
        tokens = pair.split("-")
        token_objects = [tool_storage.selected_tokens[token_name] for token_name in tokens]
        valid_pairs.append(token_objects)

    for dex_name, dex_params in tool_storage.selected_dexes.items():
        if tool_storage.get_dex_property(dex_name, 'totalRequests') > dex_params.apiInput['maxApiRequestsPerInstance']:
            continue
        request_id = 0
        for pair, amount in zip(valid_pairs, amounts):
            amount_in = normalize_amount(amount, pair[0])
            request_body = ar.ApiRequestInputValues(tokenIn=pair[0], tokenOut=pair[1], amountIn=amount_in)
            req = api.construct_api_request(
                dex_params,
                dex_name,
                request_body
            )
            if req:
                await make_request_to_aggregator(
                    tool_storage,
                    amount,
                    pair[0].name,
                    pair[1].name,
                    req,
                    dex_name,
                    dex_params, 
                    request_id
                )       
            tool_storage.increase_total_requests(dex_name)
            request_id += 1
            await await_one_second()

async def do_benchmark(tool_storage: ts.ToolStorage, new_tokens: List[Union[str, str, int, List[int]]] = []):
    for new_token in new_tokens:
        tool_storage.selected_tokens[new_token[0]] = Token(name=new_token[0], address=new_token[1], decimals=new_token[2], amounts_in=new_token[3])
    
    tokens = tool_storage.selected_tokens

    all_token_pairs = get_all_token_pairs(list(tokens.values()))
    request_id = 0
    for pair in all_token_pairs:
        for amount in pair['firstToken'].amounts_in:
            amount_in = normalize_amount(amount, pair['firstToken'])

            requests_to_make = prepare_requests_for_pair_and_amount_for_each_aggregator(
                tool_storage,
                pair['firstToken'],
                pair['secondToken'],
                amount_in
            )

            await asyncio.gather(
                *(make_request_to_aggregator(
                    tool_storage,
                    amount_in,
                    pair['firstToken'].name,
                    pair['secondToken'].name,
                    request['axiosRequestConfig'],
                    request['dexName'],
                    request['dexParams'],
                    request_id
                ) for request in requests_to_make)
            )
            request_id += 1
            await await_one_second()


async def await_one_second():
    await asyncio.sleep(1)

async def make_request_to_aggregator(
    tool_storage: ts.ToolStorage,
    amount_in: str,
    current_token_in_name: str,
    current_token_out_name: str,
    request,
    dex_name: str,
    dex_params: Dex,
    request_id: int
):
    try:
        print(
            f"Making request {request_id} to {dex_name}, for pair {current_token_in_name}-{current_token_out_name} and amount {amount_in}..."
        )
        initial_time = int(time.time() * 1000)
        response = None
        async with ClientSession() as session:
            timeout = ClientTimeout(total=10)
            if 'GET' in request['method']:
                response = await session.get(request['url'], params=request['params'], headers=request['headers'], timeout=timeout)
            else:
                response = await session.post(
                    request['url'],
                    params=request['params'],
                    json=request['data'],
                    headers=request['headers'], 
                    timeout=timeout
                )
        json_response = await response.json()
        end_time = int(time.time() * 1000)
        if response.status != 200:
            raise Exception(f"Request failed with status code {response.status}. Response: {json_response}")
        if 'status' in json_response and json_response['status'] == 'Error':
            raise Exception(f"Request failed. Response: {json_response['details']['status']}")
        if 'status' in json_response and json_response['status'] == 'fail':
            raise Exception(f"Request failed. Response: {json_response['error']}")
        await save_aggregator_response(
            tool_storage,
            dex_name,
            dex_params,
            amount_in,
            json_response,
            initial_time,
            end_time,
            current_token_in_name,
            current_token_out_name,
            request_id
            )
    except Exception as error:
        print(
            f"Request FAILED to {dex_name} for pair {current_token_in_name}-{current_token_out_name} and amount {amount_in}. Error: {error}"
        )


def prepare_requests_for_pair_and_amount_for_each_aggregator(
    tool_storage: ts.ToolStorage,
    current_token_in: Token,
    current_token_out: Token,
    amount_in: str
):
    requests = []
    for dex_name, dex_params in tool_storage.selected_dexes.items():
        if tool_storage.get_dex_property(dex_name, 'totalRequests') > dex_params.apiInput['maxApiRequestsPerInstance']:
            continue
        
        request_body = ar.ApiRequestInputValues(tokenIn=current_token_in, tokenOut=current_token_out, amountIn=amount_in)
        req = api.construct_api_request(
            dex_params,
            dex_name,
            request_body
        )
        if req:
            requests.append({
                'dexName': dex_name,
                'dexParams': dex_params,
                'axiosRequestConfig': req
            })

        tool_storage.increase_total_requests(dex_name)
    return requests

async def save_aggregator_response(
    tool_storage: ts.ToolStorage,
    dex_name: str,
    dex_params: Dex,
    amount_in: str,
    response: Dict,
    initial_time: int,
    end_time: int,
    current_token_in_name: str,
    current_token_out_name: str,
    request_id: int
):  
    elapsed_time = end_time - initial_time
    tool_storage.increase_succeeded_requests(dex_name)
    dex_output = api.render_api_output(
        dex_params,
        amount_in,
        response,
        str(initial_time),
        str(end_time),
        str(elapsed_time) + 'ms',
        current_token_in_name,
        current_token_out_name,
        request_id
    )

    # Get callData for odos by performing a new API request
    if dex_name == 'odos' and response['pathId']:
        path_id = response['pathId']
        request = {
            'url': 'https://api.odos.xyz/sor/assemble',
            'method': 'POST',
            'data': {
                'userAddr': '0x1111111111111111111111111111111111111111',
                'pathId': path_id,
                'simulate': False
            }
        }
        data =  {
                'userAddr': '0x1111111111111111111111111111111111111111',
                'pathId': path_id,
                'simulate': False
                }
        try:
            odos_response = requests.post(request['url'], json=data)
            odos_response_json = odos_response.json()
            dex_output.callData = odos_response_json['transaction']['data']
        except Exception as err:
           print(f"Error getting callData for odos: {err}")

    tool_storage.save_dex_request_output(dex_name, f"{current_token_in_name}-{current_token_out_name}", dex_output)    

def normalize_amount(amount: int, current_token_in: Token) -> str:
    amount_str = str(amount)
    if '.' in amount_str:
        numbers_after_decimal = len(amount_str.split('.')[1])
        amount_without_decimals = amount_str.replace('.', '')
        
        return str(int(amount_without_decimals) * 10 ** (current_token_in.decimals - numbers_after_decimal))
    return str(amount * 10 ** current_token_in.decimals)


def get_all_token_pairs(arr: List[Token]):
    pairs = []

    for i in range(len(arr)):
        for j in range(len(arr)):
            if i == j:
                continue
            pairs.append({'firstToken': arr[i], 'secondToken': arr[j]})

    return pairs
