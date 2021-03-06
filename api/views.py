from django.shortcuts import get_object_or_404
from core.models import User, Trip, Contact, Log, Comment, Image
from .serializers import ContactSerializer, ImageSerializer, LogCommentImageSerializer, LogCommentSerializer, UserSerializer, TripSerializer, LogSerializer, TripLogSerializer, CommentSerializer
from rest_framework.generics import ListCreateAPIView, CreateAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.conf import settings
from django.core.mail import send_mail
from django.utils.timezone import now
from django.template.loader import render_to_string
from rest_framework.parsers import FileUploadParser, JSONParser




# custom login for the front end to get userpk when logging in [POST]
class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'username': user.username,
            'last_login': user.last_login,
            'email': user.email,
            'bio': user.bio
        })



# Profile page [GET]
class UserProfileView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user



# Create a new trip with [POST], List of all trips [GET]
class TripListView(ListCreateAPIView):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)



# Specific user and their trips [GET]
class UserTripsView(ListCreateAPIView):
    serializer_class = TripSerializer

    def get_queryset(self):
        return self.request.user.trips.all()



# Log an entry on a trip [POST]
class TripLogView(CreateAPIView):
    serializer_class = LogSerializer
    queryset = Trip.objects.all()

    def get_queryset(self):
        return self.request.user.trips.all()


    def perform_create(self, serializer):
        trip = get_object_or_404(Trip, pk=self.kwargs["trip_pk"])
        serializer.save(user=self.request.user, trip=trip)
        log_entry = serializer.instance # grab the serializer to reference it in the HTML formatted email
        self.mail_trip_subscribers(log_entry)


    def mail_trip_subscribers(self, log_entry):
        contact_list = Contact.objects.all()
        
        email_list = []
        for contact in contact_list:
            
            email_list.append(contact.email)
            send_mail( 
                'Someone you know is checking in',
                'Body', 
                settings.EMAIL_HOST_USER,
                email_list,
                html_message = render_to_string('mail/log.html', {'greeting': 'just checking in...'})
            )



# Trips with associated logs [GET]
class TripDetailView(RetrieveAPIView):
    queryset = Trip.objects.all()
    serializer_class = TripLogSerializer



# Log detail page [GET]
class LogDetailView(RetrieveAPIView):
    queryset = Log.objects.all()
    serializer_class = LogCommentSerializer



# Comment on a log [POST]
class CommentView(ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        log = get_object_or_404(Log, pk=self.kwargs["pk"])
        serializer.save(user=self.request.user, log=log)



# Upload pictures to S3 [POST]
class PictureUploadView(ListCreateAPIView):
    parser_classes = [FileUploadParser, JSONParser]
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

    def perform_create(self, serializer):
        if 'file' in self.request.data:
            log = get_object_or_404(Log, pk=self.kwargs['pk'])
            serializer.save(picture=self.request.data['file'], user=self.request.user, log=log)




# Current active trip for logged in user [GET]
class CurrentActiveView(ListCreateAPIView):
    queryset = Trip.objects.all()
    serializer_class = TripLogSerializer

    def get_queryset(self):
        user = self.request.user
        return Trip.objects.filter(end__gt=now().date(), begin__lte=now().date(), user=user)



# Future trips for a logged in user [GET]
class FutureActiveView(ListCreateAPIView):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer

    def get_queryset(self):
        user = self.request.user
        return Trip.objects.filter(begin__gte=now().date(), user=user)



# Past trips for a logged in user [GET]
class PastActiveView(ListCreateAPIView):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer

    def get_queryset(self):
        user = self.request.user
        return Trip.objects.filter(end__lte=now().date(), user=user)



# Add/Delete/View contacts for a User
class UserContactView(ListCreateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer



# View Trips logged in User is subscribed to
class UserSubView(ListCreateAPIView):
    serializer_class = TripSerializer
    queryset = Trip.objects.all()
    
    def get_queryset(self):
        user_email = self.request.user.email
        contact = Contact.objects.get(email=user_email)
        return contact.trip_subscribers.all()



# View current trips logged in user is subscribed to
class UserCurrentSubView(ListCreateAPIView):
    serializer_class = TripSerializer
    queryset = Trip.objects.all()

    def get_queryset(self):
        user_email = self.request.user.email
        contact= Contact.objects.get(email=user_email)        
        return contact.trip_subscribers.filter(end__gt=now().date(), begin__lte=now().date())



# View past trips logged in user is subscribed to
class UserPastSubView(ListCreateAPIView):
    serializer_class = TripSerializer
    queryset = Trip.objects.all()

    def get_queryset(self):
        user_email = self.request.user.email
        contact= Contact.objects.get(email=user_email)
        return contact.trip_subscribers.filter(end__lte=now().date())



# View future trips logged in user is subscribed to
class UserFutureSubView(ListCreateAPIView):
    serializer_class = TripSerializer
    queryset = Trip.objects.all()

    def get_queryset(self):
        user_email = self.request.user.email
        contact= Contact.objects.get(email=user_email)
        return contact.trip_subscribers.filter(begin__gte=now().date())



# View log detail
class LogCommentImageView(RetrieveAPIView):
    serializer_class = LogCommentImageSerializer
    queryset = Log.objects.all()

