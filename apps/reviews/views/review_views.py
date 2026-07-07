from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response

from apps.reviews.services import ReviewService
from apps.reviews.selectors import ReviewSelector
from apps.reviews.serializers import ReviewSerializer, ReviewCreateSerializer
from apps.reviews.permissions import IsCustomer
from common.responses.standard import StandardResponse


class ReviewListView(APIView):
    """
    API View to list and create customer reviews.
    Requires authentication.
    """

    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated(), IsCustomer()]
        return [IsAuthenticated()]

    def get(self, request: Request) -> Response:
        rating_param = request.query_params.get("rating")
        date_from = request.query_params.get("date_from")
        date_to = request.query_params.get("date_to")

        rating = int(rating_param) if rating_param is not None else None

        reviews = ReviewSelector.get_reviews(
            user=request.user,
            rating=rating,
            date_from=date_from,
            date_to=date_to,
        )
        serializer = ReviewSerializer(reviews, many=True)
        return StandardResponse(
            data=serializer.data,
            message="Reviews list retrieved successfully.",
            status=status.HTTP_200_OK,
        )

    def post(self, request: Request) -> Response:
        serializer = ReviewCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        review = ReviewService.create_review(
            user=request.user, validated_data=serializer.validated_data
        )
        result_serializer = ReviewSerializer(review)

        return StandardResponse(
            data=result_serializer.data,
            message="Review submitted successfully.",
            status=status.HTTP_201_CREATED,
        )
