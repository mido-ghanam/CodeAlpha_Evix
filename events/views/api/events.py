from rest_framework import generics, permissions, pagination
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.db.models import Q
from datetime import datetime

from ...serializers import EventSerializer
from ...models import Event


class IsAdminOrReadOnly(permissions.BasePermission):
  def has_permission(self, request, view):
    if request.method in permissions.SAFE_METHODS:
      return True
    return bool(request.user and request.user.is_staff)


class EventPagination(pagination.PageNumberPagination):
  page_size = 10
  page_size_query_param = 'page_size'


class EventsListCreateAPI(generics.ListCreateAPIView):
  queryset = Event.objects.all().order_by('-start_date')
  serializer_class = EventSerializer
  permission_classes = [IsAdminOrReadOnly]
  pagination_class = EventPagination

  def get_queryset(self):
    qs = super().get_queryset()
    q = self.request.query_params.get('search')
    category = self.request.query_params.get('category')
    date_str = self.request.query_params.get('date')

    if q:
      qs = qs.filter(Q(title__icontains=q) | Q(description__icontains=q))

    if category:
      qs = qs.filter(category__iexact=category)

    if date_str:
      try:
        date_obj = datetime.fromisoformat(date_str).date()
        qs = qs.filter(start_date__date=date_obj)
      except Exception:
        pass

    return qs

  def perform_create(self, serializer):
    organizer = self.request.user if self.request.user and self.request.user.is_authenticated else None
    serializer.save(organizer=organizer)


class EventsDetailAPI(generics.RetrieveUpdateDestroyAPIView):
  queryset = Event.objects.all()
  serializer_class = EventSerializer
  permission_classes = [IsAdminOrReadOnly]


class UploadBannerAPI(APIView):
  permission_classes = [permissions.IsAdminUser]

  def post(self, request, pk):
    event = get_object_or_404(Event, pk=pk)
    file = request.FILES.get('banner')
    if not file:
      return Response({"status": False, "message": "no file provided"}, status=400)

    # Basic validation: content type and size
    content_type = getattr(file, 'content_type', '')
    if not content_type.startswith('image/'):
      return Response({"status": False, "message": "invalid file type"}, status=400)

    max_size = 5 * 1024 * 1024  # 5 MB
    if file.size > max_size:
      return Response({"status": False, "message": "file too large"}, status=400)

    # Verify image using Pillow
    try:
      from PIL import Image
      img = Image.open(file)
      img.verify()
      # Reset file pointer for Django to read it again
      file.seek(0)
    except Exception:
      return Response({"status": False, "message": "corrupt or invalid image"}, status=400)

    event.banner = file
    event.save()
    banner_url = event.banner.url if getattr(event.banner, 'url', None) else None
    return Response({"status": True, "message": "banner uploaded", "banner_url": banner_url})


class CategoriesAPI(APIView):
  permission_classes = [permissions.AllowAny]

  def get(self, request):
    cats = Event.objects.values_list('category', flat=True).distinct()
    # filter out empty
    cats = [c for c in cats if c]
    return Response({"status": True, "categories": cats})

