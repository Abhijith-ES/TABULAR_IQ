import pandas as pd
import numpy as np
import time


def execute_code(code: str, df: pd.DataFrame) -> dict:
    execution_globals = {
        "__builtins__": {
            "sum": sum,
            "min": min,
            "max": max,
            "abs": abs,
            "round": round
            },
        "pd": pd,
        "np": np,
    }

    execution_locals = {
        "df": df
    }

    try:
        start = time.perf_counter()
        exec(code, execution_globals, execution_locals)
        end = time.perf_counter()

        result = execution_locals["result"]

        return {
            "result": result,
            "execution_time_ms": (end-start)*1000
        }
    
    except KeyError:
        raise ValueError("The Executed code doesn't produces 'result' variable.")