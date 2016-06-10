import os.path
import tempfile
import subprocess
import shutil
from git.repo.base import Repo

class GitModule(object):
    
    def __init__(self , **kwargs):
        url = kwargs.get("url")
        local_path = kwargs.get("local_path")

        if url is None and local_path is None:
            raise ValueError("Must supply one of url and local_path")
            
        if url and local_path:
            raise ValueError("Can only supply one of url and local_path")
            
        if url:
            local_path = tempfile.mkdtemp( )
            self.repo = Repo.clone_from( url , local_path )
        else:
            self.repo = Repo( local_path )
            origin = self.repo.remote( name = "origin")
            origin.fetch( )
    

    def getRoot(self):
        return self.repo.working_tree_dir

    def relPath(self , path):
        if path.startswith( self.getRoot( ) ):
            N = len(self.getRoot()) + 1
            return path[N:]
        else:
            raise IOError("Not part of repo:%s ?!" % path)


    def absPath(self , path):
        repo_path = os.path.join( self.getRoot() , path)
        if os.path.exists( repo_path ):
            return repo_path
        else:
            raise IOError("No such entry in repo:%s" % path)


    def checkout(self , branch):
        self.repo.git.checkout( branch )



    def runTests(self , cmd):
        full_cmd = self.absPath( cmd )
        if not os.path.isfile( full_cmd ):
            raise IOError("Is not an executable file:%s" % cmd)

        if not os.access( full_cmd , os.X_OK):
            raise OSError("File not executable: %s" % cmd)
            
        exit_code = subprocess.call( full_cmd )
        if exit_code == 0:
            return True
        else:
            return False


    def install(self , target, files = [] , directories = []):
        if os.path.exists( target ):
            if not os.path.isdir( target ):
                raise OSError("Target:%s already exists - and is not a directory" % target)
        else:    
            os.makedirs( target )

        for dir in directories:
            if os.path.dirname( dir ):
                target_path = os.path.join( target , os.path.dirname( dir ))
                if not os.path.isdir( target_path ):
                    os.makedirs( target_path )
            
            for dirpath , dirnames , filenames in os.walk( self.absPath(dir)):
                target_path = os.path.join( target , self.relPath( dirpath ))
                if not os.path.isdir( target_path ):
                    os.makedirs( target_path )

                for file in filenames:
                    src_file = os.path.join( dirpath , file )
                    target_file = os.path.join( target_path , file )
                    shutil.copyfile( src_file , target_file )



        for file in files:
            target_file = os.path.join( target , file )
            if os.path.dirname( file ):
                target_path = os.path.join( target , os.path.dirname( file ))
                if not os.path.isdir( target_path ):
                    os.makedirs( target_path )

            shutil.copyfile( self.absPath( file ) , target_file )

        
        