from django.db import models

class DATASET_NLP(models.Model):
    conversation_id = models.IntegerField()
    question = models.CharField(max_length=3000)
    question_intent = models.CharField(max_length=3000)
    question_ner = models.CharField(max_length=300)

    def __str__(self):
        # return "{}".format(self.question,)
        return self.question

class DATASET_ANSWER(models.Model):
    conversation_id = models.IntegerField()
    answer = models.CharField(max_length=3000)
    answer_intent = models.CharField(max_length=3000)
    answer_ner = models.CharField(max_length=200)
    question_ner = models.CharField(max_length=300, default='')

    def __str__(self):
        return "{}".format(self.answer)