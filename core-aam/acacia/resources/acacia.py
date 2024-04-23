import acacia_atspi
import json
from ua_parser import user_agent_parser

def main(request, response):
    # First get the browser from the UA string

    ua_string = request.headers.get("User-Agent").decode("utf-8");
    ua = user_agent_parser.ParseUserAgent(ua_string)
    ua_family = ua["family"];

    root = acacia_atspi.findRootAtspiNodeForName(ua_family)

    if root.isNull():
      print("Cannot find root accessibility node for %s - did you turn on accessibility?"
            % ua_family);
      return (200, 'could not find %s' % ua_family), [('Content-Type', 'foo/bar')], 'no data'
    test_url = request.GET[b'test_url'].decode('UTF-8')
    tab = find_tab(root, test_url)
    if not tab:
      print('Cannot find document for %s'
            % test_url);
      return (200, 'could not find %s' % test_url), [('Content-Type', 'foo/bar')], 'no data'

    test_id = request.GET[b'id'].decode('UTF-8')
    node = find_node(tab, test_id)
    if not node:
        print('Cannot find node for %s' % test_id)
        return (200, 'could not find %s' % test_id), [('Content-Type', 'foo/bar')], 'no data'

    node_dictionary = {}
    node_dictionary['role'] = node.getRoleName()
    node_dictionary['name'] = node.getName()
    node_dictionary['description'] = node.getDescription()
    node_dictionary['states'] = sorted(node.getStates())
    node_dictionary['interfaces'] = sorted(node.getInterfaces())
    node_dictionary['attributes'] = sorted(node.getAttributes())

    return ((200, 'Found'), [('Content-Type', 'text/json')], json.dumps(node_dictionary))

def find_tab(root, test_url):
    stack = [root]
    while stack:
        node = stack.pop()

        if node.getRoleName() == 'document web':
            document = node.queryDocument()
            if document.isNull():
                continue
            attributes = document.getDocumentAttributes()
            for attribute_pair in attributes:
                [attribute, value] = attribute_pair.split(':', 1)
                if attribute == 'DocURL':
                    if value == test_url:
                        return node
            # Don't continue traversing into documents
            continue

        for i in range(node.getChildCount()):
            child = node.getChildAtIndex(i)
            stack.append(child)

    return None


def find_node(tab, test_id):
    stack = [tab]
    while stack:
        node = stack.pop()

        attributes = node.getAttributes()
        for attribute_pair in attributes:
            [attribute, value] = attribute_pair.split(':', 1)
            if attribute == 'id':
                if value == test_id:
                    return node

        for i in range(node.getChildCount()):
            child = node.getChildAtIndex(i)
            stack.append(child)

    return None
