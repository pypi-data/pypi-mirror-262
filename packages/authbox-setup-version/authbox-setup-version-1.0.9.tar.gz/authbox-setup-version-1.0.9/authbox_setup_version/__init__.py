'''
    Must have variable
        > __version__ = Version("menu", 1, 0, 31)
        
    Or just install incremental to auto create this variable
        > pip install incremental
        
    Date Create:
        2023-03-06
'''

from os.path import abspath, dirname, join
import os
import codecs

def _read_file(rel_path):
    '''
        private function (not for call from outside)
        read version file (example: menu/_version.py)
    '''
    import os
    #here = abspath(dirname(__file__))
    #print('File Path = ' , join(here, rel_path))
    print('current dir = ', os.getcwd())
    here = os.getcwd()
    with codecs.open(join(here, rel_path), 'r') as fp:
        tmp =  fp.read()         
        return tmp

def get_version(rel_path):
    '''
        public function        
        example in setup.py: get_version('menu/_version.py')
        must have variable __version__ in _version.py
    '''        
    # print('rel_path = ', rel_path)
    for line in _read_file(rel_path).splitlines():        
        # print('line = ', line)
        if line.startswith('__version__'):            
            delim = line[line.find("(")+1:line.find(")")]            
            
            # clear space through array of string
            i = 0
            tmp = ""
            while i < len(delim):
                tmp += str(delim[i]).strip()
                i += 1
            
            delim_split = tmp.split(',')
            
            # variable __version__ contain: Version("menu", 1, 0, 31)
            # remove "menu"
            delim_split.pop(0)            
            
            # join string
            return ".".join(delim_split)                        
    else:
        raise RuntimeError("Unable to find version string.")

def increment_version(rel_path, package_name, major=0, minor=0, micro=1):
    '''
        # 0 dan 1 di parameter adalah penanda true false, buka jumalah increment nya
        Run this to increment version
    '''
    m_version = get_version(rel_path)
    m_array_str = m_version.split('.')
    m_array_int = []
    for i in m_array_str:
        m_array_int.append(int(i))
        
    # if major ada data maka abaikan option lain
    # else minor ada data, maka abaikan yg lain
    # else, increment micro
        
    if len(m_array_int) >= 3:
        if major > 0:
            m_array_int[0] += 1
        elif minor > 0:
            m_array_int[1] += 1
        else:
            m_array_int[2] += 1
        
    ret = ""
    for i in m_array_int:
        if ret: ret += "."
        ret += str(i)
        
    if ret:
        cmd = f"python -m incremental.update {package_name} --newversion={ret}"
        returned_value = os.system(cmd) 
        # print(returned_value)
        
    return ret
    
