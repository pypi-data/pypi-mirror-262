from pathlib import Path
from typing import Optional

from docker import DockerClient
from docker.models.containers import Container

from sonaris.defaults import (
    APP_NAME,
    GF_DASHBOARDS_DIR,
    GF_DATASOURCES_DIR,
    GF_PORT,
    GF_SECURITY_ADMIN_PASSWORD,
    SONARIS_NETWORK_NAME,
)
from sonaris.services.container_service import ContainerService
from sonaris.utils.log import get_logger

logger = get_logger()

from sonaris.defaults import GF_INSTALL_PLUGINS, GF_PORT, GF_SECURITY_ADMIN_PASSWORD


class GrafanaService(ContainerService):
    def __init__(
        self,
        client: DockerClient = None,
        port: int = None,
        image: str = None,
        datasources_dir: Path = None,
        dashboards_dir: Path = None,
        network_name: str = None,
        plugins: str = None,
    ):
        super().__init__(
            client=client,
            network_name=network_name if network_name else SONARIS_NETWORK_NAME,
            service_name="grafana",
            image=image or "grafana/grafana",
        )
        self.plugins = plugins or GF_INSTALL_PLUGINS
        self.port = port or GF_PORT
        self.datasources_dir = datasources_dir or GF_DATASOURCES_DIR
        self.dashboards_dir = dashboards_dir or GF_DASHBOARDS_DIR

    def create_container(self, image: str = "grafana/grafana") -> Optional[str]:
        if self.client is None:
            logger.error("Docker client is unavailable. Cannot start Grafana service.")
            return None
        try:
            container: Container = self.client.containers.run(
                image,
                ports={"3000/tcp": self.port},
                environment={
                    "GF_SECURITY_ADMIN_PASSWORD": f"{GF_SECURITY_ADMIN_PASSWORD}",
                    "GF_INSTALL_PLUGINS": self.plugins,
                },
                volumes={
                    str(self.datasources_dir): {
                        "bind": "/etc/grafana/provisioning/datasources",
                        "mode": "rw",
                    },
                    str(self.dashboards_dir): {
                        "bind": "/etc/grafana/provisioning/dashboards",
                        "mode": "rw",
                    },
                },
                labels={f"grafana": self._container_label},
                detach=True,
            )
            if self.network:
                self.network.connect(container)
            logger.info(
                f"Grafana container created and started. Accessible on http://localhost:{self.port}."
            )
            return container.id
        except Exception as e:
            logger.error(f"Failed to create Grafana container: {e}")
            return None
