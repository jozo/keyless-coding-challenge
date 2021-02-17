# keyless-coding-challenge
Coding challenge from Keyless.io

API for encryption of input data with AES-GCM. Implemented with Python and FastAPI.

Docs (Swagger): http://0.0.0.0:8000/docs

## How to run

**Docker**
```shell
docker-compose up
```

**Poetry**
```shell
poetry install
poetry run uvicorn api.main:app
```

### Example POST request
POST http://0.0.0.0:8000/api/encrypt/
```json
{
    "data": "YWhvag=="
}
```

Output
```json
{
    "ciphertext": "b8b2vT25fHSVbAGqBHeGhdevVAQ=",
    "key": "9kyu5t7gRSmTFycUwcRtSZdIcfc4EcKK+KkzaO6oyC0=",
    "nonce": "u2Ql2bWPFHzYqGNK"
}
```

## Possible improvements
- API versioning
- rate limiting
- Add CI (build image, run tests, scan security issues)
- Add tracing, monitoring, Sentry...
- Play with uvicorn config - e.g. number of workers
- CORS


## Assignment
Imagine that your first task once you’ll join the Keyless team will be to 
design and implement a micro-service that acts as an encryption oracle.

Specifically, the micro-service should expose some REST APIs that allow 
the caller to encrypt a payload (provided as an input to the API) using AES-GCM.
The encrypted payload shall be returned as a response the user (as an output 
of the REST API), together with the AES encryption key used and to any 
additional information required.

The service should run within a Docker image/container and should follow best 
practices for REST APIs, micro-services, and secure software development. Bonus 
points if it ships with unit and integration tests.

Please take a moment to consider this task and try to implement 
the micro-service it describes. Then, within a few days from this message, 
zip the resulting implementation within a compressed archive and attach it 
to this mail. Feel free to also add any design specification or additional 
material that you have prepared.
