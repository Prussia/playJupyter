From jupyter/scipy-notebook:python-3.8

RUN pip install --upgrade jupyterlab jupyterlab-git jupyterlab-github
RUN jupyter server extension enable jupyterlab_git
RUN jupyter server extension enable jupyterlab_github