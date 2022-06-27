FROM ubuntu:20.04 as refal_host

RUN apt-get update
RUN apt-get install -y git dos2unix curl unzip sed g++

RUN DEBIAN_FRONTEND=noninteractive apt-get install -y keyboard-configuration
ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt-get update && apt-get install -y python3.10 python3-distutils python3-pip python3-apt
RUN apt install python3-ply
RUN apt-get install python3-pip
RUN pip3 install file_read_backwards
RUN pip3 install graphviz
# RUN pip3 install pydot pydot-ng
RUN apt-get install -y graphviz
# fetch refal-5-lambda
WORKDIR /usr/src
RUN git clone https://github.com/bmstu-iu9/simple-refal-distrib.git

# install refal-5-lambda
WORKDIR /usr/src/simple-refal-distrib
RUN ./bootstrap.sh

ENV PATH="/usr/src/simple-refal-distrib/bin:${PATH}"
ENV RL_MODULE_PATH="/usr/src/simple-refal-distrib/lib:$RL_MODULE_PATH"

# install scp4
WORKDIR /usr/src
RUN curl -LO https://mazdaywik.github.io/direct-link/scp4new-version-05-03-2019-srefc.zip
RUN unzip scp4new-version-05-03-2019-srefc.zip
WORKDIR /usr/src/scp4new-version-05-03-2019-srefc
RUN rlc install
RUN dos2unix doc/install.lst
ENV SHELL="/bin/bash"
RUN ./install linux
RUN sed -i 's/srefc/rlc/g' refcall.bat
RUN ./refcall.bat

ENV PATH="/usr/src/scp4new-version-05-03-2019-srefc:${PATH}"

#install mscp-a
WORKDIR /SuperCompiler/my-app	
COPY MSCPAver1.7z .
RUN apt-get install -y p7zip-full
RUN 7z x MSCPAver1.7z
WORKDIR /SuperCompiler/my-app/MSCPAver1
RUN rlmake mscp-a.ref

#install graphs
WORKDIR /SuperCompiler/my-app	
COPY graphs.7z .
RUN 7z x graphs.7z

#install mscp-a trace
# WORKDIR /SuperCompiler/my-app	
# COPY mscp-trace.7z .
# RUN 7z x mscp-trace.7z
# RUN rlmake mscp-a.ref

#install dot
WORKDIR /SuperCompiler/my-app
COPY decode_graph.ref .
RUN rlmake decode_graph.ref

WORKDIR /SuperCompiler/my-app

WORKDIR /backend

COPY compile.sh .
COPY mscp.sh .
COPY syntaxcompl.sh .
COPY mscpTrace.sh .
COPY graphs.sh .
RUN chmod +x ./compile.sh
RUN chmod +x ./mscp.sh
RUN chmod +x ./syntaxcompl.sh
RUN chmod +x ./mscpTrace.sh
RUN chmod +x ./graphs.sh
COPY setup.sh .
