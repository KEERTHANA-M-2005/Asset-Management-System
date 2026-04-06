from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)
resp = client.get('/api/reports/?period=30d')
print('STATUS', resp.status_code)
print('TEXT', resp.text)
print('CT', resp.headers.get('content-type'))
