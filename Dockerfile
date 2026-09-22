FROM debian:bookworm-slim

RUN apt-get update \
    && apt-get install --no-install-recommends -y bash cowsay fortune-mod fortunes-min netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /tmp/wisecow
COPY wisecow.sh /opt/wisecow.sh
RUN chmod 0755 /opt/wisecow.sh \
    && chown 65532:65532 /tmp/wisecow

EXPOSE 4499
ENV PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games"
USER 65532:65532
ENTRYPOINT ["/opt/wisecow.sh"]