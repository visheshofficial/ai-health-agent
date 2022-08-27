# Health Agent


pip install rasa
pip install "rasa[transformers]"
pip install scispacy
pip install pandas
pip install https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.5.0/en_ner_bc5cdr_md-0.5.0.tar.gz

### Rasa server
To run the server, use the following command:

```commandline
rasa run --cors "*"
```


The --cors "*" command is used to solve the cross-origin resource sharing (CORS) problem between client and Rasa servers.


### Action server

```commandline
rasa run actions
```

Web client server
Run the following command:

```commandline
python -m http.server
```

This will start an HTTP-based server in the local 8000 port. We can visit http://localhost:8000 in a browser to visit the chatbot.



# Validations 
rasa data validate


