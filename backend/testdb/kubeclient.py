from kubernetes import client, config
from postgresTest import settings

config.load_kube_config(config_file=settings.KUBE_CONFIG)
v1 = client.CoreV1Api()
apps_v1 = client.AppsV1Api()
NAMESPACE = "django-backend"

def setup_app(app_name, app_size):
    pvc = client.V1PersistentVolumeClaim(
        metadata=client.V1ObjectMeta(name=f"{app_name}-pvc"),
        spec=client.V1PersistentVolumeClaimSpec(
            storage_class_name="rawfile-localpv",
            access_modes=["ReadWriteOnce"],
            resources=client.V1ResourceRequirements(
                requests={"storage": f"{app_size}Mi"}
            )
        )
    )

    v1.create_namespaced_persistent_volume_claim(namespace=NAMESPACE, body=pvc)

    deployment = client.V1Deployment(
        metadata=client.V1ObjectMeta(name=app_name),
        spec=client.V1DeploymentSpec(
            replicas=1,
            selector={'matchLabels': {'app': app_name}},
            template=client.V1PodTemplateSpec(
                metadata=client.V1ObjectMeta(labels={'app': app_name}),
                spec=client.V1PodSpec(containers=[
                    client.V1Container(
                        name=app_name,
                        image='hub.hamdocker.ir/postgres:latest',
                        ports=[client.V1ContainerPort(container_port=5432)],
                        env=[
                            client.V1EnvVar(name='POSTGRES_DB', value='exampledb'),
                            client.V1EnvVar(name='POSTGRES_USER', value='exampleuser'),
                            client.V1EnvVar(name='POSTGRES_PASSWORD', value='examplepass'),
                            client.V1EnvVar(name='PGDATA', value='/var/lib/postgresql/data/db-files/')
                        ],
                        volume_mounts=[client.V1VolumeMount(
                            name=f"{app_name}-storage",
                            mount_path="/var/lib/postgresql/data"
                        )]
                    )
                ],
                volumes=[client.V1Volume(
                    name=f"{app_name}-storage",
                    persistent_volume_claim=client.V1PersistentVolumeClaimVolumeSource(
                        claim_name=f"{app_name}-pvc"
                    )
                )])
            )
        )
    )

    apps_v1.create_namespaced_deployment(namespace=NAMESPACE, body=deployment)

def get_app(app):
    sanitized_name = app.name.strip().replace(' ', '-')
    pod_list = v1.list_namespaced_pod(namespace=NAMESPACE, label_selector=f"app={sanitized_name}")
    return pod_list

def delete_app(app):
    apps_v1.delete_namespaced_deployment(name=app.name, namespace=NAMESPACE)
    v1.delete_namespaced_persistent_volume_claim(name=f"{app.name}-pvc", namespace=NAMESPACE)

def update_app(app, new_size):
    pvc_name = f"{app.name}-pvc"
    pvc = v1.read_namespaced_persistent_volume_claim(name=pvc_name, namespace=NAMESPACE)
    pvc.spec.resources.requests['storage'] = f"{new_size}Mi"
    v1.patch_namespaced_persistent_volume_claim(name=pvc_name, namespace=NAMESPACE, body=pvc)