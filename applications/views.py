from django.shortcuts import render
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from config.utils import check_email_subscription
from .tasks import application_approval_email, application_refusal_email
# 뷰를 어떻게 작성할지는 url 설계 생각하면서도 바뀔 수 있구나

# 지원자가
# TeamApplication 생성 -- 신청 api
# 지원 수정 api -- 도 가능하게 !
# 지원 취소 api

# 팀 생성자가
# 지원자를 승인/거절 api
# approve refuse
from rest_framework import viewsets, status

from applications.models import TeamApplication
from applications.permissions import IsTeamLeader, IsApplicationTeamLeader
from applications.serializers import TeamApplicationSerializer


class TeamApplicationViewSet(viewsets.GenericViewSet):
    queryset = TeamApplication.objects.all()
    serializer_class = TeamApplicationSerializer
    permission_classes = [IsAuthenticated, IsApplicationTeamLeader]

    # 승인/거절 api  # 팀 리더
    ''' 팀 리더가 신청 승인 :: GET http://127.0.0.1:8000/applications/{application_pk}/approve/ '''

    @action(methods=['get'], detail=True, url_path='approve',
            url_name='approve_application')
    def approve_application(self, request, *args, **kwargs):
        # pk 가 TeamApplication 거니까
        # 객체 가져와서 상태만 변경하면 되겠지 ?

        # try:
        application = self.get_object()  # not found ? -- TODO 에러잡기
        # print(application)
        # except:
        #     return Response({"message": "not found."}, status=status.HTTP_404_NOT_FOUND)
        # not found + permission 에러 각각 못잡는다

        if application.join_status == TeamApplication.WAITING:
            application.join_status = TeamApplication.APPROVED
            application.save()
            # print(application)
            # serializer = self.get_serializer(application)
            # print(serializer.data)

            does_subscribe_to_email, email = check_email_subscription(application.applicant)
            if does_subscribe_to_email:
                application_approval_email.delay(email)  # 회원에게 신청 승인 메일

            return Response({"message": "ok"}, status=status.HTTP_200_OK)
        return Response({"message": "Application Status Error."}, status=status.HTTP_400_BAD_REQUEST)

    ''' 팀리더가 신청 거부 :: GET http://127.0.0.1:8000/applications/{application_pk}/refuse/ '''

    @action(methods=['get'], detail=True, url_path='refuse',
            url_name='refuse_application')
    def refuse_application(self, request, *args, **kwargs):
        application = self.get_object()

        if application.join_status == TeamApplication.WAITING:
            application.join_status = TeamApplication.REJECTED
            application.save()

            # serializer = self.get_serializer(application)
            # print(serializer.data)

            does_subscribe_to_email, email = check_email_subscription(application.applicant)
            if does_subscribe_to_email:
                application_refusal_email.delay(email)  # 회원에게 신청 거부 메일

            return Response({"message": "ok"}, status=status.HTTP_200_OK)
        return Response({"message": "Application Status Error."}, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def get_questions(request):
#
#     ''' response format -- 피드백받기
#     :return:
#     {
#         "questions" : serializer.data
#     }
#     '''
#     pass
