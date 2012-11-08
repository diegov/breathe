def _wrap(f):
    def _new_f(self):
        from docutils import nodes

        if not hasattr(self, 'data_object'):
            return f(self)

        if not hasattr(self.data_object, 'get_refid'):
            return f(self)

        refid = str(self.data_object.get_refid())
        url = self.project_info.url() + refid + '.html'
        if hasattr(self.data_object, 'get_name'):
            name = self.data_object.get_name()
        else:
            name = refid

        link = nodes.reference('', name, 
                               internal=False, refuri=url, reftitle=refid)
        p = nodes.paragraph()
        p.append(link)

        return [p]

    return _new_f

class RenderHijackerMetaClass(type):
    def __new__(cls, clazz_name, parents, attributes):

        print 'Creating ' + clazz_name

        if 'render' in attributes:        
            attributes['render'] = _wrap(attributes['render'])

        return super(RenderHijackerMetaClass, cls).__new__(cls, clazz_name, parents, attributes)

class Renderer(object):
    __metaclass__ = RenderHijackerMetaClass

    def __init__(self,
            project_info,
            data_object,
            renderer_factory,
            node_factory,
            state,
            document,
            domain_handler,
            target_handler
            ):

        self.project_info = project_info
        self.data_object = data_object
        self.renderer_factory = renderer_factory
        self.node_factory = node_factory
        self.state = state
        self.document = document
        self.domain_handler = domain_handler
        self.target_handler = target_handler


