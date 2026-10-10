# Standard Operating Procedure (SOP) – Raft Cluster Deployment

This document describes how to deploy a three‑node Raft cluster inside the
workspace using Docker‑Compose, run the integration pilot, collect performance
metrics, and visualise the results with a basic Grafana dashboard.

## Prerequisites

* Docker >= 29.8.1 installed on the host (already available in the workspace).
* The `raft_integration` directory present in the workspace (this repository).
* Sufficient disk space – each Raft node runs a lightweight Flask server.

## Steps

1. **Deploy the cluster & run the pilot**
   ```bash
   cd ~/ .openclaw/workspace/raft_integration
   ./scripts/run_cluster.sh
   ```
   The script will:
   * Bring up the three Raft nodes, a Grafana instance and a pilot container.
   * Wait for the pilot to finish its key‑value operations.
   * Copy the generated `metrics/pilot_metrics.json` to
     `metrics/raft_cluster_metrics.json` for downstream consumption.
   * Tear down the Docker‑Compose stack, leaving only the metric file.

2. **Inspect the collected metrics**
   The file `metrics/raft_cluster_metrics.json` contains a JSON object with the
   number of operations performed (`ops`), latency measurements (currently an
   empty array – can be extended in the pilot) and a status field.

3. **Launch Grafana for visualisation**
   ```bash
   docker compose -f docker-compose.yml up -d grafana
   ```
   Grafana will be available at <http://localhost:3000>. The default login is
   `admin` / `admin` (change on first access).

   The provisioning directory `grafana/provisioning/datasources/datasource.yml`
   defines a **TestData** datasource that Grafana ships with. The dashboard
   defined in `grafana/provisioning/dashboards/raft_dashboard.json` displays a
   single stat panel showing the `ops` value from the metrics file.

4. **Import the dashboard** (if not automatically loaded)
   * In Grafana UI, go to *Dashboards → Manage → Import*.
   * Upload `grafana/provisioning/dashboards/raft_dashboard.json`.

5. **Cleanup**
   When finished, stop Grafana:
   ```bash
   docker compose -f docker-compose.yml down grafana
   ```

---

**Notes**

* The Raft nodes are mock implementations; they do not provide real consensus.
  They are sufficient for exercising the bridge and pilot logic.
* The bridge (`skills/raft_bridge/bridge.py`) defaults to the first node
  (`http://raft-node-1:8000`). Override via `RAFT_ENDPOINT` env var if needed.

<!-- project: github.com/gonzoblasco/workspace_openclaw -->
