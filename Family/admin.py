from django.contrib import admin
from Family import models
# Register your models here.

class InformationInline(admin.StackedInline):
    model = models.InformationText

@admin.register(models.FamilyNode)
class NodeAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'stDate', 'enDate')
    list_editable = ('stDate', 'enDate')
    pass
    #inlines = [InformationInline]

@admin.register(models.Relation)
class RelationAdmin(admin.ModelAdmin):
    pass

@admin.register(models.InformationText)	
class InformationTextAdmin(admin.ModelAdmin):
	pass