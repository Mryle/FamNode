from django.shortcuts import render
from django.db.models import Q
from django.views import generic
from Family import models
import queue

class SinglePage(generic.ListView):
    model = models.FamilyNode
    template_name = 'Technical/single_page.html'
    def repackPersonId(self):
        it = 1
        dic = dict(self.request.GET)
        ret = {}
        for key in dic:
            if key.startswith('person.') and dic[key][0] == 'true':
                ret[int(key[7:])] = it
                it += 1
        return ret
    def filterContext(self, context):
        def repackPerson(object, newId):
            object.id = newId
            return object
        def repackEdge(object, renameDict):
            object.person1.id = renameDict[object.person1.id]
            object.person2.id = renameDict[object.person2.id]
            return object
        renameDict = self.repackPersonId()
        if renameDict.keys():
            context['object_list'] = [repackPerson(x, renameDict[x.id]) for x in context['object_list'] if x.id in renameDict]
            context['edge_list'] = [repackEdge(x, renameDict) for x in context['edge_list'] if x.person1.id in renameDict and x.person2.id in renameDict]
    def get_context_data(self, **kwargs):
        print(self.repackPersonId())
        context = super(SinglePage, self).get_context_data(**kwargs)
        context['edge_list'] = models.Relation.objects.all()
        context['text_list'] = models.InformationText.objects.all()
        self.filterContext(context)
        return context
    def post(self, **kwargs):
        return self.get(kwargs)
        
class DevPage(generic.ListView):
    model = models.FamilyNode
    template_name = 'Technical/dev_page.html'
    
    def get_context_data(self, **kwargs):
        context = super(DevPage, self).get_context_data(**kwargs)
        context['edge_list'] = models.Relation.objects.all()
        context['text_list'] = models.InformationText.objects.all()
        #nodes, edges = create_hierarchical_view(context['object_list'], models.Relation.objects.all())
        #context['object_list'] = nodes
        #context['edge_list'] = edges
        return context