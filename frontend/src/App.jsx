import { useEffect, useState } from "react";
import { createPortal } from "react-dom";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from "recharts";
import "./style.css";

const API = "http://127.0.0.1:8000";

const shortId = (id) => {
  if (!id) return "";
  return id.length > 24 ? `${id.slice(0, 24)}...` : id;
};

function App() {
  const [summary, setSummary] = useState({});
  const [optimization, setOptimization] = useState({ recommendations: [] });
  const [ml, setMl] = useState({ results: [] });
  const [resources, setResources] = useState([]);
  const [clusters, setClusters] = useState([]);
  const [approvals, setApprovals] = useState([]);
  const [error, setError] = useState("");
  const [analytics, setAnalytics] = useState(null);
  const [regression, setRegression] = useState(null);
  const [vmLabels, setVmLabels] = useState({});
  const [selectedResource, setSelectedResource] = useState(null);

  const getVmLabel = (id) => {
    if (!id) return "Unknown";
    return vmLabels[id] || shortId(id);
  };

  const buildVmLabels = (...lists) => {
    const map = {};
    let counter = 1;

    lists.flat().forEach((item) => {
      const id =
        typeof item === "string"
          ? item
          : item?.resource_id ?? item?.resourceId;

      if (id && !map[id]) {
        map[id] = `VM-${String(counter).padStart(2, "0")}`;
        counter += 1;
      }
    });

    setVmLabels(map);
  };
  const refreshData = async () => {
  try {
    const response = await fetch(
      `${API}/data/refresh`,
      {
        method: "POST"
      }
    );

    if (!response.ok) {
      throw new Error("Refresh failed");
    }

    await load();

    alert(
      "Current resource data refreshed successfully."
    );

  } catch (error) {

    console.error(error);

    alert(
      "Unable to refresh resource data."
    );
  }
};

  const handleApproval = async (resourceId, status) => {
    try {
      const action = status === "APPROVED" ? "stop" : "keep_running";

      const response = await fetch(
        `${API}/approvals/?resource_id=${encodeURIComponent(
          resourceId
        )}&action=${action}&status=${status}`,
        { method: "POST" }
      );

      if (!response.ok) throw new Error("Approval failed");

      alert(
        `${getVmLabel(resourceId)} ${
          status === "APPROVED" ? "approved" : "rejected"
        } successfully`
      );

      load();
    } catch (e) {
      console.error(e);
      alert("Approval action failed");
    }
  };

  const load = async () => {
    setError("");

    try {
      const summaryRes = await fetch(`${API}/resources/summary`);
      let summaryData = {};
      if (summaryRes.ok) {
        summaryData = await summaryRes.json();
        setSummary(summaryData);
      }

      const resourcesRes = await fetch(`${API}/resources/?limit=50`);
      let resourceData = [];
      if (resourcesRes.ok) {
        resourceData = await resourcesRes.json();
        setResources(Array.isArray(resourceData) ? resourceData : []);
      }

      const recommendationRes = await fetch(`${API}/recommendations/`);
      let recommendationData = { recommendations: [] };
      if (recommendationRes.ok) {
        recommendationData = await recommendationRes.json();
        setOptimization(recommendationData);
      }

      const mlRes = await fetch(`${API}/ml/anomalies`);
      let mlData = { results: [] };
      if (mlRes.ok) {
        mlData = await mlRes.json();
        setMl(mlData);
      }

      const clusterRes = await fetch(`${API}/ml/clusters`);
      let clusterData = { clusters: [] };
      if (clusterRes.ok) {
        clusterData = await clusterRes.json();
        if (Array.isArray(clusterData)) {
          clusterData = { clusters: clusterData };
        }
        setClusters(clusterData.clusters || []);
      }

      const approvalRes = await fetch(`${API}/approvals/`);
      let approvalData = [];
      if (approvalRes.ok) {
        const data = await approvalRes.json();
        approvalData = Array.isArray(data)
          ? data
          : data.approvals || data.results || [];
        setApprovals(approvalData);
      }

      const analyticsResponse = await fetch(`${API}/analytics/overview`);
      let analyticsData = null;
      if (analyticsResponse.ok) {
        analyticsData = await analyticsResponse.json();
        setAnalytics(analyticsData);
      }

      const regressionResponse = await fetch(`${API}/ml/cost-prediction`);
      let regressionData = null;
      if (regressionResponse.ok) {
        regressionData = await regressionResponse.json();
        setRegression(regressionData);
      } else {
        setRegression(null);
      }

      buildVmLabels(
        resourceData,
        recommendationData?.recommendations || [],
        mlData?.results || [],
        clusterData?.clusters || [],
        regressionData?.predictions || [],
        approvalData
      );
    } catch (e) {
      console.error(e);
      setError("Some dashboard data could not be loaded.");
    }
  };

  useEffect(() => {
    load();
  }, []);

  const chartData = resources.map((r) => ({
    name: getVmLabel(r.resource_id),
    fullId: r.resource_id,
    CPU: Number(r.cpu_utilization || 0),
    Memory: Number(r.memory_utilization || 0),
  }));

  const predictionRows = regression?.predictions || [];

  const predictionChartData = predictionRows.slice(0, 12).map((item) => ({
    name: getVmLabel(item.resource_id),
    fullId: item.resource_id,
    Actual: Number(item.actual_cost || 0),
    Predicted: Number(item.predicted_cost || 0),
  }));

  const avgActual = predictionRows.length
    ? predictionRows.reduce(
        (sum, item) => sum + Number(item.actual_cost || 0),
        0
      ) / predictionRows.length
    : 0;

  const avgPredicted = predictionRows.length
    ? predictionRows.reduce(
        (sum, item) => sum + Number(item.predicted_cost || 0),
        0
      ) / predictionRows.length
    : 0;

  const avgDifference = Math.abs(avgActual - avgPredicted);

  const costCarbonData = resources.slice(0, 12).map((r) => ({
    name: getVmLabel(r.resource_id),
    fullId: r.resource_id,
    Cost: Number(r.estimated_cost || 0),
    Carbon: Number(r.carbon_emission || 0),
  }));

  const CustomTooltip = ({ active, payload }) => {
    if (!active || !payload?.length) return null;

    const fullId = payload[0]?.payload?.fullId;

    return (
      <div
        style={{
          background: "#ffffff",
          border: "1px solid #dfe7e2",
          borderRadius: "10px",
          padding: "10px 12px",
          boxShadow: "0 8px 24px rgba(0,0,0,0.08)",
        }}
      >
        <strong>{payload[0]?.payload?.name}</strong>
        {fullId && (
          <div style={{ fontSize: "11px", marginTop: "5px", maxWidth: "260px", wordBreak: "break-all" }}>
            {fullId}
          </div>
        )}
        {payload.map((entry) => (
          <div key={entry.dataKey} style={{ marginTop: "4px" }}>
            {entry.name}: {Number(entry.value || 0).toFixed(2)}
          </div>
        ))}
      </div>
    );
  };

  return (
    <div className="app">
      <style>{resourceIdStyles}</style>
      {/* HEADER */}
      <header>
        <div>
          <p className="eyebrow">GREENOPS</p>
          <h1>Cloud Cost & Carbon Optimization</h1>
          <p className="sub">
            AI-assisted monitoring, anomaly detection and optimization recommendations.
          </p>
        </div>
        <button
          onClick={refreshData}
            className="refresh-btn"
          >
          Refresh Current Data
        </button>
      </header>

      {error && <div className="error">{error}</div>}

      {/* SUMMARY CARDS */}
      <section className="cards">
        <Card title="Resources" value={summary.total_resources ?? 0} />
        <Card
          title="Estimated Cost"
          value={`₹${Number(summary.total_estimated_cost ?? 0).toFixed(2)}`}
        />
        <Card
          title="Carbon Estimate"
          value={Number(summary.total_carbon_emission ?? 0).toFixed(2)}
        />
        <Card
          title="Average CPU"
          value={`${Number(summary.average_cpu_utilization ?? 0).toFixed(2)}%`}
        />
      </section>

      {/* RESOURCE UTILIZATION */}
      <section className="panel chart-section">
        <div className="section-heading">
          <div>
            <h2>📊 Resource Utilization</h2>
            <p className="muted">CPU and memory utilization across cloud resources</p>
          </div>
        </div>

        <ResponsiveContainer width="100%" height={360}>
          <BarChart data={chartData.slice(0, 20)}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" interval={0} />
            <YAxis />
            <Tooltip content={<CustomTooltip />} />
            <Legend />
            <Bar dataKey="CPU" name="CPU %" fill="#16a34a" radius={[5, 5, 0, 0]} />
            <Bar dataKey="Memory" name="Memory %" fill="#86efac" radius={[5, 5, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </section>

      {/* AI OPTIMIZATION */}
      <section className="panel optimization-section">
        <div className="section-heading">
          <div>
            <h2>🤖 AI Optimization Recommendations</h2>
            <p className="muted">
              AI-generated recommendations for reducing cloud cost and carbon emissions
            </p>
          </div>

          <div className="saving-box">
            <span>Potential Monthly Saving</span>
            <strong>₹{Number(optimization.total_potential_monthly_saving ?? 0).toFixed(2)}</strong>
          </div>
        </div>

        <div className="recommendation-grid">
          {optimization.recommendations?.slice(0, 12).map((r, i) => (
            <div className="recommendation-card" key={r.resource_id || i}>
              <div className="recommendation-header">
                <ResourceIdButton resourceId={r.resource_id} label={getVmLabel(r.resource_id)} onClick={setSelectedResource} />
                <span className={`badge ${r.priority?.toLowerCase() || ""}`}>
                  {r.priority}
                </span>
              </div>

              <p className="recommendation-title">{r.recommendation}</p>
              <p className="recommendation-reason">{r.reason}</p>

              <div className="impact">
                <div>
                  💰 Saving
                  <strong>₹{Number(r.estimated_monthly_saving ?? 0).toFixed(2)}</strong>
                </div>
                <div>
                  🌱 Carbon Reduction
                  <strong>{Number(r.estimated_carbon_reduction ?? 0).toFixed(2)}</strong>
                </div>
              </div>

              <div className="approval-buttons">
                <button
                  className="approve-btn"
                  onClick={() => handleApproval(r.resource_id, "APPROVED")}
                >
                  ✓ Approve
                </button>
                <button
                  className="reject-btn"
                  onClick={() => handleApproval(r.resource_id, "REJECTED")}
                >
                  ✕ Reject
                </button>
              </div>
            </div>
          ))}
        </div>

        {!optimization.recommendations?.length && (
          <p className="muted">No recommendations available.</p>
        )}
      </section>

      {/* ISOLATION FOREST */}
      <section className="panel">
        <h2>🤖 AI Anomaly Detection</h2>
        <p className="muted">Algorithm: {ml.algorithm || "Isolation Forest"}</p>

        <div className="anomalyGrid">
          {ml.results?.slice(0, 15).map((r, i) => (
            <div className={`anomaly ${r.anomaly_label?.toLowerCase()}`} key={i}>
              <ResourceIdButton resourceId={r.resource_id} label={getVmLabel(r.resource_id)} onClick={setSelectedResource} />
              <span>{r.anomaly_label}</span>
              <small>
                CPU {r.cpu_utilization}% · Cost ₹{Number(r.estimated_cost || 0).toFixed(2)}
              </small>
            </div>
          ))}
        </div>
      </section>

      {/* K-MEANS */}
      <section className="panel">
        <h2>🤖 AI Resource Clustering</h2>
        <p className="muted">Algorithm: K-Means Clustering</p>

        {clusters.length > 0 ? (
          <div className="anomalyGrid">
            {clusters.slice(0, 15).map((cluster, i) => {
              const resourceId =
                cluster.resource_id ?? cluster.resourceId ?? cluster.id ?? `Resource ${i + 1}`;
              const clusterNumber =
                cluster.cluster ?? cluster.cluster_id ?? cluster.cluster_label ?? "N/A";

              return (
                <div className="anomaly" key={i}>
                  <ResourceIdButton resourceId={resourceId} label={getVmLabel(resourceId)} onClick={setSelectedResource} />
                  <span>Cluster {clusterNumber}</span>
                  <small>
                    CPU {cluster.cpu_utilization ?? cluster.cpu ?? 0}% · Memory {cluster.memory_utilization ?? cluster.memory ?? 0}%
                  </small>
                </div>
              );
            })}
          </div>
        ) : (
          <p className="muted">No clustering data available.</p>
        )}
      </section>

      {/* COST PREDICTION */}
      <section className="panel cost-prediction-panel">
        <div className="panel-header">
          <div>
            <h2>💰 Cost Prediction</h2>
            <p className="muted">Random Forest based cost prediction</p>
          </div>
        </div>

        {regression?.status === "SUCCESS" && predictionRows.length > 0 ? (
          <>
            <div className="cards" style={{ marginBottom: "24px" }}>
              <Card title="Predictions" value={predictionRows.length} />
              <Card title="Average Actual Cost" value={`₹${avgActual.toFixed(2)}`} />
              <Card title="Average Predicted Cost" value={`₹${avgPredicted.toFixed(2)}`} />
              <Card title="Average Difference" value={`₹${avgDifference.toFixed(2)}`} />
            </div>

            <div style={{ marginBottom: "28px" }}>
              <h3 style={{ marginBottom: "6px" }}>Actual vs Predicted Cost</h3>
              <p className="muted" style={{ marginBottom: "18px" }}>
                Comparison of actual resource cost with the Random Forest prediction.
              </p>

              <ResponsiveContainer width="100%" height={330}>
                <BarChart data={predictionChartData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" interval={0} />
                  <YAxis />
                  <Tooltip content={<CustomTooltip />} />
                  <Legend />
                  <Bar dataKey="Actual" name="Actual Cost (₹)" fill="#16a34a" radius={[5, 5, 0, 0]} />
                  <Bar dataKey="Predicted" name="Predicted Cost (₹)" fill="#86efac" radius={[5, 5, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>

            <div className="prediction-table-card">
  <div className="prediction-table-header">
    <div>
      <h3>Prediction Details</h3>
      <p>
        Actual cost compared with the predicted monthly cost
      </p>
    </div>

    <span className="prediction-count">
      {predictionRows.length} Resources
    </span>
  </div>

  <div className="prediction-table-wrapper">
    <table className="prediction-table">
      <thead>
        <tr>
          <th>Resource</th>
          <th>Actual Cost</th>
          <th>Predicted Cost</th>
          <th>Difference</th>
          <th>Prediction Status</th>
        </tr>
      </thead>

      <tbody>
        {predictionRows.slice(0, 20).map((item) => {
          const actual = Number(item.actual_cost || 0);
          const predicted = Number(item.predicted_cost || 0);
          const difference = Math.abs(actual - predicted);

          const percentage =
            actual > 0 ? (difference / actual) * 100 : 0;

          let status = "Accurate";

          if (percentage > 10) {
            status = "High Difference";
          } else if (percentage > 5) {
            status = "Moderate Difference";
          }

          return (
            <tr key={item.resource_id}>
              <td>
                <button
                  type="button"
                  className="vm-id-button"
                  onClick={() =>
                    setSelectedResource(item.resource_id)
                  }
                >
                  {getVmLabel(item.resource_id)}
                </button>
              </td>

              <td>₹{actual.toFixed(2)}</td>

              <td>₹{predicted.toFixed(2)}</td>

              <td>₹{difference.toFixed(2)}</td>

              <td>
                <span
                  className={
                    status === "Accurate"
                      ? "prediction-status accurate"
                      : status === "Moderate Difference"
                      ? "prediction-status moderate"
                      : "prediction-status high"
                  }
                >
                  {status}
                </span>
              </td>
            </tr>
          );
        })}
      </tbody>
    </table>
  </div>
</div>


          </>
        ) : (
          <p className="muted">Regression data unavailable.</p>
        )}
      </section>

      {/* COST + CARBON ANALYTICS */}
      <section className="panel">
        <h2>📊 Cost & Carbon Analytics</h2>
        <p className="muted">
          Overall cloud cost, carbon emission and optimization impact
        </p>

        <div className="cards">
          <Card
            title="Total Monthly Cost"
            value={`₹${Number(analytics?.total_monthly_cost ?? 0).toFixed(2)}`}
          />
          <Card
            title="Total Carbon Emission"
            value={Number(analytics?.total_carbon_emission ?? 0).toFixed(2)}
          />
          <Card
            title="Potential Monthly Saving"
            value={`₹${Number(analytics?.potential_monthly_saving ?? 0).toFixed(2)}`}
          />
          <Card
            title="Potential Carbon Reduction"
            value={Number(analytics?.potential_carbon_reduction ?? 0).toFixed(2)}
          />
        </div>

        <div style={{ marginTop: "30px" }}>
          <h3>Resource Cost vs Carbon Impact</h3>

          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={costCarbonData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" interval={0} />
              <YAxis />
              <Tooltip content={<CustomTooltip />} />
              <Legend />
              <Bar dataKey="Cost" name="Estimated Cost (₹)" fill="#16a34a" />
              <Bar dataKey="Carbon" name="Carbon Emission" fill="#f59e0b" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </section>

      {/* APPROVAL HISTORY */}
      <section className="panel">
        <h2>📋 Approval History</h2>
        <p className="muted">Admin approval and rejection records</p>

        {approvals.length > 0 ? (
          <div>
            {approvals.map((approval, i) => {
              const resourceId =
                approval.resource_id ?? approval.resourceId ?? "Unknown Resource";

              return (
                <div className="item" key={i}>
                  <div>
                    <ResourceIdButton resourceId={resourceId} label={getVmLabel(resourceId)} onClick={setSelectedResource} />
                    <p>Action: {approval.action ?? "N/A"}</p>
                    <small>
                      Created: {approval.created_at ?? approval.createdAt ?? "N/A"}
                    </small>
                  </div>
                  <span className={`badge ${approval.status?.toLowerCase() || ""}`}>
                    {approval.status ?? "UNKNOWN"}
                  </span>
                </div>
              );
            })}
          </div>
        ) : (
          <p className="muted">No approval history available.</p>
        )}
      </section>

      {selectedResource && typeof document !== "undefined" && createPortal(
        <div
          onClick={() => setSelectedResource(null)}
          style={{
            position: "fixed",
            inset: 0,
            width: "100vw",
            height: "100vh",
            background: "rgba(0,0,0,0.48)",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            padding: "20px",
            boxSizing: "border-box",
            zIndex: 2147483647
          }}
        >
          <div
            onClick={(e) => e.stopPropagation()}
            style={{
              width: "min(520px, 92vw)",
              background: "#ffffff",
              borderRadius: "16px",
              padding: "24px",
              boxSizing: "border-box",
              boxShadow: "0 24px 70px rgba(0,0,0,0.30)",
              border: "1px solid #e5e7eb"
            }}
          >
            <div style={{
              display: "flex",
              alignItems: "flex-start",
              justifyContent: "space-between",
              gap: "16px"
            }}>
              <div>
                <div style={{
                  fontSize: "12px",
                  color: "#6b7280",
                  textTransform: "uppercase",
                  letterSpacing: "0.08em",
                  marginBottom: "5px"
                }}>
                  Resource
                </div>
                <h3 style={{ margin: 0, fontSize: "24px", color: "#111827" }}>
                  {getVmLabel(selectedResource)}
                </h3>
              </div>

              <button
                type="button"
                onClick={() => setSelectedResource(null)}
                aria-label="Close"
                style={{
                  border: "none",
                  background: "#f3f4f6",
                  width: "36px",
                  height: "36px",
                  borderRadius: "50%",
                  fontSize: "24px",
                  lineHeight: 1,
                  cursor: "pointer",
                  color: "#374151"
                }}
              >
                ×
              </button>
            </div>

            <div style={{
              marginTop: "22px",
              padding: "16px",
              background: "#f8fafc",
              border: "1px solid #e5e7eb",
              borderRadius: "10px"
            }}>
              <div style={{
                fontSize: "12px",
                color: "#6b7280",
                marginBottom: "9px"
              }}>
                Full Resource ID
              </div>
              <code style={{
                display: "block",
                fontSize: "14px",
                lineHeight: 1.6,
                color: "#166534",
                wordBreak: "break-all"
              }}>
                {selectedResource}
              </code>
            </div>

            <button
              type="button"
              onClick={() => setSelectedResource(null)}
              style={{
                marginTop: "18px",
                width: "100%",
                border: "none",
                borderRadius: "9px",
                padding: "11px 14px",
                background: "#16a34a",
                color: "#ffffff",
                fontWeight: 700,
                cursor: "pointer"
              }}
            >
              Close
            </button>
          </div>
        </div>,
        document.body
      )}

      <footer>
        GreenOps • AI-Driven Cloud Cost, Energy & Carbon Optimization
      </footer>
    </div>
  );
}

function ResourceIdButton({ resourceId, label, onClick }) {
  if (!resourceId) return <span>{label || "Unknown"}</span>;

  const handleClick = (e) => {
    e.preventDefault();
    e.stopPropagation();
    onClick(resourceId);
  };

  return (
    <button
      type="button"
      className="resource-id-button"
      aria-label={`View full Resource ID for ${label || "resource"}`}
      onMouseDown={(e) => e.stopPropagation()}
      onClick={handleClick}
    >
      {label}
    </button>
  );
}

function Card({ title, value }) {
  return (
    <div className="card">
      <span>{title}</span>
      <strong>{value}</strong>
    </div>
  );
}


const resourceIdStyles = `
.resource-id-button {
  border: 0;
  background: transparent;
  padding: 2px 6px;
  margin: 0;
  font: inherit;
  font-weight: 700;
  color: inherit;
  cursor: pointer;
  border-radius: 6px;
  transition: background 0.15s ease, transform 0.15s ease;
}
.resource-id-button:hover {
  background: rgba(22, 163, 74, 0.10);
  transform: translateY(-1px);
}
.resource-id-overlay {
  position: fixed;
  inset: 0;
  z-index: 9999;
  background: rgba(0, 0, 0, 0.42);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}
.resource-id-modal {
  width: min(520px, 100%);
  background: #fff;
  border-radius: 16px;
  padding: 22px;
  box-shadow: 0 20px 60px rgba(0,0,0,0.22);
}
.resource-id-modal-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 16px;
}
.resource-id-modal-header h3 {
  margin: 4px 0 0;
  font-size: 24px;
}
.resource-id-modal-label {
  font-size: 12px;
  color: #6b7280;
  text-transform: uppercase;
  letter-spacing: .08em;
}
.resource-id-close {
  border: 0;
  background: #f3f4f6;
  width: 34px;
  height: 34px;
  border-radius: 50%;
  font-size: 24px;
  cursor: pointer;
}
.resource-id-full {
  margin-top: 20px;
  padding: 15px;
  background: #f8fafc;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
}
.resource-id-full span {
  display: block;
  margin-bottom: 8px;
  font-size: 12px;
  color: #6b7280;
}
.resource-id-full code {
  display: block;
  word-break: break-all;
  font-size: 14px;
  color: #166534;
}
.resource-id-done {
  margin-top: 18px;
  width: 100%;
  border: 0;
  border-radius: 9px;
  padding: 10px 14px;
  background: #16a34a;
  color: white;
  font-weight: 700;
  cursor: pointer;
}
`;

export default App;





