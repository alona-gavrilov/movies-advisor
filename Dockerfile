# Use AWS Lambda Python base image
FROM public.ecr.aws/lambda/python:3.9

ENV HF_HOME=/tmp/huggingface
ENV HUGGINGFACE_HUB_CACHE=/tmp/huggingface
ENV SENTENCE_TRANSFORMERS_HOME=/tmp/huggingface


# ---- System dependencies  ----
RUN yum update -y && \
    yum install -y \
        gcc \
        postgresql15 \
        postgresql15-devel \
    && yum clean all   


RUN pip install --no-cache-dir \
    torch==2.2.2+cpu \
    --index-url https://download.pytorch.org/whl/cpu \
    --extra-index-url https://pypi.org/simple \
    sentence-transformers==2.7.0 \
    transformers==4.38.2 \
    huggingface-hub==0.19.4 \
    numpy==1.26.4 \
    psycopg2-binary==2.9.9 \
    typing_extensions \
    requests \
    idna

# Pre-download model into image
RUN python -c "\
from sentence_transformers import SentenceTransformer; \
SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2').save('/opt/model')"    

# Copy function code
COPY app.py ${LAMBDA_TASK_ROOT}

CMD [ "app.handler" ]