from rest_framework import serializers
from project.models import Project,Tag,Review
from users.models import Profile


class ProfileSerlizer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

class TagSerlizer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class ReviewSerlizer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class ProjectSerializers(serializers.ModelSerializer):
    owner = ProfileSerlizer(many = False)
    tags = TagSerlizer(many=True)
    reviews = serializers.SerializerMethodField()
    class Meta:
        model = Project
        fields = '__all__'

    def get_reviews(self,obj):
        reviews = obj.review_set.all()
        serializer = ReviewSerlizer(reviews,many = True)
        return serializer.data