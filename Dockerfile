FROM ros:humble-ros-core

RUN apt-get update && apt-get install -y python3-pip python3-venv curl \
    && pip3 install --upgrade pip

RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-venv \
    curl \
    python3-colcon-common-extensions \
 && pip3 install --upgrade pip && rm -rf /var/lib/apt/lists/*

ENV POETRY_VERSION=1.8.0
RUN curl -sSL https://install.python-poetry.org | python3 -

ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app

COPY pyproject.toml poetry.lock /app/

RUN poetry config virtualenvs.create false \
 && poetry install --no-root --no-interaction --no-ansi

COPY . /app/

RUN /bin/bash -c "source /opt/ros/humble/setup.bash && colcon build --packages-select ground_vehicles_system"

ENTRYPOINT ["/bin/bash", "-c", "source /opt/ros/humble/setup.bash && source /app/install/setup.bash && exec \"$@\"", "--"]
CMD ["bash"]
