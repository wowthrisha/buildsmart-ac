from html.parser import HTMLParser

class DivTracker(HTMLParser):
    def __init__(self):
        super().__init__()
        self.div_stack = []
        self.issues = []

    def handle_starttag(self, tag, attrs):
        if tag == "div":
            self.div_stack.append(self.getpos()[0])

    def handle_endtag(self, tag):
        if tag == "div":
            if self.div_stack:
                self.div_stack.pop()
            else:
                self.issues.append(f"Extra closing div at line {self.getpos()[0]}")

tracker = DivTracker()
with open("app/templates/architect/project_workspace.html", "r") as f:
    tracker.feed(f.read())

if tracker.div_stack:
    print("Unclosed divisions started at lines:", tracker.div_stack)
if tracker.issues:
    print("Mismatched closing divisions:", tracker.issues)
