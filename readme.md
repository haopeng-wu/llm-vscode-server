# Before running
Create .env-openai.yml and populate your openai credentials into .env-openai.yml

# To run
cd llm-vscode-server
docker build  -t llm-server:0.1 .
docker container run -p 8001:8000 -v "$(pwd)":/app llm-server:0.1
