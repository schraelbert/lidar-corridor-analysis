FROM mambaorg/micromamba:latest

USER root

WORKDIR /workspace

COPY environment.yml /tmp/environment.yml

RUN micromamba install -y -n base -f /tmp/environment.yml \
    && rm -f /opt/conda/lib/libpdal_plugin_reader_hdf.so \
             /opt/conda/lib/libpdal_plugin_reader_icebridge.so \
    && micromamba clean --all --yes

COPY . /workspace

ENV PATH="/opt/conda/bin:${PATH}"

CMD ["bash"]