from datetime import datetime

from django.db import models


class DirectoryBase(models.Model):
    """
    DirectoryBase Model extending by Directory adding a many versions of base directory
    """
    name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return f'{self.short_name} description: {self.description[:50]}'

    def last_version(self):
        return self.versions.first().version

    def current_directory(self):
        """
        :return: directory of current version
        """
        current_date = datetime.now()
        return self.versions.filter(start_date__lte=current_date).first()

    def current_version(self):
        return self.current_directory().version

    class Meta:
        verbose_name = 'Directory'
        verbose_name_plural = 'Directories'


class Directory(models.Model):
    """
    This Model extends DirectoryBase adding version system

    """
    version = models.CharField(max_length=100, blank=False)
    start_date = models.DateField()
    directory_base = models.ForeignKey(DirectoryBase, on_delete=models.CASCADE, related_name='versions')
    related_items = models.ManyToManyField('DirectoryItem')

    def __str__(self):
        return f'{self.directory_base.short_name}, ' \
               f'version {self.version}, start date is {self.start_date}'

    class Meta:
        verbose_name = 'Directory version'
        verbose_name_plural = 'Directories version'
        unique_together = [['version', 'directory_base'], ['start_date', 'directory_base']]

        ordering = ['-start_date']


class DirectoryItem(models.Model):
    """
    Directory Item
    we can store several items with the same code if their values differ
    """
    directories = models.ManyToManyField(Directory, blank=True)
    code = models.CharField(max_length=255, blank=False)
    value = models.CharField(max_length=255, blank=False)

    class Meta:
        verbose_name = 'Item'
        verbose_name_plural = 'Items'
        unique_together = ['code', 'value']

    def __str__(self):
        return f'code:{self.code}, value:{self.value}'
