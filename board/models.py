from django.db import models

# Create your models here.
from django.db.models import Max

from user.models import User


class Board(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField(blank=False, null=False)
    hit = models.IntegerField(default=0)
    reg_date = models.DateTimeField(auto_now=True)
    group_no = models.IntegerField(default=0)
    order_no = models.IntegerField(default=1)
    depth = models.IntegerField(default=0)
    userid = models.ForeignKey(User,on_delete=models.CASCADE,to_field='id')

    class Meta:
        managed = True
        db_table = 'board'

    def __str__(self):
        return "Board(%s,%s,%s,%s,%s,%s,%s,%s)"\
               %(self.title,self.content,self.hit,self.reg_date,
                 self.group_no,self.order_no,self.depth,self.userid)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.group_no == 0:
            max_group_no = Board.objects.aggregate(Max('group_no'))
            self.group_no = max_group_no['group_no__max'] + 1

        super(Board, self).save()
