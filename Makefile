# Makefile for Docker Compose

.PHONY: build build-one up down logs restart shell help

# 镜像 tag，默认为 latest
TAG ?= latest

# 构建所有服务的镜像
build:
	@echo "Building Docker images for all services..."
	@docker-compose build --build-arg TAG=${TAG}

# 构建指定服务的镜像 (例如: make build-image service=backend)
build-image:
	@echo "Building Docker image for service: $(service)..."
	@docker-compose build $(service)

# 在后台启动所有服务
up:
	@echo "Starting all services in detached mode..."
	@docker-compose up -d

# 停止并删除所有服务、网络和卷
down:
	@echo "Stopping and removing all services, networks, and volumes..."
	@docker-compose down -v

# 重启服务
restart: down up

# 查看所有服务的日志
logs:
	@echo "Tailing logs for all services..."
	@docker-compose logs -f

# 进入指定服务的 shell (例如: make shell service=backend)
shell:
	@docker-compose exec $(service) /bin/sh

# 帮助信息
help:
	@echo "Usage: make [target]"
	@echo "Targets:"
	@echo "  build      Build all service images"
	@echo "  build-image  Build a specific service image (e.g., 'make build-image service=backend')"
	@echo "  up         Start all services"
	@echo "  down       Stop and remove all services"
	@echo "  restart    Restart all services"
	@echo "  logs       View logs from all services"
	@echo "  shell      Enter a service's shell (e.g., 'make shell service=backend')"