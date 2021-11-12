# vui

## Virtines frontend

A simple UI and CLI to interface with Virtines. Currently supported languages are c and ~~js~~.


## Available functions:

### actions:
- create
- get
- ~~update~~
- ~~save~~
- delete
- invoke
- list

### moitoring/telemetry:
- ~~CPU usage~~
- ~~usage memory~~
- ~~number of instances (warm, cold)~~
- ~~Cold start time~~
- ~~Execution time~~
- ~~invocation traces~~

### testing:
- ~~workload generator~~

### logging:
- ~~invocations~~
- ~~misses~~

### trigger:
- ~~Message queue~~
- RESTFUL call

## Todo:

- Multiple language support
- Map action names to function names
- Map function signature to key_value pair
- Save functions in db/fs
- Natively call wasp as shared library while passing the path of bin as one of the argument
- Include dependencies
- ~~Execute virtines using restful APIs~~
- ~~Using namespace to map actions~~
- ~~Create a main class to handle toplevel stuff~~
- ~~Use fastapi/other service to achieve production level code~~

## Steps to run


Steps to start the Server:
```python3 fast_app.py```

To view webpage:
```host:8989/```

To view swagger documentation:
```host:8989/docs```

## *Notes

- By default running on port 8989
- Interfaces to support multiple languages implemented
- Need to look into CLI
- Steps to install virtines [here](install_steps_and_resources.md)

### Resources

- https://arxiv.org/abs/2104.11324
- https://apt.llvm.org/

