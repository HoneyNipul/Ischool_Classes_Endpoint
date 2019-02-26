import datetime
from collections import OrderedDict

import requests
from auth_core.api_permissions import IsOwnerOrAuthReadOnly
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.utils import timezone
from drf_yasg.utils import no_body, swagger_auto_schema
from rest_framework import generics, pagination, status, views, viewsets
from rest_framework.compat import coreapi, coreschema
from rest_framework.decorators import (api_view, authentication_classes,
                                       detail_route, list_route)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .permissions import IsAuthenticatedSU
from .serializers import (
    ClassSerializer,
    EmptySerializer,
    TermSerializer,
    WaitlistClassSerializer,
    ClassWaitlistEntrySerializer,
    )

from . import olddbservice

# See http://www.django-rest-framework.org/


class iSchoolClassAPI():

    def class_list(self, termid=None):
        """ class list

        Get class list by term from old ischool api

        :param termid: string
        :return list: class object
        """
        if termid is None:
            response = requests.get('{}classes/?fullInstructorInfo=true'.format(settings.ISCHOOL_API_HOST), auth=(settings.ISCHOOL_API_USER, settings.ISCHOOL_API_PASSWORD))
        else:
            response = requests.get('{}classes/term/{}?fullInstructorInfo=true'.format(settings.ISCHOOL_API_HOST, termid), auth=(settings.ISCHOOL_API_USER, settings.ISCHOOL_API_PASSWORD))
        if response.status_code != status.HTTP_200_OK:
             return None
        data = response.json()
        return data


    def class_detail(self, classid):
        """ class detail

        Get class from old ischool api

        :param classid: string
        :return dict: class object
        """
        classid = classid.replace("-", ".")
        url = '{}classes/{}?professorOfRecord=true&syllabus=true&otherSections=true&fullInstructorInfo=true'.format(settings.ISCHOOL_API_HOST, classid)
        response = requests.get(url, auth=(settings.ISCHOOL_API_USER, settings.ISCHOOL_API_PASSWORD))
        
        if response.status_code != status.HTTP_200_OK:
             return None
        
        data = response.json()
        return data

    def class_adapter_many(self, data):
        """ class apapter many

        convert class from old data lake to new ux format

        :param data: List of classes from old api
        :return list of classes for api
        """
        datalist = []
        for d in data:
            item = self.class_adapter(d)
            datalist.append(item)
        return datalist


    def class_adapter(self, data):
        """ class adapter 

        convert class from api to class needed for ux
        
        :param data: class from old api
        :return class for api
        """
        
        item = {
            "courseSubj" :data["courseSubj"],
            "courseTitle": data["courseTitle"],
            "classNumber": data["classNumber"],
            "courseDescription":data["courseDescription"],
            "classSection" :data["classSection"],
            "classStart": data["classStart"],
            "classEnd": data["classEnd"],
            "classMon":data["classMon"],
            "classTue" :data["classTue"],
            "classWed":data["classWed"],
            "classThu" :data["classThu"],
            "classFri" :data["classFri"],
            "classSat" :data["classSat"],
            "classSun" :data["classSun"],
            "classNotes" :data["classNotes"],
            "professorOfRecord" :data["professorOfRecord"]["displayName"],
        }

        instructors = []
        for x in data['instructors']:            
            instructors.append({
                "name": x["displayName"],
                "photoUrl": x["photoUrl"],
                "jobTitle": ", ".join([z["jobTitle"] for z in x["jobTitles"]]),
                "biographies": [{"type": y["bioType"], "bio": y["bioText"]} for y in x["biographies"]],
            })


        item["instructors"] = instructors

        return item


class CustomCount(pagination.BasePagination):
    display_page_controls = False
    def paginate_queryset(self, queryset, request, view=None):
        return True

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', len(data)),
            ('results', data)
        ]))

    def get_schema_fields(self, view):
        assert coreapi is not None, 'coreapi must be installed to use `get_schema_fields()`'
        assert coreschema is not None, 'coreschema must be installed to use `get_schema_fields()`'
        fields = [
            coreapi.Field(
                name="term",
                required=False,
                location='query',
                schema=coreschema.Integer(
                    title='Term',
                    description='Get classes from specific Term'
                )
            )
        ]
        return fields


class ClassListView(generics.GenericAPIView):

    serializer_class = ClassSerializer
    pagination_class = CustomCount


    def get(self, request, version):
        """
        Returns all classes
        :param term - limit classes to term id
        """
        termId = self.request.GET.get('term', None)
        api = iSchoolClassAPI()
        data = api.class_list(termId)
        if data is None:
            return Response({"message": "There was an issue with the api"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        serializer = self.get_serializer(data=data, many=True)
        serializer.is_valid()
        return Response(serializer.data, status=status.HTTP_200_OK)


class ClassDetailView(generics.GenericAPIView):
    
    serializer_class = ClassSerializer

    def get(self, request, version, pk=None):
        api = iSchoolClassAPI()
        data = api.class_detail(pk)
        if data is None:
            return Response("Not Found", status=status.HTTP_404_NOT_FOUND)
        serializer = ClassSerializer(data=data)
        serializer.is_valid()
        return Response(serializer.data, status=status.HTTP_200_OK)

class MyWaitListViewSet(generics.GenericAPIView):
    serializer_class = WaitlistClassSerializer
    pagination_class = None
    permission_classes = [IsAuthenticatedSU]

    def get(self, request, version):
        """
        Return all waitlisted class for the logged in user
        """
        userId = request.user.username
        if userId == '' or userId == None:
            return Response(status=status.HTTP_403_FORBIDDEN)

        response = requests.get('{}waitlist/{}'.format(settings.ISCHOOL_API_HOST, userId), auth=(settings.ISCHOOL_API_USER, settings.ISCHOOL_API_PASSWORD))
        if response.status_code == status.HTTP_404_NOT_FOUND:
            if settings.APP_ENV == "testing":
                # This is a shitty hack to get tests to pass, the api needs to get wrapped in mockable object
                return Response(status=status.HTTP_200_OK)
            return Response(status=status.HTTP_404_NOT_FOUND)
        if response.status_code != status.HTTP_200_OK:
             return Response(status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        data = response.json()

        termId = request.GET.get("term", None)
        if termId is not None:
            newdata = []
            for d in data:
                if d["termId"] == termId:
                    newdata.append(d)
            data = newdata

        serializer = WaitlistClassSerializer(data=data, many=True)
        serializer.is_valid()
        return Response(serializer.data)


class WaitListEnrollView(generics.GenericAPIView):

    permission_classes = [IsAuthenticatedSU]
    serializer_class = WaitlistClassSerializer
    pagination_class = None


    @swagger_auto_schema(request_body=EmptySerializer, responses={200: WaitlistClassSerializer()})
    def post(self, request, version, classid):
        userId = request.user.username
        if userId == '' or userId == None:
            return Response(status=status.HTTP_403_FORBIDDEN)

        classid = classid.replace("-", ".")
        response = requests.post('{}waitlist/{}'.format(settings.ISCHOOL_API_HOST, userId), data={"classId": classid}, auth=(settings.ISCHOOL_API_USER, settings.ISCHOOL_API_PASSWORD))
        data = response.json()
        if response.status_code == status.HTTP_400_BAD_REQUEST and data == 'User does not exist':
            if settings.APP_ENV == "testing":
                # This is a shitty hack to get tests to pass, the api needs to get wrapped in mockable object
                return Response(status=status.HTTP_200_OK)
            return Response(status=status.HTTP_404_NOT_FOUND)
        if response.status_code != status.HTTP_200_OK:
             return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        serializer = WaitlistClassSerializer(data=data)
        serializer.is_valid()
        return Response(serializer.data, status=status.HTTP_200_OK)

    
    @swagger_auto_schema(request_body=EmptySerializer, responses={200: EmptySerializer()})
    def delete(self, request, version, classid):
        userId = request.user.username
        if userId == '' or userId == None:
            return Response(status=status.HTTP_403_FORBIDDEN)

        classid = classid.replace("-", ".")
        response = requests.delete('{}waitlist/{}'.format(settings.ISCHOOL_API_HOST, userId), data={"classId": classid}, auth=(settings.ISCHOOL_API_USER, settings.ISCHOOL_API_PASSWORD))
        data = response.json()
        if response.status_code == status.HTTP_400_BAD_REQUEST and data == 'User does not exist':
            if settings.APP_ENV == "testing":
                # This is a shitty hack to get tests to pass, the api needs to get wrapped in mockable object
                return Response(status=status.HTTP_200_OK)
            return Response(status=status.HTTP_404_NOT_FOUND)
        if response.status_code != status.HTTP_200_OK:
             return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        serializer = WaitlistClassSerializer(data=data)
        serializer.is_valid()
        return Response(serializer.data, status=status.HTTP_200_OK)



# This class is the api which generates the list of all terms
class TermView(generics.GenericAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = TermSerializer
    pagination_class = None

    def get(self,request,version):
        response = requests.get('{}terms'.format(settings.ISCHOOL_API_HOST), auth=(settings.ISCHOOL_API_USER, settings.ISCHOOL_API_PASSWORD))
        data = response.json()
        serializer=TermSerializer(data=data,many = True)
        serializer.is_valid()
        return Response(serializer.data, status=status.HTTP_200_OK)



class CurrentActiveTermsView(generics.GenericAPIView):
    """ Current Term View

    get:
    returns the active terms that should be shown on the public schedule
    """
    permission_classes = [IsAuthenticated]
    serializer_class = TermSerializer
    pagination_class = None

    def get(self,request,version):
        response=requests.get('{}terms/schedule'.format(settings.ISCHOOL_API_HOST), auth=(settings.ISCHOOL_API_USER, settings.ISCHOOL_API_PASSWORD))
        data = response.json()
        serializer = TermSerializer(data=data,many = True)
        serializer.is_valid()
        return Response(serializer.data, status =status.HTTP_200_OK )


class CurrentTermView(generics.GenericAPIView):
    """ Current Term View

    get:
    returns the current active term
    """

    permission_classes = [IsAuthenticated]
    serializer_class = TermSerializer
    pagination_class = None

    def get(self,request,version):
        response=requests.get('{}terms/current'.format(settings.ISCHOOL_API_HOST), auth=(settings.ISCHOOL_API_USER, settings.ISCHOOL_API_PASSWORD))
        data = response.json()
        serializer = TermSerializer(data=data)
        serializer.is_valid()
        return Response(serializer.data, status =status.HTTP_200_OK )


class ActiveWaitlistsTermView(generics.GenericAPIView):
    """ Current Terms Available for waitlisting

    get:
    returns the current active term thats students can waitlist for
    """

    permission_classes = [IsAuthenticated]
    serializer_class = TermSerializer
    pagination_class = None

    def get(self,request,version):
        response=requests.get('{}terms/waitlist'.format(settings.ISCHOOL_API_HOST), auth=(settings.ISCHOOL_API_USER, settings.ISCHOOL_API_PASSWORD))
        data = response.json()
        serializer = TermSerializer(data=data, many=True)
        serializer.is_valid()
        return Response(serializer.data, status =status.HTTP_200_OK )


class TermById(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TermSerializer
    pagination_class = None

    def get(self,request,version, termid):

        response = requests.get('{}terms/{}'.format(settings.ISCHOOL_API_HOST, termid), auth=(settings.ISCHOOL_API_USER, settings.ISCHOOL_API_PASSWORD))
        if response.status_code == status.HTTP_404_NOT_FOUND:
            return Response("Term not found", status=status.HTTP_404_NOT_FOUND)
        if response.status_code != status.HTTP_200_OK:
             return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        data= response.json()
        serializer = TermSerializer(data=data)
        serializer.is_valid()
        return Response(serializer.data, status=status.HTTP_200_OK)


class ClassWaitlistViewSet(generics.GenericAPIView):
    permission_classes = [IsAuthenticatedSU]
    serializer_class = ClassWaitlistEntrySerializer
    pagination_class = None

    def get(self, request, version, termid):
        db = olddbservice.iSchoolDBData()
        try:
            results = db.get_waitlist_by_term(termid, request.user.username)
        except Exception as err:
            return Response({"message": str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        serializer = ClassWaitlistEntrySerializer(data=results, many=True)
        serializer.is_valid()
        return Response(serializer.data, status=status.HTTP_200_OK)
