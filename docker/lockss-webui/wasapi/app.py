#!/usr/bin/env python3

import connexion

if __name__ == '__main__':
    app = connexion.App(__name__, specification_dir='./swagger/')
    app.add_api('swagger.yaml', arguments={'title': 'WASAPI Export API.  A draft of the minimum that a Web Archiving Systems API server must implement. '})
    app.run(port=8880)
