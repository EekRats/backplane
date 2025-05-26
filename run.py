from backplane import create_app

backplane = create_app()

if __name__ == '__main__':
    backplane.run(debug=True)