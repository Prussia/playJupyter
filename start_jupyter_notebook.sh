echo ${PWD}

cd  ${PWD}

docker run -it --rm -p 8888:8888 -v /Users/prussia/workspaces/jupyter_workspace/jupyter-notebook:/home/jovyan/work \
--user root -e NB_GID=100 -e GEN_CERT=yes -e GRANT_SUDO=yes \
prussia/scipy-notebook