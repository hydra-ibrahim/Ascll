from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import UserFCMToken, ChatMessage
from .serializers import FCMTokenSerializer, ChatMessageSerializer
from django.contrib.auth.models import User
from .firebase_chat import send_fcm_notification

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def store_fcm_token(request):
    user = request.user
    token = request.data.get("fcm_token")

    if not token:
        return Response({"error": "FCM token is required"}, status=400)

    obj, created = UserFCMToken.objects.update_or_create(user=user, defaults={"fcm_token": token})
    
    return Response({"message": "FCM Token stored successfully"})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_message(request):
    sender = request.user
    receiver_id = request.data.get("receiver")
    message_text = request.data.get("message")

    try:
        receiver = User.objects.get(id=receiver_id)
        chat_message = ChatMessage.objects.create(sender=sender, receiver=receiver, message=message_text)
        
        # Retrieve FCM Token
        receiver_fcm = UserFCMToken.objects.filter(user=receiver).first()
        if receiver_fcm:
            send_fcm_notification(receiver_fcm.fcm_token, "New Message", message_text)
        
        return Response({"message": "Message sent successfully!"})
    
    except User.DoesNotExist:
        return Response({"error": "Receiver not found"}, status=404)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_messages(request, user_id):
    sender = request.user
    receiver_id = user_id

    # Fetch chat messages between sender and receiver (both ways)
    messages = ChatMessage.objects.filter(
        sender=sender, receiver_id=receiver_id
    ) | ChatMessage.objects.filter(
        sender_id=receiver_id, receiver=sender
    ).order_by("timestamp")  # Order by oldest to newest

    serializer = ChatMessageSerializer(messages, many=True)
    return Response(serializer.data)
