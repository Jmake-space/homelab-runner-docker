FROM ghcr.io/actions/actions-runner:2.316.1

USER root
RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends python3 tzdata \
    && python3 -c 'from zoneinfo import ZoneInfo; assert ZoneInfo("America/New_York").key == "America/New_York"' \
    && rm -rf /var/lib/apt/lists/*
USER runner
