from django.shortcuts import render
from django.db.models import Q
from django.views import generic
from Family import models
import queue

# Create your views here.

# class PersonSimpleList(generic.ListView):
    # model = models.FamilyNode
    # template_name = 'Person/person_list.html'

# def create_hierarchical_view(nodes, edges):
    # def repack_object(object, nid, level):
        # return {"title": object.title, "id": nid, "level": level}
    # def repack_edge(edge, nnodes):
        # return {"node1": nnodes[edge.person1.id]['number'], "node2": nnodes[edge.person2.id]['number']}
    # # def walk_edge(node, edge, number):
        # # object = node['object']
        # # if edge.person1 == object:
            # # number += 1
            # # return ({'object': edge.person2, 'number': number}, number)
        # # elif edge.person2 == object:
            # # number += 1
            # # return ({'object': edge.person1, 'number': number}, number)
        # # else:
            # # return (None, number)
    # def walk_edge(node, nnodes, edge, number):
        # object = node['object']
        # if edge.person1 == object and nnodes[edge.person2.id]['number'] is None:
            # return {'object': edge.person2, 'level': node['level'] + 1}
        # elif edge.person2 == object and nnodes[edge.person1.id]['number'] is None:
            # return {'object': edge.person1, 'level': node['level'] - 1}
        # else:
            # return None
    # # def walk_dfs(nnodes, node, number):
        # # id = node['object'].id
        # # if nnodes[id]['number'] is None:
            # # print(node['object'].title)
            # # nnodes[id] = node
            # # for edge in edges:
                # # next, number = walk_edge(node, edge, number)
                # # if next is not None:
                    # # number = walk_dfs(nnodes, next, number)
    # def walk_bfs(nnodes, nodeQueue, number):
        # while not nodeQueue.empty():
            # node = nodeQueue.get()
            # id = node['object'].id
            # if nnodes[id]['number'] is None:
                # print(node['object'].title)
                # node['number'] = number
                # number += 1
                # nnodes[id] = node
                # for edge in edges:
                    # next = walk_edge(node, nnodes, edge, number)
                    # if next is not None:
                        # nodeQueue.put(next)
        # return number

    # if len(nodes) == 0:
        # return []
    # nnodes = { n.id: { 'object': n, 'number': None } for n in nodes}
    # nodeQueue = queue.LifoQueue()
    # nodeQueue.put({'object': nodes[0], 'level': 0})
    # mnum = walk_bfs(nnodes, nodeQueue, 0)
    # sorted = { nnodes[id]['number']: repack_object(nnodes[id]['object'],nnodes[id]['number'],nnodes[id]['level']) for id in nnodes}
    # return [ sorted[num] for num in range(mnum)], [ repack_edge(edge, nnodes) for edge in edges]

# class PersonTree(generic.ListView):
    # model = models.FamilyNode
    # template_name = 'Person/person_tree.html'
    
    # def get_context_data(self, **kwargs):
        # context = super(PersonTree, self).get_context_data(**kwargs)
        # nodes, edges = create_hierarchical_view(context['object_list'], models.Relation.objects.all())
        # context['object_list'] = nodes
        # context['edge_list'] = edges
        # return context
        
# class PersonGraph(generic.ListView):
    # model = models.FamilyNode
    # template_name = 'Person/person_graph.html'
    
    # def get_context_data(self, **kwargs):
        # context = super(PersonGraph, self).get_context_data(**kwargs)
        # nodes, edges = create_hierarchical_view(context['object_list'], models.Relation.objects.all())
        # context['object_list'] = nodes
        # context['edge_list'] = edges
        # return context
        
# class PersonDetails(generic.DetailView):
    # model = models.FamilyNode
    # template_name = 'Person/person_detail.html'
    
    # def get_context_data(self, **kwargs):
        # context = super(PersonDetails, self).get_context_data(**kwargs)
        # context['rel_list'] = models.Relation.objects.filter(Q(person1 = self.object) | Q(person2 = self.object))
        # context['text_list'] = models.InformationText.objects.filter(person = self.object)
        # return context
        
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