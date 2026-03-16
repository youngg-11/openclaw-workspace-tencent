#!/usr/bin/env python3
import imaplib
import email
import os
import re
import ssl
import time
import json
import hashlib
import subprocess
from datetime import datetime
from pathlib import Path

STATE_FILE = Path('/root/.openclaw/workspace/project_email/otp_watcher/state.json')
LOG_FILE = Path('/root/.openclaw/workspace/project_email/otp_watcher/otp.log')

OTP_REGEX = re.compile(os.getenv('OTP_REGEX', r'\\b\\d{4,8}\\b'))
KEYWORDS = [k.strip().lower() for k in os.getenv('OTP_KEYWORDS', 'otp,code,verification,verify,验证码,动态码,校验码,一次性').split(',') if k.strip()]
EXCLUDE_SUBJECT_PATTERNS = [
    re.compile(r'你有\d+\s*条新通知'),
    re.compile(r'new notifications?', re.I),
]

MAIL_HOST = os.getenv('MAILBOX_1_HOST', 'imap.gmail.com')
MAIL_PORT = int(os.getenv('MAILBOX_1_PORT', '993'))
MAIL_USER = os.getenv('MAILBOX_1_USER', '')
MAIL_PASS = os.getenv('MAILBOX_1_PASS', '')
OPENCLAW_BIN = os.getenv('OPENCLAW_BIN', '/root/.local/share/pnpm/openclaw')
PUSH_CHANNEL = os.getenv('PUSH_CHANNEL', 'feishu')
PUSH_TARGET = os.getenv('PUSH_TARGET', 'user:ou_6fca8ce759906602dfffae5538baa09f')


def log(msg: str):
    ts = datetime.utcnow().isoformat()
    line = f"[{ts}] {msg}"
    print(line, flush=True)
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with LOG_FILE.open('a', encoding='utf-8') as f:
        f.write(line + '\n')


def load_state():
    if not STATE_FILE.exists():
        return {'seen': []}
    try:
        return json.loads(STATE_FILE.read_text(encoding='utf-8'))
    except Exception:
        return {'seen': []}


def save_state(state):
    STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding='utf-8')


def text_from_message(msg):
    parts = []
    if msg.is_multipart():
        for part in msg.walk():
            ctype = part.get_content_type()
            if ctype in ('text/plain', 'text/html'):
                try:
                    payload = part.get_payload(decode=True) or b''
                    parts.append(payload.decode(part.get_content_charset() or 'utf-8', errors='ignore'))
                except Exception:
                    continue
    else:
        payload = msg.get_payload(decode=True) or b''
        parts.append(payload.decode(msg.get_content_charset() or 'utf-8', errors='ignore'))
    return '\n'.join(parts)


def should_skip_subject(subject: str) -> bool:
    return any(p.search(subject) for p in EXCLUDE_SUBJECT_PATTERNS)


def extract_otp(subject, body):
    if should_skip_subject(subject):
        return None

    txt = f"{subject}\n{body}"
    lower = txt.lower()

    # 必须出现关键词，避免普通通知数字误判
    if KEYWORDS and not any(k in lower for k in KEYWORDS):
        return None

    # 仅在关键词附近寻找数字串
    for m in OTP_REGEX.finditer(txt):
        start, end = m.span()
        win = txt[max(0, start - 60): min(len(txt), end + 60)].lower()
        if any(k in win for k in KEYWORDS):
            return m.group(0)
    return None


def send_push(text: str):
    try:
        proc = subprocess.run(
            [OPENCLAW_BIN, 'message', 'send', '--channel', PUSH_CHANNEL, '--target', PUSH_TARGET, '--message', text],
            capture_output=True,
            text=True,
            timeout=20,
            env={**os.environ, 'PATH': '/root/.nvm/versions/node/v22.22.0/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin'}
        )
        if proc.returncode != 0:
            log(f"push failed rc={proc.returncode} stderr={proc.stderr.strip()[:200]}")
            return False
        return True
    except Exception as e:
        log(f"push exception: {e}")
        return False


def run_once(conn, state):
    conn.select('INBOX')
    typ, data = conn.search(None, 'UNSEEN')
    if typ != 'OK':
        return
    for num in data[0].split():
        typ, msg_data = conn.fetch(num, '(RFC822)')
        if typ != 'OK' or not msg_data or not msg_data[0]:
            continue
        raw = msg_data[0][1]
        h = hashlib.sha256(raw).hexdigest()
        if h in state['seen']:
            continue
        msg = email.message_from_bytes(raw)
        subject = str(email.header.make_header(email.header.decode_header(msg.get('Subject', ''))))
        sender = msg.get('From', '')
        body = text_from_message(msg)
        otp = extract_otp(subject, body)
        if otp:
            text = f"🔐 验证码提醒\n邮箱: {MAIL_USER}\n发件人: {sender}\n主题: {subject}\n验证码: {otp}\n时间(UTC): {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}"
            ok = send_push(text)
            log(f"OTP found and pushed={'ok' if ok else 'fail'} subject={subject[:80]}")
        else:
            log(f"No OTP subject={subject[:80]}")
        state['seen'].append(h)
        state['seen'] = state['seen'][-500:]
        save_state(state)


def main():
    if not MAIL_USER or not MAIL_PASS:
        log('MAILBOX_1_USER/MAILBOX_1_PASS missing; exiting')
        return
    state = load_state()
    while True:
        try:
            ctx = ssl.create_default_context()
            conn = imaplib.IMAP4_SSL(MAIL_HOST, MAIL_PORT, ssl_context=ctx)
            conn.login(MAIL_USER, MAIL_PASS)
            log('IMAP login success')
            while True:
                run_once(conn, state)
                time.sleep(10)
        except Exception as e:
            log(f'loop error: {e}')
            time.sleep(15)


if __name__ == '__main__':
    main()
