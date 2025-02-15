
terraform {
    required_providers {
      kubernetes = {
        source = "hashicorp/kubernetes"
        version = ">=2.4"
      }
    }
}



provider "kubernetes" {
    config_path = "~/.kube/config"
    config_context = "minikube"
}

resource "kubernetes_namespace" "corteva"{
  metadata {
    name = "corteva"
  }
}


resource "kubernetes_manifest" "deployment" {
    manifest = yamldecode(file("${path.module}/../kubernetes-config/deployment.yaml"))
}


resource "kubernetes_manifest" "service" {
    manifest = yamldecode(file("${path.module}/../kubernetes-config/service.yaml"))
}