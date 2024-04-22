import acacia_atspi
from ua_parser import user_agent_parser

def main(request, response):

    # First get the browser from the UA string

    ua_string = request.headers.get("User-Agent").decode("utf-8");
    ua = user_agent_parser.ParseUserAgent(ua_string)
    ua_family = ua["family"];

    print("Searching for browser with name %s" % ua_family)
    root = acacia_atspi.findRootAtspiNodeForName(ua_family)

    if root.isNull():
      print("Cannot find root accessibility node for %s - did you turn on accessibility?"
            % ua_family);
      return (200, 'could not find %s' % ua_family), [('Content-Type', 'foo/bar')], 'no data'

    print("Found!!");
    return (200, 'Found'), [('Content-Type', 'foo/bar')], 'test data'
