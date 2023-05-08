import http from 'k6/http';
import { check, group } from 'k6';
import { Counter } from 'k6/metrics';
import { SharedArray } from 'k6/data';

const postReqFailures = new Counter('post_req_failures');
const getReqFailures = new Counter('get_req_failures');

export let options = {
  scenarios: {
    get_requests: {
      executor: 'ramping-vus',
      startVUs: 10,
      stages: [
        { duration: '30s', target: 100 },
        { duration: '1m', target: 2000 },
        { duration: '30s', target: 0 },
      ],
      exec: 'getEndpoint',
    },
    post_requests: {
      executor: 'ramping-vus',
      startVUs: 10,
      stages: [
        { duration: '30s', target: 50 },
        { duration: '1m', target: 200 },
        { duration: '30s', target: 0 },
      ],
      exec: 'postEndpoint',
    },
  },
};

export function getEndpoint() {
  group('GET requests', () => {
    const getResponse = http.get('http://localhost/repositories');
    const isGetReqSuccessful = check(getResponse, {
      'Get request status is 200': (r) => r.status === 200,
    });

    if (!isGetReqSuccessful) {
      getReqFailures.add(1);
    }
  });
}

export function postEndpoint() {
  group('POST requests', () => {
    const payload = JSON.stringify({
      text: 'string',
      top_k: 5,
    });

    const params = {
      headers: {
        'Content-Type': 'application/json',
      },
    };

    const postResponse = http.post('http://localhost/search', payload, params);
    const isPostReqSuccessful = check(postResponse, {
      'Post request status is 200': (r) => r.status === 200,
    });

    if (!isPostReqSuccessful) {
      postReqFailures.add(1);
    }
  });
}
