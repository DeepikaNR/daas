from subprocess import call
import os

from constants import ALLOWED_EXTENSIONS, UPLOAD_FOLDER
#UPLOAD_FOLDER = '/Users/deepikaravi/yojana/restful_docker/uploads/'


def create_docker_folder(tar_file_name, parent_path ='/Users/deepikaravi/yojana/restful_docker/repo/'):
    print "tar_file_name=" + tar_file_name
    folder_name = tar_file_name.split('.')[0]
    docker_path = parent_path + folder_name
    print "mkdir " + docker_path + "..."
    if not os.path.exists(docker_path):
        os.makedirs(docker_path)
    else:
        print "dir exists"
    print "cd " + docker_path + "..."
    os.chdir(docker_path)

    print "untarring..."
    print UPLOAD_FOLDER + folder_name
    print call(["tar", "xvzf", UPLOAD_FOLDER + tar_file_name])

    return docker_path


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

if __name__ == '__main__':
    print create_docker_folder("finite_docker.tar.gz")



