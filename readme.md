# To run
1. Enter the directory,
```bash
cd llm-vscode-server
```
2. Under one terminal, run
```bash
python server.py
```

3. Under another terminal, run
```bash
gunicorn -c gunicorn.conf.py main:app
```


3. Test it
```bash
curl http://127.0.0.1:8000/health
```

```bash
curl http://127.0.0.1:8000/generate -d '{"inputs":"<fim_prefix>def fib(n):<fim_suffix>    else:\n        return fib(n - 2) + fib(n - 1)<fim_middle>"}' -H "Content-Type: application/json"
```

4. Use with the extension
    1. install the vscode extension, **llm-vscode**, and open the settings for it
    2. change “Config Template” to `custom`
    3. change “Model ID Or Endpoint” to `http://localhost:8000/` or `http://0.0.0.0:8000/`, whichever works for you.
