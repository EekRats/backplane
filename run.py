from backplane import create_app

backplane = create_app()

if __name__ == '__main__':
    import os
    # Never default to the debugger: on an exposed port it is remote code
    # execution. Opt in explicitly with BACKPLANE_DEBUG=1 for local dev only.
    debug = os.environ.get('BACKPLANE_DEBUG') == '1'
    backplane.run(debug=debug)