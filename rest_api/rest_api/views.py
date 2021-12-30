from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime


class TimeView(APIView):
    """ A simple view to see the time """

    def get(self, request, format=None):
        date = datetime.now().strftime("%d-%m-%Y, %H:%M:%S")
        message = f'Current time is {date}'
        return Response(data={"message":message}, status=status.HTTP_200_OK)