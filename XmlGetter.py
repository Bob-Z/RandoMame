import subprocess
import xml.etree.ElementTree as ElementTree


def load_string():
    print("Reading MAME's XML data")
    out = subprocess.Popen(['/media/4To/emu/mame/mame/mame64', '-listxml'],
                           stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT)

    return out.communicate()


def get():
    stdout, stderr = load_string()
    print("Parsing MAME's XML data")

    target = XmlFilter()
    parser = ElementTree.XMLParser(target=target)

    return ElementTree.fromstring(stdout, parser=parser)


class XmlFilter:
    skip = False
    defaultBuilder = ElementTree.TreeBuilder()

    def start(self, tag, attrib):  # Called for each opening tag.
        if tag == "rom":
            self.skip = True
            pass
        elif tag == "device_ref":
            self.skip = True
            pass
        elif tag == "chip":
            self.skip = True
            pass
        elif tag == "display":
            self.skip = True
            pass
        elif tag == "sound":
            self.skip = True
            pass
        elif tag == "dipswitch":
            self.skip = True
            pass
        elif tag == "port":
            self.skip = True
            pass
        elif tag == "biosset":
            self.skip = True
            pass
        else:
            return self.defaultBuilder.start(tag, attrib)

    def end(self, tag):  # Called for each closing tag.
        if self.skip is False:
            return self.defaultBuilder.end(tag)
        else:
            self.skip = False

    def data(self, data):
        if self.skip:
            pass
        else:
            return self.defaultBuilder.data(data)

    def close(self):  # Called when all data has been parsed.
        print("close")
        return self.defaultBuilder.close()
