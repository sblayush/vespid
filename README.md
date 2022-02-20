# Vespid

## Vespid User Interface

A Serverless Platform to interface with Virtines. In this platform, users can register Javascript and C functions, which produces requests to Virtines endpoint. These requests are handled by a concurrent server which runs each serverless function in a distinct virtine (rather than a container) by leveraging the Wasp runtime API. 

## Available functions:

### actions:
- create
- get
- delete
- invoke
- list

### moitoring/telemetry:
- CPU usage
- Memory usage
- Execution time

### testing:
- workload generator using locust

### logging:
- invocations
- cache hits and misses

### trigger:
- RESTFUL call

## Steps to run


Steps to start the Server:
```python3 app.py```

To view webpage:
```<host_ip>:8989/```

To view swagger documentation:
```<host_ip>:8989/docs```

## *Notes

- By default running on port 8989
- Steps to install virtines [here](install_steps_and_resources.md)

### Resources

- https://arxiv.org/abs/2104.11324
- https://apt.llvm.org/
