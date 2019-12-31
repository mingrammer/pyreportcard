FROM python:3.6-alpine

# Prepare a non-root user to run the app in the container
ARG USERNAME=pyreportcard
ARG USER_UID=1000
ARG USER_GID=${USER_UID}

RUN addgroup -g ${USER_GID} ${USERNAME} \
    && adduser -s /bin/sh -u ${USER_UID} -D -G ${USERNAME} ${USERNAME} \
    && apk update \
    && apk add --no-cache --upgrade build-base curl gcc git python3-dev
COPY --chown=${USER_UID}:${USER_GID} . /home/${USERNAME}/app
WORKDIR /home/${USERNAME}/app

RUN pip install --no-cache-dir pipenv \
    && pipenv install --deploy --ignore-pipfile --system

USER ${USERNAME}
EXPOSE 5000

CMD [ "python", "./run.py", "--host", "0.0.0.0", "--debug" ]