FROM python:3.10

RUN useradd -ms /bin/bash myuser

<<<<<<< HEAD
COPY requirements.txt /tmp/
RUN pip install --no-cache-dir -r /tmp/requirements.txt

RUN mkdir /workspace && chown myuser:myuser /workspace
>>>>>>> 2881dae (new mods)

USER myuser
CMD ["bash"]
