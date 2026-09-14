# Data Management

The syllabus introduces distributed storage, replication, NoSQL, big-data concepts, Hadoop, and Spark. fileciteturn0file0L108-L114

## Current implementation

- PostgreSQL: durable event storage.
- Redis: low-latency queueing and cache-style access.
- Event-oriented records: suitable for batch and stream processing experiments.

## Extension path

For a larger deployment, the same logical pipeline can be moved to object storage plus Spark for batch analytics, while a partitioned/replicated NoSQL store can serve high-volume operational reads. The repository intentionally keeps these boundaries visible so the architectural trade-offs can be demonstrated in a viva rather than hidden behind a framework.
