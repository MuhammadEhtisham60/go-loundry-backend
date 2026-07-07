from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

from apps.chats.services import ChatService
from apps.chats.selectors import ChatSelector
from apps.chats.serializers import (
    ConversationSerializer,
    MessageSerializer,
    MessageInputSerializer,
    AssignAgentSerializer,
)
from apps.chats.permissions import IsSupportAgent
from common.responses.standard import StandardResponse


class ConversationListView(APIView):
    """
    API View to list and initiate support chat sessions.
    Requires authentication.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request: Request) -> Response:
        is_resolved_str = request.query_params.get("is_resolved")
        is_resolved = None
        if is_resolved_str is not None:
            is_resolved = is_resolved_str.lower() == "true"

        conversations = ChatSelector.get_conversations(
            user=request.user, is_resolved=is_resolved
        )
        serializer = ConversationSerializer(conversations, many=True)
        return StandardResponse(
            data=serializer.data,
            message="Support conversations list retrieved.",
            status=status.HTTP_200_OK,
        )

    def post(self, request: Request) -> Response:
        # Start or get the active unresolved support chat session
        conversation = ChatService.create_or_get_conversation(customer=request.user)
        return StandardResponse(
            data=ConversationSerializer(conversation).data,
            message="Support session initialized.",
            status=status.HTTP_200_OK,
        )


class MessageListView(APIView):
    """
    API View to retrieve conversation message histories and append replies.
    Supports file uploads for image attachments.
    """

    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get(self, request: Request, conversation_id: str) -> Response:
        messages = ChatSelector.get_messages(
            user=request.user, conversation_id=conversation_id
        )
        serializer = MessageSerializer(messages, many=True)
        return StandardResponse(
            data=serializer.data,
            message="Message history retrieved.",
            status=status.HTTP_200_OK,
        )

    def post(self, request: Request, conversation_id: str) -> Response:
        serializer = MessageInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        message = ChatService.send_message(
            sender=request.user,
            conversation_id=conversation_id,
            text=serializer.validated_data.get("text"),
            image_file=request.FILES.get("image"),
        )

        return StandardResponse(
            data=MessageSerializer(message).data,
            message="Message sent successfully.",
            status=status.HTTP_201_CREATED,
        )


class ConversationAssignView(APIView):
    """
    API View for back office admins to assign support agents to chat tickets.
    """

    permission_classes = [IsAuthenticated, IsSupportAgent]

    def post(self, request: Request, conversation_id: str) -> Response:
        serializer = AssignAgentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        conversation = ChatService.assign_agent(
            conversation_id=conversation_id,
            agent_id=str(serializer.validated_data["agent_id"]),
        )

        return StandardResponse(
            data=ConversationSerializer(conversation).data,
            message="Support agent assigned to chat ticket.",
            status=status.HTTP_200_OK,
        )


class ConversationResolveView(APIView):
    """
    API View for back office admins to resolve chat tickets.
    """

    permission_classes = [IsAuthenticated, IsSupportAgent]

    def post(self, request: Request, conversation_id: str) -> Response:
        conversation = ChatService.resolve_conversation(
            conversation_id=conversation_id
        )

        return StandardResponse(
            data=ConversationSerializer(conversation).data,
            message="Chat marked as resolved successfully.",
            status=status.HTTP_200_OK,
        )
