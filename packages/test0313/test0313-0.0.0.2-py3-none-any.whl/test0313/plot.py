import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
from process import process
from sklearn.cluster import KMeans


class plot:
    def __init__(self, df, target_column):
        self.df = df.copy()
        self.target_column = target_column

    def update_df(self, df, target_column):
        self.df = df.copy()
        self.target_column = target_column

    def plot_correlation_matrix(self):
        """
        데이터셋 내의 모든 변수들 간의 상관관계를 히트맵 형태로 시각화합니다.
        상관계수는 -1부터 +1까지의 값을 가지며, 색상의 강도가 이 값을 나타냅니다.
        밝은 색은 강한 양의 상관관계를, 어두운 색은 강한 음의 상관관계를 나타냅니다.
        0에 가까울수록 색상은 옅어지며, 이는 변수 간 관계가 약하거나 없음을 의미합니다.

        이 행렬은 다음과 같은 분석에 유용합니다:
        1. 다중공선성 문제 식별: 두 변수 간의 상관계수가 매우 높으면(예: 0.8 이상)
        이 변수들은 서로 강하게 연관되어 있으며, 이는 회귀 모델에서 다중공선성 문제를 일으킬 수 있습니다.
        2. 중요한 특성 선별: 타겟 변수와 높은 상관관계를 보이는 변수들은 모델에서 중요한 역할을 할 수 있으며,
        이러한 변수들은 모델의 예측 성능 향상에 기여할 수 있습니다.

        Returns:
            None: 상관관계 행렬을 히트맵 형태로 시각화합니다.
        """
        corr_matrix = self.df.corr()
        fig = px.imshow(corr_matrix, title="Correlation Matrix")
        return fig

    def plot_rfe(self, rfe_features):
        if rfe_features is None:
            raise ValueError("RFE features not found. Please run RFE first.")
        fig = px.bar(rfe_features, title="Feature Importance (RFE)")
        # fig = px.bar(x=self.rfe_features.index, y=self.rfe_features, title="Feature Importance (RFE)")
        return fig

    def plot_pca_2d(self, pca_df):
        if (pca_df is None) or (pca_df.shape[1] < 3):
            raise ValueError("2D PCA results not found. Please run PCA first.")
        fig = px.scatter(pca_df, x="PC1", y="PC2", color="target", title="PCA (2 components)")
        return fig

    def plot_pca_3d(self, pca_df_3d):
        if (pca_df_3d is None) or (pca_df_3d.shape[1] < 3):
            raise ValueError("3D PCA results not found. Please run PCA first.")
        fig = px.scatter_3d(pca_df_3d, x="PC1", y="PC2", z="PC3", color="target", title="PCA (3 components)")
        return fig

    def plot_pls(self, pls, pls_scores, n_components=2):
        if pls is None:
            raise ValueError("pls model not found. Please run PLS first.")
        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=pls_scores[:, 0],
                y=pls_scores[:, 1],
                mode="markers",
                marker=dict(color=self.df[self.target_column]),
                text=self.df.index,
            )
        )
        fig.update_layout(title="PLS (2 components)", xaxis_title="PLS 1", yaxis_title="PLS 2")
        return fig

    def plot_vif(
        self, vif_data=None, high_vif_features=None, correlated_features=None, vif_threshold=10.0, verbose=False
    ):
        if (vif_data is None) or (high_vif_features is None) or (correlated_features is None):
            raise ValueError("VIF results not found. Please run VIF first.")
        fig = px.bar(vif_data, x="feature", y="VIF", title="Variance Inflation Factor (VIF) for Each Feature")
        fig.add_hline(y=vif_threshold, line_dash="dash", line_color="red")

        # VIF 임계값을 초과하는 변수들의 색상을 변경
        colors = ["red" if feature in high_vif_features else "blue" for feature in vif_data["feature"].tolist()]
        fig.data[0].marker.color = colors

        if verbose:
            print("Highly Correlated Features (Correlation > 0.9):", correlated_features)
            print("Features with High VIF (VIF > 10):", high_vif_features)

        return fig

    def plot_forward_selection(self, forward_selection_results=None):
        if forward_selection_results == None:
            raise ValueError("Forward Selection results not found. Please run Forward Selection first.")

        # 저장된 결과를 바탕으로 시각화
        fig = go.Figure()

        for step, adj_r_squared in zip(
            forward_selection_results["steps"], forward_selection_results["adjusted_r_squared"]
        ):
            hover_text = ", ".join(forward_selection_results["selected_variables"][step])
            fig.add_trace(go.Scatter(x=[step], y=[adj_r_squared], mode="markers", hoverinfo="text", text=hover_text))

        fig.update_layout(
            title="Forward Selection Results",
            xaxis=dict(title="Step"),
            yaxis=dict(title="Adjusted R Squared"),
            showlegend=False,
        )

        # 최종 선택된 특성들을 출력
        if forward_selection_results["selected_variables"]:
            final_features = forward_selection_results["selected_variables"][-1]
            print("Final selected features:", final_features)

        return fig

    def plot_influence_analysis(self, influence_analysis=None):
        if influence_analysis is None:
            raise ValueError("Influence Analysis results not found. Please run Influence Analysis first.")

        n = len(self.df)  # 데이터 포인트의 개수
        p = len(self.df.columns) - 1  # 변수의 개수 (타겟 변수 제외)

        # DFFITS 기준
        dffits_threshold = 2 * np.sqrt(p / n)

        # Cook's Distance 기준
        cooks_d_threshold = 0.5  # 누적 확률값 0.5 or 1이상

        # DFBETAS 기준
        dfbetas_threshold = 2 / np.sqrt(n)

        # fig 묶기

        # DFFITS 시각화
        fig = go.Figure()
        fig.add_trace(go.Scatter(y=influence_analysis["DFFITS"], mode="markers", name="DFFITS"))
        fig.add_hline(y=dffits_threshold, line_dash="dash", line_color="red")
        fig.add_hline(y=-dffits_threshold, line_dash="dash", line_color="red")
        fig.update_layout(
            title="DFFITS (Threshold: ±" + str(dffits_threshold) + ")", xaxis_title="Index", yaxis_title="DFFITS"
        )
        return fig

    def plot_clusters(self, n_clusters=3):
        # 데이터 클러스터링
        X = self.df.drop(self.target_column, axis=1)
        kmeans = KMeans(n_clusters=n_clusters, random_state=42).fit(X)
        self.df["Cluster"] = kmeans.labels_

        # 클러스터별 패턴 분석
        cluster_patterns = self.df.groupby("Cluster").mean()

        # 클러스터별 평균 특성 값 시각화
        sns.clustermap(cluster_patterns, cmap="coolwarm", standard_scale=1)
        return cluster_patterns

    def plot_shapiro(self, shapiro_results, filter_normality=None):
        if shapiro_results is None:
            raise ValueError("Shapiro-Wilk results not found. Please run Shapiro-Wilk test first.")

        filtered_results = shapiro_results
        if filter_normality in ["normal", "not-normal"]:
            normality_flag = "Yes" if filter_normality == "normal" else "No"
            filtered_results = shapiro_results[self.shapiro_results["Normality"] == normality_flag]
            filtered_results = shapiro_results[self.shapiro_results["Normality"] == normality_flag]
        print(filtered_results)
        print("\nInterpretation:")
        for _, row in filtered_results.iterrows():
            print(
                f"Feature '{row['Feature']}' - Shapiro Statistic: {row['Statistic']:.3f}, p-value: {row['p-value']:.3f}.",
                end=" ",
            )
            if row["Normality"] == "Yes":
                print("The distribution is likely normal.")
            else:
                print("The distribution is likely not normal.")

    def plot_umap(self, umap_results):
        if umap_results is None:
            raise ValueError("UMAP results not found. Please run UMAP first.")
        fig = px.scatter(
            x=umap_results[:, 0],
            y=umap_results[:, 1],
            color=self.df[self.target_column],
            title="UMAP Visualization",
        )
        return fig

    def plot_hdbscan(self, umap_results, hdbscan_results):
        fig = px.scatter(
            x=umap_results[:, 0],
            y=umap_results[:, 1],
            color=hdbscan_results,
            title="HDBSCAN Visualization",
        )
        return fig
