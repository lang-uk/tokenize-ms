# tokenize-ms
Microservice for tokenization

## Usage

### Docker

Easiest way to run it though the Docker (even on Windows). Once you have Docker installed, do the following:

```
docker run -it -p 8080:8080 chaliy/tokenize-ms
```

## Examples

### Curl

Show info about service
```
curl -X POST -H "Content-Type: application/json; charset=UTF-8" -d '{ "text": "Несе Галя воду, Коромисло гнеться, За нею Іванко, Як барвінок, в’ється." }' http://localhost:8080/tokenize_text/
```

# License

MIT
