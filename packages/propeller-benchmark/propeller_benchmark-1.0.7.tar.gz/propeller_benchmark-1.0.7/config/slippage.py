from .aggregators import SupportedAggregators

slippage_multipliers = {
    '1Inch': 0.001,  # 0.1% expressed as 0.001
    'propeller': 0.000005,  # 0.0005%
    'enso': 1,  # 100% expressed as 1
    '0x': 0.01,  # 1%
    'odos': 0.001  # 0.1% expressed as 0.001
}

def convert_slippage(slippage_value: float, dex_name: str):
    if dex_name not in slippage_multipliers:
        return 0
    return slippage_value * slippage_multipliers[dex_name]
