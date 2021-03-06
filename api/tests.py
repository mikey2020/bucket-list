from django.test import TestCase
from .models import BucketList
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User

# Create your tests here.
class BucketListTestCase(TestCase):
    """ This defines test suite for the bucket list model """

    def setUp(self):
        user = User.objects.create(username="asta")
        self.bucketlist = BucketList(name="test", owner=user)

    def test_can_create_bucketlist(self):
        old_count = BucketList.objects.count()
        self.bucketlist.save()
        new_count = BucketList.objects.count()
        self.assertEqual(old_count,0)
        self.assertEqual(new_count,1)
        self.assertGreater(new_count,old_count)


class ViewTestCase(TestCase):
    """ Test for api views """

    def setUp(self):
        user = User.objects.create(username="richard")
        self.client = APIClient()
        self.client.force_authenticate(user=user)
        self.bucketlist_data = {'name': 'the king', 'owner': user.id}
        self.response = self.client.post(
            reverse('create'),
            self.bucketlist_data,
            format="json"
        )

    def test_authorization_is_enforced(self):
        """Test that the api has user authorization."""
        new_client = APIClient()
        res = new_client.get('/bucketlists/', kwargs={'pk': 3}, format="json")
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_api_can_create_bucketlist(self):
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_api_can_get_bucketlist(self):
        bucket_list = BucketList.objects.get(id=1)
        response = self.client.get(
            reverse('details', kwargs={'pk': bucket_list.id }),
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, bucket_list)

    def test_api_can_update_bucketlist(self):
        bucket_list = BucketList.objects.get()
        change_bucketlist = {'name': 'Something new'}
        res = self.client.put(
            reverse('details', kwargs={'pk': bucket_list.id}),
            change_bucketlist,
            format="json"
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_api_can_delete_bucketlist(self):
        bucket_list = BucketList.objects.get()
        response = self.client.delete(
            reverse('details', kwargs={'pk': bucket_list.id}),
            format="json",
            follow=True
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)



    
