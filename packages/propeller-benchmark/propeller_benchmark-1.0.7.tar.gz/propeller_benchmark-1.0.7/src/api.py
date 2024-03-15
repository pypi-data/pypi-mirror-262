from utils.array_builder import build_array_from_string
from config.aggregators import dexes
from types_custom.tokens import Token
from config.slippage import convert_slippage, slippage_multipliers
from datetime import datetime as Date
from datetime import timedelta
import time
import json
import types_custom.dex as d
import types_custom.apiKeys as ak
import types_custom.apiRequests as ar

def construct_api_request(dex: d.Dex, dex_name: str, request_body: ar.ApiRequestInputValues, swaps_1Inch: dict = None):

    request = {
        'headers': {},
        'params': {},
        'method': dex.apiInput['requestMethod'],
        'url': dex.apiInput['url']
    }

    api_key = dex.apiInput.get('apiKey')
    if api_key:
        api_key_place = dex.apiInput['apiKey']['place']
        api_key_value = dex.apiInput['apiKey']['value']
        if api_key_place == ak.ApiKeyPlace.HEADER_AUTHORIZATION:
            request['headers']['Authorization'] = api_key_value
        elif api_key_place == ak.ApiKeyPlace.ZERO_EX:
            request['headers']['0x-api-key'] = api_key_value

    secondary_objects = {}

    for p in ['tokenInParameter', 'tokenOutParameter', 'amountInParameter']:
        key = p
        out_value = key.replace('Parameter', '')

        if not dex.apiInput[key]:
            continue

        final_value = None
        
        token = getattr(request_body, out_value)
        if p == 'tokenInParameter' or p == 'tokenOutParameter':
            final_value = token.address if isinstance(token, Token) else None
        else:
            final_value = token

        if '/' in dex.apiInput[key]:
            out_parameter = dex.apiInput[key].split('/')

            if out_parameter[0] not in secondary_objects:
                secondary_objects[out_parameter[0]] = [] if out_parameter[0].isdigit() else {}

            current_object = build_array_from_string(dex.apiInput[key], secondary_objects[out_parameter[0]], final_value)

            secondary_objects[out_parameter[0]] = current_object.copy()

            request['params'].update(current_object)
        else:
            if dex.apiInput[key]:
                request['params'][dex.apiInput[key]] = final_value


    slippage = dex.apiInput.get('slippage')
    if slippage:
        if '/' in dex.apiInput['slippage']['parameter']:
            out_parameter = dex.apiInput['slippage']['parameter'].split('/')
            if out_parameter[0] not in secondary_objects:
                secondary_objects[out_parameter[0]] = [] if out_parameter[0] else {}
            current_object = build_array_from_string(dex.apiInput['slippage']['parameter'], secondary_objects[out_parameter[0]], dex.apiInput['slippage']['value'])
            secondary_objects[out_parameter[0]] = current_object.copy()
            request['params'].update(current_object)
        else:
            valid_slippage = convert_slippage(dex.apiInput['slippage']['value'], dex_name)
            request['params'][dex.apiInput['slippage']['parameter']] = valid_slippage

    json_body = dex.apiInput.get('jsonBody')
    if json_body:
        body = dex.apiInput['jsonBody'].replace('__tokenIn__', str(request_body.tokenIn.address)).replace('__tokenOut__', str(request_body.tokenOut.address)).replace('__amountIn__', str(request_body.amountIn))
        request['params'].update(json.loads(body))

    additional_body_parameters = dex.apiInput.get('additionalBodyParameters')
    if additional_body_parameters:
        for additional_parameter_name, additional_parameter_value in dex.apiInput['additionalBodyParameters'].items():
            timestamp = int(time.time())
            timestamp_plus_two_hours = timestamp + (2 * 60 * 60)
            request['params'][additional_parameter_name] = str(timestamp_plus_two_hours) if additional_parameter_name == 'deadline' else additional_parameter_value

    if request['method'] == 'POST':
        request['data'] = request['params'].copy()
        request['params'].clear()

    if dex_name == 'propeller':
        request['params'].update(dex.apiInput['additionalBodyParameters'])

    if dex.apiInput['url'] == dexes['barterswap'].apiInput['url']:
        try:
            if not swaps_1Inch:
                fake_value = 1 / 10 ** 2
                request['data']['targetTokenMinReturn'] = fake_value # / 10 ** request_body.tokenOut.decimals)
                return request
            
            pair_swaps_1inch = swaps_1Inch #None #ts.get_dex_property('1Inch', 'swaps')[f"{request_body.tokenIn.name}-{request_body.tokenOut.name}"]
            amountOut_min = None

            for swap in pair_swaps_1inch:
                if not swap:
                    continue
                amountOut_reference = float((swap['amountOut']).toString())
                amountIn = float((swap['amountIn']).toString())
                price_reference = amountIn / amountOut_reference
                amountOut_min = (float((request_body.amountIn).toString()) / price_reference) * 0.6
                break
            if not amountOut_min:
                return None
            request['params']['targetTokenMinReturn'] = (amountOut_min * 10 ** request_body.token_out.decimals).toString()
        except Exception as e:
            return None

    return request
def render_api_output(dex: d.Dex, amountIn: str, response_body, 
                      initial_time: str, end_time: str, elapsed_time: str, 
                      token_in_name: str, token_out_name: str, requestId: int) -> ar.ApiRequestOutputValues:
    api_output = dex.apiOutput
    response = ar.ApiRequestOutputValues(
        amountIn=amountIn,
        amountOut=0,
        hopsLength=0,
        requestStartTimestamp=initial_time,
        requestReturnedTimestamp=end_time,
        timestampElapsedBetweenRequestAndResponse=elapsed_time,
        gasPrice='0',
        requestId=f"{token_in_name}-{token_out_name}-{amountIn}-{requestId}"
    )
    is_param_present = api_output.get('gasPriceParameter')
    if is_param_present:
        if '/' in api_output['gasPriceParameter']:
            out_parameter = api_output['gasPriceParameter'].split('/')
            current_place = response_body
            for param in out_parameter:
                if param.isdigit():
                    index = int(param)
                    current_place = current_place[index]
                    
                else:
                    for key, value in current_place.items():
                        if key == param:
                            current_place = value
                            break
            response.gasPrice = str(int(current_place))
        else:
            response.gasPrice = str(int(response_body[api_output['gasPriceParameter']]))

    if '/' in api_output['amountOutParameter']:
        out_parameter = api_output['amountOutParameter'].split('/')
        current_place = response_body
        for param in out_parameter:
            if param.isdigit():
                    index = int(param)
                    current_place = current_place[index]
                    
            else:
                for key, value in current_place.items():
                    if key == param:
                        current_place = value
                        break
        response.amountOut = current_place
    else:
        response.amountOut = response_body[api_output['amountOutParameter']]

    
    is_param_present = api_output.get('gasCostParameter')
    if is_param_present:
        if '/' in api_output['gasCostParameter']:
            out_parameter = api_output['gasCostParameter'].split('/')
            current_place = response_body
            for param in out_parameter:
                if param.isdigit():
                    index = int(param)
                    current_place = current_place[index]
                    
                else:
                    for key, value in current_place.items():
                        if key == param:
                            current_place = value
                            break
            response.gasCost = current_place
        else:
            response.gasCost = response_body[api_output['gasCostParameter']]
   
    is_param_present = api_output.get('routesParameter')
    if is_param_present:
        if '/' in api_output['routesParameter']:
            out_parameter = api_output['routesParameter'].split('/')
            current_place = response_body
            for param in out_parameter:
                if param.isdigit():
                    index = int(param)
                    current_place = current_place[index]
                    
                else:
                    for key, value in current_place.items():
                        if key == param:
                            current_place = value
                            break
            response.routes = current_place
        else:
            response.routes = response_body[api_output['routesParameter']]

    is_param_present = api_output.get('callDataParameter')
    if is_param_present:
        if '/' in api_output['callDataParameter']:
            out_parameter = api_output['callDataParameter'].split('/')
            current_place = response_body
            for param in out_parameter:
                if param.isdigit():
                    index = int(param)
                    current_place = current_place[index]
                    
                else:
                    for key, value in current_place.items():
                        if key == param:
                            current_place = value
                            break
            response.callData = current_place
        else:
            response.callData = response_body[api_output['callDataParameter']]

    return response
