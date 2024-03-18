<!-- <br />
<a href="https://github.com/stream-processing/sp2#gh-light-mode-only">
  <img src="https://github.com/stream-processing/sp2/raw/main/docs/img/sp2-light.png?raw=true#gh-light-mode-only" alt="sp2" width="400"></a>
</a>
<a href="https://github.com/stream-processing/sp2#gh-dark-mode-only">
  <img src="https://github.com/stream-processing/sp2/raw/main/docs/img/sp2-dark.png?raw=true#gh-dark-mode-only" alt="sp2" width="400"></a>
</a>
<br/> -->

# sp2

[![PyPI](https://img.shields.io/pypi/v/sp2.svg?style=flat)](https://pypi.python.org/pypi/sp2)
[![License](https://img.shields.io/badge/license-Apache--2.0-green)](https://github.com/timkpaine/sp2/LICENSE)
[![Build Status](https://github.com/timkpaine/sp2/actions/workflows/build.yml/badge.svg)](https://github.com/timkpaine/sp2/actions/workflows/build.yml)
[![Python Versions](https://img.shields.io/badge/python-3.8_%7C_3.9_%7C_3.10_%7C_3.11-blue)](https://github.com/timkpaine/sp2/blob/main/pyproject.toml)

<br/>

`sp2` is a high performance reactive stream processing library. The main engine is a C++ complex event graph processor, with bindings exposed into Python. Its key features include switchable simulation/realtime timesteps for both offline and online processing, custom input and output adapters for integration with static and streaming data sources and sinks, and extensible acceleration via customizable C++ nodes for calculations.

The high level goal of `sp2` is to make writing realtime code simple and performant. Write event driven code once, test it in simulation, then deploy as realtime without any code changes.

Here is a very simple example of a small `sp2` program to calculate a [bid-ask spread](https://www.investopedia.com/terms/b/bid-askspread.asp). In this example, we use a constant bid and ask, but in the real world you might pipe these directly into your live streaming data source, or into your historical data source, without modifications to your core logic.

```python
import sp2
from sp2 import ts
from datetime import datetime


@sp2.node
def spread(bid: ts[float], ask: ts[float]) -> ts[float]:
    if sp2.valid(bid, ask):
        return ask - bid


@sp2.graph
def my_graph():
    bid = sp2.const(1.0)
    ask = sp2.const(2.0)
    s = spread(bid, ask)

    sp2.print('spread', s)
    sp2.print('bid', bid)
    sp2.print('ask', ask)


if __name__ == '__main__':
    sp2.run(my_graph, starttime=datetime.utcnow())
```

Running this, our output should look like (with some slight variations for current time):

```raw
2024-02-07 04:37:13.446548 bid:1.0
2024-02-07 04:37:13.446548 ask:2.0
2024-02-07 04:37:13.446548 spread:1.0
```

## Getting Started

See [our wiki!](https://github.com/stream-processing/sp2/wiki)

## Development

Check out the [Developer Documentation](https://github.com/stream-processing/sp2/wiki/99.-Developer)

## Authors

`sp2` was originally developed as `csp` at Point72 by the High Frequency Algo team, with contributions from users across the firm.

## License

This software is licensed under the Apache 2.0 license. See the [LICENSE](LICENSE) file for details.
