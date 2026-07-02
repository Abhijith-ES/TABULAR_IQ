import pandas as pd


MAX_VALUE = 100
SCALAR_TYPES = (int, float, bool, str)

def format_response(execution_result,
                    execution_time_ms: float) -> dict:
    if isinstance(execution_result, pd.DataFrame):
        return {
            "type": "table",
            "data": {
                "columns" : execution_result.columns.to_list(),
                "rows" : execution_result.head(MAX_VALUE).values.to_list()
            },
            "metadata": {
                "total_rows": execution_result.shape[0],
                "returned_rows": min(MAX_VALUE, execution_result.shape[0]),
                "truncated": execution_result.shape[0] > MAX_VALUE,
                "execution_time_ms": execution_time_ms
            }
        }
    
    elif isinstance(execution_result, pd.Series):
        return {
            "type": "series",
            "data": {
                "name": execution_result.name,
                "values": execution_result.head(MAX_VALUE).to_list()
            },
            "metadata": {
                "total_values": len(execution_result),
                "returned_values": min(MAX_VALUE, len(execution_result)),
                "truncated": len(execution_result) > MAX_VALUE,
                "execution_time_ms": execution_time_ms
            }
        }
    
    elif isinstance(execution_result, pd.Timestamp):
        return {
            "type": "timestamp",
            "data": execution_result.isoformat(),
            "metadata": {
                "execution_time_ms": execution_time_ms
            }
        }
    
    elif isinstance(execution_result, SCALAR_TYPES):
        return {
            "type": "scalar",
            "data": execution_result,
            "metadata":{
                "execution_time_ms": execution_time_ms
            }
        }
    
    elif type(execution_result) == list:
        return {
            "type": "list",
            "data": execution_result[:MAX_VALUE],
            "metadata":{
                "total_values": len(execution_result),
                "returned_values": min(MAX_VALUE, len(execution_result)),
                "truncated": len(execution_result) > MAX_VALUE,
                "execution_time_ms": execution_time_ms
            }
        }
    
    elif type(execution_result) == dict:
        return {
            "type": "dictionary",
            "data": execution_result,
            "metadata":{
                "execution_time_ms": execution_time_ms
            }
        }
    
    else:
        return {
            "type": "text",
            "data": str(execution_result),
            "metadata":{
                "execution_time_ms": execution_time_ms
            }
        } 