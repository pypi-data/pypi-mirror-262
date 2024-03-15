from typing import Optional, Union

class Token:
    def __init__(self, name: str, address: str, decimals: int, amounts_in: list):
        self.name = name
        self.address = address
        self.decimals = decimals
        self.amounts_in = amounts_in

class ApiRequestInputNames:
    def __init__(self, tokenInParameter: str, tokenOutParameter: str, amountInParameter: str, slippage: Optional[dict] = None, jsonBody: Optional[str] = None):
        self.tokenInParameter = tokenInParameter
        self.tokenOutParameter = tokenOutParameter
        self.amountInParameter = amountInParameter
        self.slippage = slippage
        self.jsonBody = jsonBody

class ApiRequestInputValues:
    def __init__(self, tokenIn: Token, tokenOut: Token, amountIn: Union[str, int], slippage: Optional[int] = None):
        self.tokenIn = tokenIn
        self.tokenOut = tokenOut
        self.amountIn = amountIn
        self.slippage = slippage

class ApiRequestOutputNames:
    def __init__(self, amountOutParameter: str, gasCostParameter: Optional[str] = None, routesParameter: Optional[str] = None, callDataParameter: Optional[str] = None, gasPriceParameter: Optional[str] = None):
        self.amountOutParameter = amountOutParameter
        self.gasCostParameter = gasCostParameter
        self.routesParameter = routesParameter
        self.callDataParameter = callDataParameter
        self.gasPriceParameter = gasPriceParameter

class ApiRequestOutputValues:
    def __init__(self, requestStartTimestamp: str, requestReturnedTimestamp: str, timestampElapsedBetweenRequestAndResponse: str, requestId: str, hopsLength: int, amountIn: Union[str, int], amountOut: Union[str, int], gasCost: Optional[Union[str, int]] = None, routes: Optional[Union[list, str]] = None, callData: Optional[str] = None, gasPrice: Optional[str] = None):
        self.amountIn = amountIn
        self.amountOut = amountOut
        self.gasCost = gasCost
        self.requestStartTimestamp = requestStartTimestamp
        self.requestReturnedTimestamp = requestReturnedTimestamp
        self.timestampElapsedBetweenRequestAndResponse = timestampElapsedBetweenRequestAndResponse
        self.requestId = requestId
        self.hopsLength = hopsLength
        self.routes = routes
        self.callData = callData
        self.gasPrice = gasPrice

