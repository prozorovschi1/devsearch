from rest_framework import serializers
from projects.models import Project, Tag, Review
from users.models import Profile

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class ProjectSerializer(serializers.ModelSerializer):
    owner = ProfileSerializer(many=False)  # Relație One-to-One sau ForeignKey
    tags = TagSerializer(many=True)       # Relație Many-to-Many
    reviews = serializers.SerializerMethodField()  # Câmp personalizat pentru reviews

    class Meta:
        model = Project
        fields = '__all__'

    def get_reviews(self, obj):
        reviews = obj.review_set.all()  # Accesează toate obiectele Review asociate cu proiectul
        serializer = ReviewSerializer(reviews, many=True)
        return serializer.data
