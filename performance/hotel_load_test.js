import http from 'k6/http';
import { sleep, check } from 'k6';

export let options = {
    thresholds: {
        // הסף: אם 95% מהבקשות לוקחות יותר מ-150ms - הטסט קורס מיד!
        'http_req_duration': [{ threshold: 'p(95)<150', abortOnFail: true }],
        'http_req_failed': [{ threshold: 'rate<0.01', abortOnFail: true }],
    },
    stages: [
        { duration: '10s', target: 500 },  // זינוק מהיר ל-500
        { duration: '20s', target: 2000 }, // טיפוס אגרסיבי ל-2000
    ],
};

export default function () {
    let res = http.get('https://automationintesting.online/room/');
    
    check(res, {
        'status is 200': (r) => r.status === 200,
    });
    
    // כמעט אפס מנוחה בין בקשה לבקשה
    sleep(0.01); 
}