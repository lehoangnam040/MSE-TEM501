FROM python:3.6-stretch AS builder

RUN apt-get update -y && apt-get install -y cmake git 
RUN git clone https://github.com/coccoc/coccoc-tokenizer.git

# install cython first for building coccoc-tokenizer
RUN pip install cython wheel setuptools && cd /coccoc-tokenizer && mkdir build && cd build \
    && cmake -DBUILD_PYTHON=1 -DCMAKE_INSTALL_PREFIX=~/.local .. \
    && make install

ADD setup_coccoc.py /coccoc-tokenizer/python/setup.py
RUN cd /coccoc-tokenizer/python && python setup.py sdist bdist_wheel && ls -la dist

FROM python:3.6-slim
COPY --from=builder /coccoc-tokenizer/python/dist/CocCocTokenizer-1.4-cp36-cp36m-linux_x86_64.whl /CocCocTokenizer-1.4-cp36-cp36m-linux_x86_64.whl
RUN pip install /CocCocTokenizer-1.4-cp36-cp36m-linux_x86_64.whl
COPY --from=builder /root/.local /root/.local

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
#RUN pip install pyinstaller
#RUN apt-get update -y && apt-get install -y binutils-common
COPY text_vectorize.json /text_vectorize.json
COPY preprocess.py /preprocess.py
COPY model.h5 /model.h5
COPY server.py /server.py

#RUN pyinstaller --onefile server.py -n server
#
#
#FROM frolvlad/alpine-glibc
#COPY --from=builder /dist/server /server


EXPOSE 5000
CMD ["python", "/server.py"]
