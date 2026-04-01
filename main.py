import os, logging, requests
from flask import Flask, request, jsonify
app = Flask(__name__)
TOKEN = os.environ.get("BOT_TOKEN")
API = f"https://api.telegram.org/bot{TOKEN}"
def send_msg(cid, txt):
    try: requests.post(f"{API}/sendMessage", json={"chat_id":cid,"text":txt,"parse_mode":"Markdown"}, timeout=10)
    except: pass
def handle(u):
    m=u.get("message")
    if not m: return
    cid=m["chat"]["id"]; txt=m.get("text","").strip(); name=m.get("from",{}).get("first_name","")
    if txt=="/start": send_msg(cid,"🎯 *TrustPlay Bot*\n\nNamaste! ID lene ke liye:\n/newid — ID lena\n/contact — Contact")
    elif txt=="/newid": send_msg(cid,"🆕 ID lene ke liye WhatsApp karo:\n👉 https://wa.link/vanki")
    elif txt=="/contact": send_msg(cid,"📞 Telegram: @A8439977550\nWhatsApp: https://wa.link/vanki")
    else: send_msg(cid,f"👋 Hi {name}! /start type karo")
@app.route("/",methods=["GET"])
def index(): return jsonify({"status":"ok"})
@app.route("/webhook",methods=["POST"])
def webhook(): handle(request.get_json(force=True)); return jsonify({"ok":True})
@app.route("/set_webhook",methods=["GET"])
def set_wh():
    url=request.host_url.rstrip("/")+"/webhook"
    r=requests.get(f"{API}/setWebhook?url={url}")
    return jsonify({"url":url,"result":r.json()})
if __name__=="__main__": app.run(host="0.0.0.0",port=int(os.environ.get("PORT",8080)))
