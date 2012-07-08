import re

class rpath:
    winPathRegex = '[a-zA-Z]:\\\\'

    def __init__(self, core):
        self.separator = core['SERVER']['separator']
        self.home      = core['SERVER']['home']
        self.cwd       = core['ENV']['CWD']

    def _sanitize(self, path):
        info = self._split(path)
        result = []
        elems = info['elems']
        for x in elems:
            if x in ['.','']:
                pass
            elif x == '..':
                result = result[:-1]
            elif x == '~':
                info = self._split(self.home)
                result = info['elems']
            else:
                result.append(x)
        return(info['root']+info['slash'].join(result))

    def _getabs(self, path):
        if self.isabs(path): return(path)
        return(self.abspath(path))

    def _split(self, path):
        path = self._getabs(path)
        # if linux
        if path.startswith('/'):
            platform = 'nix'
            root     = '/'
            slash    = '/'
        # if win physical path (C:\)
        elif re.match(self.winPathRegex,path):
            platform = 'win'
            root     = path[:3]
            slash    = '\\'
        # if win network path (\\1.1.1.1)
        elif path.startswith('\\'):
            platform = 'win'
            root     = '\\\\'
            slash    = '\\'
            path     = root+path.lstrip('\\')
        else:
            print 'unknow path ID on rpath.py !!!'
        dirname  = slash.join(path.split(slash)[:-1])+slash
        basename = path.split(slash)[-1]
        elems = path[len(root):].split(slash)
        result = {'platform' : platform,
                  'root'     : root,
                  'elems'    : elems,
                  'slash'    : slash,
                  'dirname'  : dirname,
                  'basename' : basename}
        return(result)


    def isabs(self, path):
        if path.startswith('/') or re.match(self.winPathRegex,path) or path.startswith('\\'):
            return(True)
        return(False)

    def abspath(self, path):
        if not self.isabs(path):
            slash = '/'
            if not '/' in path and '\\' in path:
                slash = '\\'
            elems = path.split(slash)
            oldPath = self._split(self.cwd)
            path = oldPath['root']+oldPath['slash'].join(oldPath['elems']+elems)
        return(self._sanitize(path))

    def dirname(self, path):
        return(self._split(path)['dirname'])

    def basename(self, path):
        return(self._split(path)['basename'])

    def rootdir(self, path):
        return(self._split(path)['root'])
