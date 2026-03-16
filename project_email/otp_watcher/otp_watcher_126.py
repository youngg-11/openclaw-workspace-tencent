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

# 可调参数
POLL_SECONDS = int(os.getenv('POLL_SECONDS', '2'))
OTP_REGEX = re.compile(os.getenv('OTP_REGEX', r'\b\d{4,8}\b'))
KEYWORDS = [k.strip().lower() for k in os.getenv('OTP_KEYWORDS', 'otp,code,verification,verify,验证码,动态码,校验码,一次性,password,login,signin,security').split(',') if k.strip()]

# 放宽后的“验证码来源”规则：
# 1) 命中关键词 + 数字；或
# 2) 发件人域名在白名单（可选）且有数字
SENDER_DOMAIN_ALLOW = [d.strip().lower() for d in os.getenv('SENDER_DOMAIN_ALLOW', '').split(',') if d.strip()]
SUBJECT_HINTS = [s.strip().lower() for s in os.getenv('SUBJECT_HINTS', 'verification,验证码,code,security,login').split(',') if s.strip()]

EXCLUDE_SUBJECT_PATTERNS = [
    re.compile(r'你有\d+\s*条新通知'),
    re.compile(r'你收到以下内容：\d+\s*条新通知'),
    re.compile(r'new notifications?', re.I),
]

MAIL_HOST = os.getenv('MAILBOX_2_HOST', 'imap.gmail.com')
MAIL_PORT = int(os.getenv('MAILBOX_2_PORT', '993'))
MAIL_USER = os.getenv('MAILBOX_2_USER', '')
MAIL_PASS = os.getenv('MAILBOX_2_PASS', '')
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
        return {'seen': [], 'last_uid': 0}
    try:
        d = json.loads(STATE_FILE.read_text(encoding='utf-8'))
        d.setdefault('seen', [])
        d.setdefault('last_uid', 0)
        return d
    except Exception:
        return {'seen': [], 'last_uid': 0}


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


def sender_domain(sender: str) -> str:
    s = sender.lower()
    if '@' not in s:
        return ''
    return s.split('@')[-1].strip('> "')


def extract_otp(subject, body, sender):
    if should_skip_subject(subject):
        return None

    txt = f"{subject}\n{body}"
    lower = txt.lower()
    subj_lower = subject.lower()

    matches = list(OTP_REGEX.finditer(txt))
    if not matches:
        return None

    kw_hit = any(k in lower for k in KEYWORDS)
    subj_hint_hit = any(h in subj_lower for h in SUBJECT_HINTS)
    domain = sender_domain(sender)
    sender_hit = bool(SENDER_DOMAIN_ALLOW and any(domain.endswith(d) for d in SENDER_DOMAIN_ALLOW))

    # 放宽策略：关键词命中 或 主题提示命中 或 发件域命中
    if not (kw_hit or subj_hint_hit or sender_hit):
        return None

    # 返回第一个候选验证码
    return matches[0].group(0)


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


def fetch_uid_range(conn, start_uid: int):
    conn.select('INBOX')
    criteria = f"UID {start_uid + 1}:*"
    typ, data = conn.uid('search', None, criteria)
    if typ != 'OK' or not data or not data[0]:
        return []
    return [int(x) for x in data[0].split() if x.isdigit()]


def bootstrap_last_uid(conn, state):
    conn.select('INBOX')
    typ, data = conn.uid('search', None, 'UID 1:*')
    if typ == 'OK' and data and data[0]:
        uids = [int(x) for x in data[0].split() if x.isdigit()]
        if uids:
            state['last_uid'] = max(uids)
            save_state(state)
            log(f"bootstrap last_uid={state['last_uid']} (skip history)")


def run_once(conn, state):
    if state.get('last_uid', 0) <= 0:
        bootstrap_last_uid(conn, state)
        return

    uids = fetch_uid_range(conn, state['last_uid'])
    if not uids:
        return

    for uid in uids:
        typ, msg_data = conn.uid('fetch', str(uid), '(RFC822)')
        if typ != 'OK' or not msg_data or not msg_data[0]:
            continue
        raw = msg_data[0][1]
        h = hashlib.sha256(raw).hexdigest()
        if h in state['seen']:
            state['last_uid'] = max(state['last_uid'], uid)
            continue

        msg = email.message_from_bytes(raw)
        subject = str(email.header.make_header(email.header.decode_header(msg.get('Subject', ''))))
        sender = msg.get('From', '')
        body = text_from_message(msg)

        otp = extract_otp(subject, body, sender)
        if otp:
            text = f"🔐 验证码提醒\n邮箱: {MAIL_USER}\n发件人: {sender}\n主题: {subject}\n验证码: {otp}\n时间(UTC): {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}"
            ok = send_push(text)
            log(f"OTP found and pushed={'ok' if ok else 'fail'} uid={uid} subject={subject[:80]}")
        else:
            log(f"No OTP uid={uid} subject={subject[:80]}")

        state['seen'].append(h)
        state['seen'] = state['seen'][-1000:]
        state['last_uid'] = max(state['last_uid'], uid)
        save_state(state)


def main():
    if not MAIL_USER or not MAIL_PASS:
        log('MAILBOX_2_USER/MAILBOX_2_PASS missing; exiting')
        return

    state = load_state()
    while True:
        try:
            ctx = ssl.create_default_context()
            conn = imaplib.IMAP4_SSL(MAIL_HOST, MAIL_PORT, ssl_context=ctx)
            conn.login(MAIL_USER, MAIL_PASS)
            log("about to select INBOX")
            typ, data = conn.select("INBOX")
            log(f"select result: {typ} {data}")
            log('IMAP login success')
            while True:
                run_once(conn, state)
                time.sleep(POLL_SECONDS)
        except Exception as e:
            log(f'loop error: {e}')
            time.sleep(10)


if __name__ == '__main__':
    main()
