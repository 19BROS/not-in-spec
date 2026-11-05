# notinspec-cli image run by the GitHub Action (SPEC §11). Build context: action/
# shortcut: mock CLI only; becomes core + CLI + Prism (Node) + NLI models once core evaluates
FROM python:3.12-slim
RUN apt-get update && apt-get install -y --no-install-recommends git \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir pyyaml==6.0.3
COPY mock.py /opt/notinspec/mock.py
ENTRYPOINT ["python", "/opt/notinspec/mock.py"]
