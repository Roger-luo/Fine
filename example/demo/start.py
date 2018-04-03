from fine import Fine

app = Fine(__name__)
app.load_config(filename='config.yml')

if __name__ == '__main__':
    app.run()
