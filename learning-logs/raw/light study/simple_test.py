import pytest
import requests

N8N_CHAT_URL = 'http://localhost:5678/webhook/7514fdfb-654e-4010-8cf5-e6d1cbd1dc09/chat'

test_cases = [
    {'input': '1 + 2 + 3', 'expected': 6},
    {'input': '1 부터 100까지 더해줘', 'expected': '5050'},
    {'input': '1 - 2 + 3', 'expected': '2'},
    {'input': '1 부터 100까지 더한 값에 5000을 빼줘', 'expected': '50'}
]

@pytest.mark.parametrize('case', test_cases)
def test_task_success(case):
    resp = requests.post(N8N_CHAT_URL, json={
        'chatInput': case['input'],
        'sessionId': 'automated-test',
    })
    output = resp.json()['output']
    assert str(case['expected']) in output