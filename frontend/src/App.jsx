import { useEffect, useState } from "react";
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

const API = "http://127.0.0.1:8000";

function App() {
  const [summary, setSummary] = useState({});
  const [optimization, setOptimization] = useState({
    recommendations: [],
  });
  const [ml, setMl] = useState({
    results: [],
  });
  const [resources, setResources] = useState([]);
  const [clusters, setClusters] = useState([]);
  const [approvals, setApprovals] = useState([]);
  const [error, setError] = useState("");
  const [analytics, setAnalytics] = useState(null);

  // ---------------------------------------
  // LOAD DASHBOARD DATA
  // ---------------------------------------
  const handleApproval = async (resourceId, status) => {
  try {
    const action = status === "APPROVED" ? "stop" : "keep_running";

    const response = await fetch(
      `${API}/approvals/?resource_id=${encodeURIComponent(resourceId)}&action=${action}&status=${status}`,
      {
        method: "POST",
      }
    );

    if (!response.ok) {
      throw new Error("Approval failed");
    }

    alert(
      `${resourceId} ${status === "APPROVED" ? "approved" : "rejected"} successfully`
    );

    load();
  } catch (error) {
    alert("Approval action failed");
    console.error(error);
  }
};
  
  const load = async () => {
    setError("");

    try {
      // Summary
      const summaryRes = await fetch(`${API}/resources/summary`);
      if (summaryRes.ok) {
        setSummary(await summaryRes.json());
      }

      // Resources
      const resourcesRes = await fetch(`${API}/resources/`);
      if (resourcesRes.ok) {
        setResources(await resourcesRes.json());
      }

      // Recommendations
      const recommendationRes = await fetch(
        `${API}/recommendations/`
      );

      if (recommendationRes.ok) {
        setOptimization(await recommendationRes.json());
      }

      // Isolation Forest
      const mlRes = await fetch(`${API}/ml/anomalies`);

      if (mlRes.ok) {
        setMl(await mlRes.json());
      }

      // K-Means
      const clusterRes = await fetch(`${API}/ml/clusters`);

      if (clusterRes.ok) {
        const clusterData = await clusterRes.json();

        if (Array.isArray(clusterData)) {
          setClusters(clusterData);
        } else {
          setClusters(clusterData.clusters || []);
        }
      }

      // Approval History
      const approvalRes = await fetch(`${API}/approvals/`);

      if (approvalRes.ok) {
        const approvalData = await approvalRes.json();

        if (Array.isArray(approvalData)) {
          setApprovals(approvalData);
        } else {
          setApprovals(
            approvalData.approvals ||
            approvalData.results ||
            []
            
          );
        }
      }
      const analyticsResponse = await fetch(
  `${API}/analytics/overview`
);

const analyticsData = await analyticsResponse.json();

setAnalytics(analyticsData);
    } catch (e) {
      console.error(e);
      setError(
        "Some dashboard data could not be loaded."
      );
    }
  };

  useEffect(() => {
    load();
  }, []);

  // ---------------------------------------
  // RESOURCE CHART DATA
  // ---------------------------------------
  const chartData = resources.map((r) => ({
    name: r.resource_id,
    CPU: r.cpu_utilization || 0,
    Memory: r.memory_utilization || 0,
  }));

  return (
    <div className="app">

      {/* HEADER */}
      <header>
        <div>
          <p className="eyebrow">GREENOPS</p>

          <h1>
            Cloud Cost & Carbon Optimization
          </h1>

          <p className="sub">
            AI-assisted monitoring, anomaly detection
            and optimization recommendations.
          </p>
        </div>

        <button onClick={load}>
          Refresh
        </button>
      </header>

      {/* ERROR */}
      {error && (
        <div className="error">
          {error}
        </div>
      )}

      {/* ---------------------------------------
          SUMMARY CARDS
      --------------------------------------- */}
      <section className="cards">

        <Card
          title="Resources"
          value={summary.total_resources ?? 0}
        />

        <Card
          title="Estimated Cost"
          value={`₹${summary.total_estimated_cost ?? 0}`}
        />

        <Card
          title="Carbon Estimate"
          value={`${summary.total_carbon_emission ?? 0}`}
        />

        <Card
          title="Average CPU"
          value={`${summary.average_cpu_utilization ?? 0}%`}
        />

      </section>

     {/* ---------------------------------------
    RESOURCE UTILIZATION
--------------------------------------- */}

<section className="panel chart-section">

  <div className="section-heading">
    <div>
      <h2>📊 Resource Utilization</h2>
      <p className="muted">
        CPU and memory utilization across cloud resources
      </p>
    </div>
  </div>

  <ResponsiveContainer
    width="100%"
    height={360}
  >
    <BarChart data={chartData}>

      <CartesianGrid
        strokeDasharray="3 3"
      />

      <XAxis dataKey="name" />

      <YAxis />

      <Tooltip />

      <Legend />

      <Bar
        dataKey="CPU"
        name="CPU %"
        fill="#16a34a"
        radius={[5, 5, 0, 0]}
      />

      <Bar
        dataKey="Memory"
        name="Memory %"
        fill="#86efac"
        radius={[5, 5, 0, 0]}
      />

    </BarChart>
  </ResponsiveContainer>

</section>


{/* ---------------------------------------
    AI OPTIMIZATION
--------------------------------------- */}

<section className="panel optimization-section">

  <div className="section-heading">

    <div>
      <h2>🤖 AI Optimization Recommendations</h2>

      <p className="muted">
        AI-generated recommendations for reducing
        cloud cost and carbon emissions
      </p>
    </div>

    <div className="saving-box">

      <span>Potential Monthly Saving</span>

      <strong>
        ₹{optimization.total_potential_monthly_saving ?? 0}
      </strong>

    </div>

  </div>


  <div className="recommendation-grid">

    {optimization.recommendations?.map((r, i) => (

      <div
        className="recommendation-card"
        key={i}
      >

        {/* Card Header */}

        <div className="recommendation-header">

          <strong>
            {r.resource_id}
          </strong>

          <span
            className={`badge ${
              r.priority?.toLowerCase()
            }`}
          >
            {r.priority}
          </span>

        </div>


        {/* Recommendation */}

        <p className="recommendation-title">
          {r.recommendation}
        </p>


        {/* Reason */}

        <p className="recommendation-reason">
          {r.reason}
        </p>


        {/* Impact */}

        <div className="impact">

          <div>
            💰 Saving
            <strong>
              ₹{r.estimated_monthly_saving ?? 0}
            </strong>
          </div>

          <div>
            🌱 Carbon Reduction
            <strong>
              {r.estimated_carbon_reduction ?? 0}
            </strong>
          </div>

        </div>


        {/* Actions */}

        <div className="approval-buttons">

          <button
            className="approve-btn"
            onClick={() =>
              handleApproval(
                r.resource_id,
                "APPROVED"
              )
            }
          >
            ✓ Approve
          </button>

          <button
            className="reject-btn"
            onClick={() =>
              handleApproval(
                r.resource_id,
                "REJECTED"
              )
            }
          >
            ✕ Reject
          </button>

        </div>

      </div>

    ))}

  </div>


  {!optimization.recommendations?.length && (

    <p className="muted">
      No recommendations available.
    </p>

  )}

</section>

      {/* ---------------------------------------
          ISOLATION FOREST
      --------------------------------------- */}
      <section className="panel">

        <h2>
          🤖 AI Anomaly Detection
        </h2>

        <p className="muted">
          Algorithm:{" "}
          {ml.algorithm || "Isolation Forest"}
        </p>

        <div className="anomalyGrid">

          {ml.results?.map((r, i) => (

            <div
              className={`anomaly ${
                r.anomaly_label?.toLowerCase()
              }`}
              key={i}
            >

              <strong>
                {r.resource_id}
              </strong>

              <span>
                {r.anomaly_label}
              </span>

              <small>
                CPU {r.cpu_utilization}%
                {" · "}
                Cost ₹{r.estimated_cost}
              </small>

            </div>

          ))}

        </div>

      </section>

      {/* ---------------------------------------
          K-MEANS CLUSTERING
      --------------------------------------- */}
      <section className="panel">

        <h2>
          🤖 AI Resource Clustering
        </h2>

        <p className="muted">
          Algorithm: K-Means Clustering
        </p>

        {clusters.length > 0 ? (

          <div className="anomalyGrid">

            {clusters.map((cluster, i) => {

              const resourceId =
                cluster.resource_id ??
                cluster.resourceId ??
                cluster.id ??
                `Resource ${i + 1}`;

              const clusterNumber =
                cluster.cluster ??
                cluster.cluster_id ??
                cluster.cluster_label ??
                "N/A";

              return (
                <div
                  className="anomaly"
                  key={i}
                >

                  <strong>
                    {resourceId}
                  </strong>

                  <span>
                    Cluster {clusterNumber}
                  </span>

                  <small>
                    CPU{" "}
                    {cluster.cpu_utilization ??
                      cluster.cpu ??
                      0}
                    %
                    {" · "}
                    Memory{" "}
                    {cluster.memory_utilization ??
                      cluster.memory ??
                      0}
                    %
                  </small>

                </div>
              );
            })}

          </div>

        ) : (

          <p className="muted">
            No clustering data available.
          </p>

        )}

      </section>

      {/* ---------------------------------------
    COST + CARBON ANALYTICS
--------------------------------------- */}

<section className="panel">

  <h2>
    📊 Cost & Carbon Analytics
  </h2>

  <p className="muted">
    Overall cloud cost, carbon emission and optimization impact
  </p>

  <div className="cards">

    <Card
      title="Total Monthly Cost"
      value={`₹${analytics?.total_monthly_cost ?? 0}`}
    />

    <Card
      title="Total Carbon Emission"
      value={`${analytics?.total_carbon_emission ?? 0}`}
    />

    <Card
      title="Potential Monthly Saving"
      value={`₹${analytics?.potential_monthly_saving ?? 0}`}
    />

    <Card
      title="Potential Carbon Reduction"
      value={`${analytics?.potential_carbon_reduction ?? 0}`}
    />

  </div>

  <div style={{ marginTop: "30px" }}>

  <h3>Resource Cost vs Carbon Impact</h3>

  <ResponsiveContainer width="100%" height={300}>
    <BarChart
      data={resources.map((r) => ({
        name: r.resource_id,
        Cost: r.estimated_cost || 0,
        Carbon: r.carbon_emission || 0
      }))}
    >
      <CartesianGrid strokeDasharray="3 3" />

      <XAxis dataKey="name" />

      <YAxis />

      <Tooltip />

      <Legend />

  <Bar
  dataKey="Cost"
  name="Estimated Cost (₹)"
  fill="#16a34a"
/>

<Bar
  dataKey="Carbon"
  name="Carbon Emission"
  fill="#f59e0b"
/>

    </BarChart>
  </ResponsiveContainer>

</div>

</section>

      {/* ---------------------------------------
          APPROVAL HISTORY
      --------------------------------------- */}
      <section className="panel">

        <h2>
          📋 Approval History
        </h2>

        <p className="muted">
          Admin approval and rejection records
        </p>

        {approvals.length > 0 ? (

          <div>

            {approvals.map((approval, i) => (

              <div
                className="item"
                key={i}
              >

                <div>

                  <strong>
                    {approval.resource_id ??
                      approval.resourceId ??
                      "Unknown Resource"}
                  </strong>

                  <p>
                    Action:{" "}
                    {approval.action ?? "N/A"}
                  </p>

                  <small>
                    Created:{" "}
                    {approval.created_at ??
                      approval.createdAt ??
                      "N/A"}
                  </small>

                </div>

                <span
                  className={`badge ${
                    approval.status
                      ?.toLowerCase() || ""
                  }`}
                >
                  {approval.status ??
                    "UNKNOWN"}
                </span>

              </div>

            ))}

          </div>

        ) : (

          <p className="muted">
            No approval history available.
          </p>

        )}

      </section>

      {/* FOOTER */}
      <footer>
        GreenOps • AI-Driven Cloud Cost,
        Energy & Carbon Optimization
      </footer>

    </div>
  );
}


// ---------------------------------------
// SUMMARY CARD COMPONENT
// ---------------------------------------
function Card({ title, value }) {

  return (
    <div className="card">

      <span>
        {title}
      </span>

      <strong>
        {value}
      </strong>

    </div>
  );
}


export default App;