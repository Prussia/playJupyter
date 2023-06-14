From jupyter/scipy-notebook

RUN pip install --upgrade jupyterlab jupyterlab-git jupyterlab-github
RUN jupyter server extension enable jupyterlab_git
RUN jupyter server extension enable jupyterlab_github