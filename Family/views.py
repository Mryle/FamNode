from django.shortcuts import render
from django.db.models import Q
from django.views import generic
from Family import models

# Create your views here.

class PersonSimpleList(generic.ListView):
    model = models.Person
    template_name = 'Person/person_list.html'

def create_hierarchical_view(nodes, edges):
    def walk_edge(node, edge):
        object = node['object']
        level_mod = edge.type == 'Child' ? 1 : 0
        if edge.person1 == object:
            return {'object': edge.person2, 'level': node['level'] + level_mod}
        else if edge.person2 == object:
            return {'object': edge.person1, 'level': node['level'] - level_mod}
        else:
            return None
    def walk_dfs(nnodes, node):
        for edge in edges:
            next = walk_edge(node, edge)
            id = next['object'].id
            if next is not None and nnodes[next['object'].id]['level'] is not None:
                nnodes[id] = next
                walk_dfs(nnodes, next)
    if len(nodes) == 0:
        return []
    nnodes = { (n.id, { 'object': n, 'level': None }) for n in nodes}
    node = {'object': nodes[0], 'level': 0}
    walk_dfs(nnodes, node)
    return [ node for (id, node) in nnodes]


class PersonTree(generic.ListView):
    model = models.Person
    template_name = 'Person/person_tree.html'
    
    def get_context_data(self, **kwargs):
        context = super(PersonTree, self).get_context_data(**kwargs)
        context['edge_list'] = models.Relation.objects.all()
        return context
        
class PersonDetails(generic.DetailView):
    model = models.Person
    template_name = 'Person/person_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super(PersonDetails, self).get_context_data(**kwargs)
        context['rel_list'] = models.Relation.objects.filter(Q(person1 = self.object) | Q(person2 = self.object))
        context['text_list'] = models.InformationText.objects.filter(person = self.object)
        return context