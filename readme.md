# Before running
Create .env-openai.yml and populate your openai credentials into .env-openai.yml

# To run
```bash
cd llm-vscode-server
```
1. Build the image.
```bash
docker build  -t llm-server:0.1 .
```

2. Run the container
```bash
docker container run -p 8001:8000 -v "$(pwd)":/app llm-server:0.1
```

3. Test it
```bash
curl http://0.0.0.0:8001/health
```

```bash
curl http://0.0.0.0:8001/generate -d '{"inputs":"import spacy"}' -H "Content-Type: application/json"
```
