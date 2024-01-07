# /non_functional telegram_planfix_integration/app.py

import threading
from os import sync

from app import app
from app.utils import synchronize_messages_bidirectional

if __name__ == '__main__':
    with app.test_request_context():
        synchronize_messages_bidirectional()

    q = threading.Thread(target=sync)
    q.start()

    app.run(debug=True)
