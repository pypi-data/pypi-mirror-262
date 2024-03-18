# Komodo Package

This is Komodo SDK package.

## Package hierarchy

- komodo/server: FastApi server for the Komodo Appliances
- komodo/models: Implementation of LLM model access and runners to get responses.
-
- komodo/loaders: Loaders for komodo classes and objects.
- komodo/core: Implementation of komodo agents, tools, data sources and other core components.
- komodo/shared: Shared utilities and classes used by other komodo packages.

- komodo/framework: KomodoApp, KomodoAgents, KomodoTool that form the Komodo AI platform.
- komodo/store: Layer that stores and load proto objects from redis database.
- komodo/proto: Protobuf files that define the basic data structures and services.