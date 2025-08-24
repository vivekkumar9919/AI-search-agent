
from tools.product_tools import calculate_average_price, profit_margin_analyzer, price_band_distribution, low_stock_with_velocity

TOOLS = {
    "calculate_average_price": calculate_average_price,
    "profit_margin_analyzer": profit_margin_analyzer,
    "price_band_distribution":price_band_distribution,
    "low_stock_with_velocity":low_stock_with_velocity
}

def call_tool(tool_name: str, *args, **kwargs):
    """
    Dispatch tool call dynamically from the TOOLS registry.
    
    :param tool_name: Name of the tool (key in TOOLS dict)
    :param args: Positional args for the tool
    :param kwargs: Keyword args for the tool
    :return: Result of tool execution
    """
    tool = TOOLS.get(tool_name)
    if not tool:
        raise ValueError(f"Unknown tool: {tool_name}")
    return tool(*args, **kwargs)
