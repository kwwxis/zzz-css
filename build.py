import os.path
import shutil
import glob
import time
import datetime
from csscompressor import compress
import rcssmin

# -------------- FILE NAME ------------ PURPOSE --------------
               
order       = [ 'etc.css',
                'header.css',
                'sidebar.css',
                'layout.css',
                'thing.css',
                'comments.css',
                'cpage.css',
                'usertext.css',
                'flair.css',
                'search.css',
                'submit.css',
                'wiki.css',
                'footer.css',
                'nightmode.css',
              ]      
                
# input/output variables
src_dir     = 'src'
dist_dir    = './'
dist_file   = 'dist.css'
unmin_file  = 'unmin.css'

def top(build_ver):
    return ('/* Stylesheet for /r/ZenlessZoneZero by /u/kwwxis; build #' + str(build_ver) + ' */')

def run():
    with open(r'build.dat','r+') as build:
        build_ver = int(build.read()) + 1
        print('\nBUILD #' + str(build_ver))
        
        if not os.path.isdir(src_dir):
            print('\nFailed: the source directory, "' + src_dir + '" was not found')
            return
            
        # Combine files in specified order
        with open(dist_dir + '\\' + dist_file, 'wb') as outfile:
            for src_file in order:
                path = src_dir + '\\' + src_file
                
                if os.path.isfile(path):
                    with open(path, 'rb') as readfile:
                        shutil.copyfileobj(readfile, outfile)
                        print('  + ' + path)
                else:
                    print('\nFailed: target file not found: ' + path + ';\n' +
                    'if this file is no longer in use then you must remove it from the "order" variable in build.py')
                    return
        
        # copy an unminified version of the stylesheet to a separate file
        shutil.copyfile(dist_dir + '\\' + dist_file, dist_dir + '\\' + unmin_file);
        
        # Compress
        with open(dist_dir + '\\' + dist_file, 'r+') as outfile:
            raw  = outfile.read()
            #mini = compress(raw)
            mini = rcssmin.cssmin(raw)
            outfile.seek(0)
            outfile.write(top(build_ver) + '\n' + mini)
            outfile.truncate()
            
        # Increment build version in build.dat afterwards in case of failure
        build.seek(0)
        build.write(str(build_ver))
        
        print('\nDone!')

if __name__ == '__main__':
    run()