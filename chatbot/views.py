from django.shortcuts import render, redirect
from .models import ChatSession, ChatMessage
from .utils import get_chatbot_response

def chatbot_view(request):
    # Get or create session in the database
    session_id = request.session.get('chat_session_id')
    if not session_id:
        chat_session = ChatSession.objects.create(user=request.user if request.user.is_authenticated else None)
        request.session['chat_session_id'] = chat_session.id
    else:
        chat_session = ChatSession.objects.get(id=session_id)

    if request.method == "POST":
        if "reset" in request.POST:
            request.session['chat_session_id'] = None
            return redirect("chatbot")

        user_msg = request.POST.get("message")
        if user_msg:
            # Save User Message
            ChatMessage.objects.create(session=chat_session, sender="user", message=user_msg)
            
            # Get Bot Response
            msg_count = chat_session.messages.count()
            bot_data = get_chatbot_response(
                user_msg, 
                msg_count=msg_count, 
                is_authenticated=request.user.is_authenticated
            )
            
            # Save Bot Message
            ChatMessage.objects.create(session=chat_session, sender="bot", message=bot_data['response'])

    chat_history = chat_session.messages.all().order_by('created_at')
    
    return render(request, "chatbot/chat.html", {
        "chat_history": chat_history,
        "is_anonymous": not request.user.is_authenticated
    })