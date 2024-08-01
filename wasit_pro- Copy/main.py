from website import create_app
# create_app is a function in __init__.py

app = create_app() 

if __name__=='__main__':
    app.run(debug=True, port=5002) # debug allows for automatic
