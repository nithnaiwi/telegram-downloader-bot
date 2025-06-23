from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
import requests

BOT_TOKEN = '7596997075:AAHsOxLyIlDfqm99dGClXx8xwBCpQ4D85a8'
TELEGRAM_API_URL = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'

@csrf_exempt
def telegram_webhook(request):
    if request.method == "POST":
        data = json.loads(request.body)
        message = data.get('message', {})
        chat_id = message.get('chat', {}).get('id')
        text = message.get('text', '').lower()

        if text == "hi":
            reply = "Hello Bro or Sis!"
        elif text == "Build Bright University":
            reply = "Try saying 'hi', 'bbu', or 'info' to get more replies."
        elif text in ["bbu", "info"]:
            reply = (
                "🎓 *Build Bright University (BBU)*\n\n"
                "🏛 *Founded:* 2000\n"
                "🌍 *Campuses:* Phnom Penh, Siem Reap, Battambang, Banteay Meanchey, Sihanoukville, Takeo, Ratanakiri, etc.\n"
                "🎯 *Vision:* To be a nationally and internationally recognized university.\n"
                "📚 *Programs:* Associate, Bachelor, Master, Ph.D.\n"
                "🏫 *Faculties:* Business, Science & Tech, Engineering, Doctoral Studies\n"
                "📞 *Contact:* 023 987 700 | info@bbu.edu.kh\n"
                "🌐 Website: https://bbu.edu.kh/"
            )
        else:
            reply = f"You said: {text}"

        # Send reply to user
        requests.post(TELEGRAM_API_URL, data={
            'chat_id': chat_id,
            'text': reply,
            'parse_mode': 'Markdown'
        })

        return JsonResponse({"status": "ok"})

    return JsonResponse({"error": "Invalid request"}, status=400)


