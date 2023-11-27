import datetime

from pytz import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from weapon.contacts.models import Suggest
from weapon.contacts.serializers import SuggestSerializer
from rest_framework.permissions import IsAuthenticated


KST = timezone('Asia/Seoul')
UTC = timezone("UTC")


class SuggestViewSet(viewsets.ModelViewSet):
    queryset = Suggest.objects.all()
    serializer_class = SuggestSerializer

    @action(methods=['get'], detail=False, permission_classes=[IsAuthenticated])
    def me(self, request):
        user = request.user

        queryset = self.filter_queryset(self.get_queryset()).filter(user=user)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
