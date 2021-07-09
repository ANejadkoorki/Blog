from . import models

# Object manager
# CRUDF : Create/Read/Update/Delete/Filter

x = models.Post.objects.all()  # all of the rows
y = models.Post.objects.create()  # create single record
k = models.Post.objects.get(pk=3)  # get a single record with pk or another unique attributes
z = models.Post.objects.get().delete()  # get and delete a single record
d = models.Post.objects.filter()  # filter

# to update a row we will do this  :
row = models.Post.objects.get(pk=1)
row.title = 'hello world'  # for example changing the title
row.save()

# to update a group of rows for example first 3 rows
rows = models.Post.objects.all()[:3]
rows.update(title='new title').save()
rows.delete()  # to delete this 3 rows



