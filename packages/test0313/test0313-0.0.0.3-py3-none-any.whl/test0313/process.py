import numpy as np
import pandas as pd
from scipy import stats
from scipy.stats import shapiro
from sklearn.cross_decomposition import PLSRegression
from sklearn.decomposition import PCA
from sklearn.feature_selection import RFE
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from statsmodels.stats.outliers_influence import variance_inflation_factor


class process:
    def __init__(self, df, target_column):
        self.df = df.copy()
        self.target_column = target_column

    def update_df(self, df, target_column):
        self.df = df.copy()
        self.target_column = target_column

    def perform_rfe(self, n_features=5, force=False):
        if not hasattr(self, "rfe_features") or force:
            if not hasattr(self, "X_train") or force:
                X = self.df.drop(self.target_column, axis=1)
                y = self.df[self.target_column]
                self.X_train, _, self.y_train, _ = train_test_split(X, y, test_size=0.3, random_state=42)
            model = LinearRegression()
            rfe = RFE(model, n_features_to_select=n_features)
            rfe.fit(self.X_train, self.y_train)
            self.rfe_features = pd.Series(rfe.support_, index=X.columns)
        return self.rfe_features

    def perform_pca_2d(self, n_components=2, force=False):
        """
        2차원 주성분 분석(PCA)을 수행하여 고차원 데이터를 2차원으로 축소합니다.
        이 방법은 데이터에서 가장 중요한 변동성을 포착하고, 이를 두 개의 주성분으로 요약합니다.

        2차원 PCA는 데이터의 핵심 구조를 시각적으로 이해하는 데 유용하며,
        특히 고차원 데이터셋의 패턴과 관계를 간결하게 표현할 수 있습니다.

        Args:
        n_components (int): 축소할 차원의 수, 여기서는 2.
        force (bool): 기존에 계산된 PCA 결과를 무시하고 새로 계산할지 여부.
        """
        if not hasattr(self, "pca_df") or force:
            X = self.df.drop(self.target_column, axis=1)
            pca = PCA(n_components=n_components)
            components = pca.fit_transform(X)

            # PCA 결과 DataFrame 생성 및 인덱스 맞추기
            self.pca_df = pd.DataFrame(components, columns=[f"PC{i+1}" for i in range(n_components)])
            self.pca_df.index = self.df.index  # 원본 DataFrame의 인덱스를 pca_df에 복사
            self.pca_df["target"] = self.df[self.target_column]
        return self.pca_df

    def perform_pca_3d(self, n_components=3, force=False):
        """
        3차원 PCA를 수행하는 함수입니다.
        고차원 데이터를 3차원으로 축소하여 더욱 복잡한 구조와 패턴을 탐색할 수 있습니다.
        3차원 공간에서 데이터의 변동성을 시각화하여 더욱 입체적인 데이터 분석을 가능하게 합니다.
        """
        if not hasattr(self, "pca_df_3d") or force:
            X = self.df.drop(self.target_column, axis=1)
            pca = PCA(n_components=n_components)
            components = pca.fit_transform(X)

            # PCA 결과 DataFrame 생성 및 인덱스 맞추기
            self.pca_df_3d = pd.DataFrame(components, columns=[f"PC{i+1}" for i in range(n_components)])
            self.pca_df_3d.index = self.df.index  # 원본 DataFrame의 인덱스를 pca_df_3d에 복사
            self.pca_df_3d["target"] = self.df[self.target_column]
        return self.pca_df_3d

    def perform_pls(self, n_components=2, force=False):
        """
        부분 최소 제곱 회귀(PLS)를 사용하여 데이터를 분석합니다.
        PLS는 응답 변수와 예측 변수 간의 관계를 모델링하며, 고차원 데이터에서 유용합니다.
        PLS로 차원이 축소된 데이터를 산점도로 나타냅니다.
        이를 통해 데이터의 패턴과 구조를 시각적으로 이해할 수 있습니다.

        Args:
            n_components (int): 사용할 구성 요소의 수입니다.
            force (bool): 기존에 계산된 PLS 결과를 무시하고 새로 계산할지 여부입니다.

        Returns:
            None: 계산된 PLS 결과는 클래스의 내부 상태에 저장합니다.
        """
        if not hasattr(self, "pls_scores") or force:
            X = self.df.drop(self.target_column, axis=1)
            y = self.df[self.target_column]
            self.pls = PLSRegression(n_components=n_components)
            self.pls.fit(X, y)
            self.pls_scores = self.pls.transform(X)
        return self.pls, self.pls_scores

    def perform_vif(self, vif_threshold=10.0, force=False):
        """
        VIF (Variance Inflation Factor)를 계산하여 다중공선성을 평가하는 함수입니다.
        VIF 값이 높은 변수는 다른 변수와의 강한 상관관계를 가지고 있으며, 이는 회귀 분석 등에서 문제를 일으킬 수 있습니다.
        VIF 값이 임계값을 초과하는 변수는 다르게(Red) 표시하여 다중공선성이 높은 변수를 쉽게 식별할 수 있습니다.

        Args:
            vif_threshold (float): VIF 임계값, 이 값 이상일 경우 다중공선성이 높다고 판단합니다.
            force (bool): True로 설정하면 이미 계산된 VIF 데이터를 무시하고 재계산합니다.

        Returns:
            None: 계산된 VIF 값을 클래스의 내부 상태로 저장합니다.
        """
        if not hasattr(self, "vif_data") or force:
            X = self.df.drop(self.target_column, axis=1)
            # X = cudf.DataFrame(X)
            # 상수값 열 제거
            X = X.loc[:, X.apply(pd.Series.nunique) != 1]
            # X = X.loc[:, X.applymap(cudf.Series.nunique) != 1]

            # 완벽한 상관관계가 있는 변수 확인 및 제거
            self.correlated_features = set()
            correlation_matrix = X.corr()
            for i in range(len(correlation_matrix.columns)):
                for j in range(i):
                    if abs(correlation_matrix.iloc[i, j]) > 0.9:  # 상관계수가 0.9 이상인 경우
                        colname = correlation_matrix.columns[i]
                        self.correlated_features.add(colname)

            X.drop(labels=self.correlated_features, axis=1, inplace=True)

            # VIF 계산
            self.vif_data = pd.DataFrame()
            self.vif_data["feature"] = X.columns
            self.vif_data["VIF"] = [self._calculate_vif_single(X, i) for i in range(X.shape[1])]

            # VIF 값이 높은 특성 식별
            self.high_vif_features = self.vif_data[self.vif_data["VIF"] > vif_threshold]["feature"].to_list()
            return self.vif_data, self.high_vif_features, self.correlated_features

    def _calculate_vif_single(self, X, index):
        try:
            return variance_inflation_factor(X.values, index)
        except Exception as e:
            return None  # 오류 발생 시 None 반환

    def perform_forward_selection(self, sl_enter=0.05, sl_remove=0.05):
        variables = self.df.columns.drop(self.target_column).tolist()
        y = self.df[self.target_column]
        selected_variables = []
        steps, adjusted_r_squared, sv_per_step = [], [], []

        step = 0
        total_variables = len(variables)

        for var in range(total_variables):
            print(f"Progress: Step {var+1}/{total_variables}")
            remainder = list(set(variables) - set(selected_variables))
            pval = pd.Series(dtype="float64", index=remainder)

            for col in remainder:
                X = self.df[selected_variables + [col]]
                model = LinearRegression().fit(X, y)
                y_pred = model.predict(X)
                residuals = y - y_pred
                mse = np.mean(residuals**2)
                n = len(y)
                k = len(X.columns)
                pval[col] = 1 - stats.chi2.cdf(n * mse / k, k)

            min_pval = pval.min()
            if min_pval < sl_enter:
                selected_variables.append(pval.idxmin())
                while len(selected_variables) > 0:
                    selected_X = self.df[selected_variables]
                    model = LinearRegression().fit(selected_X, y)
                    y_pred = model.predict(selected_X)
                    residuals = y - y_pred
                    mse = np.mean(residuals**2)
                    n = len(y)
                    k = len(selected_X.columns)
                    max_pval = 1 - stats.chi2.cdf(n * mse / k, k)
                    if max_pval >= sl_remove:
                        remove_variable = selected_variables[-1]
                        selected_variables = selected_variables[:-1]
                    else:
                        break

                adj_r_squared = 1 - (1 - r2_score(y, model.predict(selected_X))) * (n - 1) / (n - k - 1)
                adjusted_r_squared.append(adj_r_squared)
                sv_per_step.append(selected_variables.copy())
                steps.append(step)
                step += 1
            else:
                break

        self.forward_selection_results = {
            "steps": steps,
            "adjusted_r_squared": adjusted_r_squared,
            "selected_variables": sv_per_step,
        }
        return self.forward_selection_results

    def perform_influence_analysis(self):
        if self.target_column not in self.df.columns:
            raise ValueError(f"Target column '{self.target_column}' not found in dataset")

        X = self.df.drop(self.target_column, axis=1)
        y = self.df[self.target_column]

        # Standardize features for better performance
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        # Linear regression model fitting
        model = LinearRegression()
        model.fit(X_scaled, y)

        y_pred = model.predict(X_scaled)
        residuals = (y - y_pred) / np.sqrt(mean_squared_error(y, y_pred))
        # Standardized residuals
        # residuals = (y - model.predict(X_scaled)) / np.sqrt(model.residues_)

        # Influence analysis
        self.influence_analysis = pd.DataFrame()

        # DFFITS, Cook's Distance, DFBETAS calculation
        self.influence_analysis["DFFITS"] = residuals / np.sqrt(1 - residuals**2)
        self.influence_analysis["D"] = (residuals**2) / X.shape[1]
        dfbetas_columns = ["DFBETAS_" + col for col in X.columns]
        residuals_array = residuals.to_numpy()
        self.influence_analysis = pd.concat(
            [
                self.influence_analysis,
                pd.DataFrame(model.coef_.T * residuals_array[:, np.newaxis], columns=dfbetas_columns),
            ],
            axis=1,
        )
        return self.influence_analysis

    def perform_combine_feature_importance(self):
        if self.vif_data is None and self.rfe_features is None:
            raise ValueError("VIF and RFE results not found. Please run VIF or RFE first.")

        combined_importance = {}

        # RFE 중요도
        if hasattr(self, "rfe_features"):
            for feature, is_selected in self.rfe_features.items():
                if is_selected:
                    combined_importance[feature] = combined_importance.get(feature, 0) + 1

        # VIF 분석
        if hasattr(self, "vif_data"):
            for feature in self.vif_data[self.vif_data["VIF"] < 10]["feature"]:
                combined_importance[feature] = combined_importance.get(feature, 0) + 1

        # 상관관계 분석
        corr_matrix = self.df.corr()
        high_corr_threshold = 0.8
        for col in corr_matrix.columns:
            if corr_matrix[col].abs().max() < high_corr_threshold:
                combined_importance[col] = combined_importance.get(col, 0) + 1

        # 가장 중요한 특성 추출
        top_features = sorted(combined_importance, key=combined_importance.get, reverse=True)
        return top_features

    def perform_shapiro_wilk_test(self):
        """
        Shapiro-Wilk 테스트를 사용하여 데이터셋의 각 수치형 변수가 정규 분포를 따르는지 평가합니다.
        이 테스트는 작은 표본에 대해서도 정규성을 잘 판단합니다.
        테스트 결과에는 각 변수의 통계값, p-value, 정규성 여부가 포함됩니다.
        필터링 옵션을 통해 정규 또는 비정규 분포를 따르는 변수들만 선택적으로 보여줄 수 있습니다.


        Returns:
            None: Shapiro-Wilk 테스트 결과를 클래스의 내부 상태에 저장합니다.
        """
        self.shapiro_results = pd.DataFrame(columns=["Feature", "Statistic", "p-value", "Normality"])

        for column in self.df.columns:
            if self.df[column].dtype in ["float64", "int64"]:  # 수치형 데이터에 대해서만 테스트
                stat, p = shapiro(self.df[column])
                normality = "Yes" if p > 0.05 else "No"
                appenddf = pd.DataFrame(
                    {"Feature": [column], "Statistic": [stat], "p-value": [p], "Normality": [normality]}
                )
                dataFrame = [self.shapiro_results, appenddf]
                self.shapiro_results = pd.concat(dataFrame, ignore_index=True)
        return self.shapiro_results

    def perform_umap(self, n_components=2, n_neighbors=15, min_dist=0.1, metric="euclidean", force=False):
        """
        UMAP 알고리즘을 사용하여 데이터를 저차원으로 축소합니다.
        이 방법은 데이터의 복잡한 구조를 보존하면서 고차원 데이터를 저차원으로 효과적으로 매핑합니다.

        Args:
            n_components (int): 목표 차원 수입니다.
            n_neighbors (int): 근접 이웃의 수입니다. 이 값은 결과의 구조에 영향을 줍니다.
            min_dist (float): 점들 사이의 최소 거리입니다. 이 값이 클수록 더 넓게 분포합니다.
            metric (str): 거리 계산에 사용할 메트릭입니다.
            force (bool): 기존에 계산된 UMAP 결과를 무시하고 새로 계산할지 여부입니다.

        Returns:
            None: 계산된 UMAP 결과는 클래스의 내부 상태에 저장합니다.
        """
        import umap

        if not hasattr(self, "umap_results") or force:
            X = self.df.drop(self.target_column, axis=1)
            self.umap_model = umap.UMAP(
                n_components=n_components, n_neighbors=n_neighbors, min_dist=min_dist, metric=metric
            )
            self.umap_results = self.umap_model.fit_transform(X)
        return self.umap_results

    def perform_hdbscan(self, min_cluster_size=60, min_samples=15, metric="euclidean", force=False):
        """
        HDBSCAN 알고리즘을 사용하여 UMAP의 저차원으로 축소된 결과 데이터를 클러스터링합니다.
        각 데이터 포인트의 로컬 밀도에 따라 클러스터를 동적으로 형성하며 높은 유연성과 정확성을 가집니다.

        Args:
            min_cluster_size (int): 그룹화를 위한 최소한의 클러스터 수입니다.
            min_samples (int): 반경 내 최소 데이터 포인트의 수입니다.
            metric (str): 거리 계산에 사용할 메트릭입니다.
            force (bool): 기존에 계산된 HDBSCAN 결과를 무시하고 새로 계산할지 여부입니다.

        Returns:
            None: 계산된 HDBSCAN 결과는 클래스의 내부 상태에 저장합니다.
        """
        import hdbscan

        if not hasattr(self, "hdbscan_results") or force:
            self.hdbscan_model = hdbscan.HDBSCAN(
                min_cluster_size=min_cluster_size, min_samples=min_samples, metric=metric
            )
            self.hdbscan_results = self.hdbscan_model.fit_predict(self.umap_results)
        return self.hdbscan_results
