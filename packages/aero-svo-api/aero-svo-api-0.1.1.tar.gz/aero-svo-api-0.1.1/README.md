# aero-svo-api  
Unoficial API wrapper for Sheremetyevo International Airport [svo.aero](https://www.svo.aero/ru/main)
* Asynchronous usage
* Pydantic models as a result

## Install
```commandline
pip install aero-svo-api
```
## Basic Usage
### Example
```python
import asyncio
from datetime import datetime, timedelta
from aero_svo_api import AsyncSvoApi


async def main():
    async with AsyncSvoApi() as api:
        schedule = await api.get_schedule(
            direction='arrival',
            date_start=datetime.now() - timedelta(hours=2),
            date_end=datetime.now(),
            per_page=3,
            page=1,
        )
        print(schedule)

        
asyncio.run(main())
```