from rest_framework import viewsets
from ...models import Review
from .permissions import IsAuthenticatedOrReadOnly
from .reviewserializers import ReviewSerializer

class ReviewModelViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # To be defined later
    