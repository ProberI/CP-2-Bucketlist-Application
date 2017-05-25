#!/usr/bin/env python3
from app import app


@app.route('/')
def index():
    return "Welcome to BucketList Application API"


if __name__ == '__main__':
    app.run()
