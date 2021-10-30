# Filename: Dockerfile
FROM jinaai/jina:2.1.12-py38-daemon

# ARG num_docs=20
# ARG data_set=images

COPY . /workspace
WORKDIR /workspace

RUN apt-get update \
    && apt-get install -y --no-install-recommends apt-utils \
    && apt-get install -y wget curl \
    && echo "----------- Installing Python package -----------" \
    && pip3 install -r requirements.txt \
    # && echo "----------- Downloading dataset -----------" \
    # && sh get_data.sh \
    && echo "----------- Indexing dataset -----------" \
    && python main.py -t index -d toy_data
    # && python main.py -t index -d $data_set -n $num_docs

ENTRYPOINT ["python", "main.py"]
CMD [""-t", "query", "--query-image", "data/toy_data/example.jpg" ]