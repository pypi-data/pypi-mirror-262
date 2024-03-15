from typing import Optional, Union, Any

class ApiKey:
    def __init__(self, place: str, value: str):
        self.place = place
        self.value = value

class ApiRequestInputNames:
    def __init__(self, tokenInParameter: str, tokenOutParameter: str, amountInParameter: str, slippage: Optional[dict] = None, jsonBody: Optional[str] = None):
        self.tokenInParameter = tokenInParameter
        self.tokenOutParameter = tokenOutParameter
        self.amountInParameter = amountInParameter
        self.slippage = slippage
        self.jsonBody = jsonBody

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

class DexApiRequestInput(ApiRequestInputNames):
    def __init__(self, tokenInParameter: str, tokenOutParameter: str, amountInParameter: str, url: str, requestMethod: str, maxApiRequestsPerInstance: int, slippage: Optional[dict] = None, jsonBody: Optional[str] = None, apiKey: Optional[ApiKey] = None, additionalBodyParameters: Optional[Any] = None):
        super().__init__(tokenInParameter, tokenOutParameter, amountInParameter, slippage, jsonBody)
        self.url = url
        self.requestMethod = requestMethod
        self.apiKey = apiKey
        self.additionalBodyParameters = additionalBodyParameters
        self.maxApiRequestsPerInstance = maxApiRequestsPerInstance

class Dex:
    def __init__(self, apiInput: DexApiRequestInput, apiOutput: ApiRequestOutputNames):
        self.apiInput = apiInput
        self.apiOutput = apiOutput

class StoredDex:
    def __init__(self, totalRequests: int, failedRequests: int, succeededRequests: int, swaps: dict):
        self.totalRequests = totalRequests
        self.failedRequests = failedRequests
        self.succeededRequests = succeededRequests
        self.swaps = swaps
