from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import CreateModelMixin
from rest_framework import request,response,status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .models import Review, ReviewMedia
from .serializers import ReviewSerializer, ReviewReportSerializer, MediaReviewSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]

    def get_queryset(self):
        return Review.objects.all()


    @action(detail=True, permission_classes=[IsAuthenticated], methods=['GET'])
    def vote(self, request:request.Request, pk):
        review : Review = self.get_object()
        review.votes.add(request.user)
        return response.Response(status=status.HTTP_200_OK)


    @action(detail=True, permission_classes=[IsAuthenticated], methods=['GET'])
    def unvote(self, request:request.Request, pk):
        review : Review = self.get_object()
        review.votes.remove(request.user)
        return response.Response(status=status.HTTP_200_OK)


class ReviewMediaViewSet(ModelViewSet):
    queryset = ReviewMedia.objects.all()
    serializer_class = MediaReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


    def create(self, request):
        files = request.FILES.getlist('file')#files

        files_ids = []

        for file in files:
            file_created = ReviewMedia.objects.create(file=file)
            files_ids.append(file_created.id)

        return Response(files_ids, status=status.HTTP_200_OK)


class ReviewReportCreateAPIView(CreateModelMixin, GenericViewSet):
    serializer_class = ReviewReportSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer) -> None:
        serializer.save(review_id = self.kwargs['review_id'], user=self.request.user)