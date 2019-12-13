from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
# from django.core.urlresolvers import reverse
from blackboard.models import DATASET_ANSWER, DATASET_NLP

class ModelTestCase(TestCase):
   # """This class defines the test suite for the model."""

    def setUp(self):
      #  """Define the test client and other test variables."""
      self.ds_nlp_name =  "Write questions"
      self.ds_answer_name = "Write answers"
      self.ds_nlp = DATASET_NLP(question=self.ds_nlp_name)
      self.ds_answer = DATASET_ANSWER(answer=self.ds_answer_name) 

    def test_model_can_create_a_dataset(self):
    #"""Test the bucketlist model can create a bucketlist."""
      old_counta = DATASET_NLP.objects.count()
      old_countb = DATASET_ANSWER.objects.count()
      self.ds_nlp.save()
      self.ds_answer.save()
      new_counta = DATASET_NLP.objects.count()
      new_countb = DATASET_ANSWER.objects.count()
      self.assertNotEqual(old_counta, new_counta)



