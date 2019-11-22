"""
========================================
Release Highlights for scikit-learn 0.22
========================================

We are pleased to announce the release of scikit-learn 0.22, which comes
with many bug fixes and new features! We detail below a few of the major
features of this release. For an exhaustive list of all the changes, please
refer to the :ref:`release notes <changes_0_22>`.

To install the latest version (with pip)::

    pip install -U scikit-learn --upgrade

or with conda::

    conda install scikit-learn
"""

##############################################################################
# Permutation-based feature importance
# ------------------------------------
#
# The :func:`~sklearn.inspection.permutation_importance` can be used to get an
# estimate of the importance of each feature, for any fitted estimator:

from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification
from sklearn.inspection import permutation_importance
import matplotlib.pyplot as plt

X, y = make_classification(random_state=0, n_features=5, n_informative=3)
rf = RandomForestClassifier(random_state=0).fit(X, y)
result = permutation_importance(rf, X, y, n_repeats=10, random_state=0,
                                n_jobs=-1)

fig, ax = plt.subplots()
sorted_idx = result.importances_mean.argsort()
ax.boxplot(result.importances[sorted_idx].T,
           vert=False, labels=range(X.shape[1]))
ax.set_title("Permutation Importance of each feature")
ax.set_ylabel("Features")
fig.tight_layout()
plt.show()

##############################################################################
# Native support for missing values for gradient boosting
# -------------------------------------------------------
#
# The :class:`~sklearn.ensemble.HistGradientBoostingClassifier`
# and :class:`~sklearn.ensemble.HistGradientBoostingRegressor` now have native
# support for missing values (NaNs). This means that there is no need for
# imputing data when training or predicting.

from sklearn.experimental import enable_hist_gradient_boosting  # noqa
from sklearn.ensemble import HistGradientBoostingClassifier
import numpy as np

X = np.array([0, 1, 2, np.nan]).reshape(-1, 1)
y = [0, 0, 1, 1]

gbdt = HistGradientBoostingClassifier(min_samples_leaf=1).fit(X, y)
print(gbdt.predict(X))

##############################################################################
# New plotting API
# ----------------
#
# A new plotting API is available for creating visualizations. This new API
# allows for quickly adjusting the visuals of a plot without involving any
# recomputation. It is also possible to add different plots to the same
# figure. See more examples in the :ref:`User Guide <visualizations>`.

from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import plot_roc_curve

X, y = make_classification(random_state=0)
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)

svc = SVC(random_state=42)
svc.fit(X_train, y_train)
rfc = RandomForestClassifier(random_state=42)
rfc.fit(X_train, y_train)

svc_disp = plot_roc_curve(svc, X_test, y_test)
rfc_disp = plot_roc_curve(rfc, X_test, y_test, ax=svc_disp.ax_)
rfc_disp.figure_.suptitle("ROC curve comparison")

plt.show()

#############################################################################
# Tree pruning
# ------------
#
# It is now possible to prune most tree-based estimators once the trees are
# built. The pruning is based on minimal cost-complexity. Read more in the
# :ref:`User Guide <minimal_cost_complexity_pruning>` for details.

X, y = make_classification(random_state=0)

rf = RandomForestClassifier(random_state=0, ccp_alpha=0).fit(X, y)
print("Average number of nodes without pruning {:.1f}".format(
    np.mean([e.tree_.node_count for e in rf.estimators_])))

rf = RandomForestClassifier(random_state=0, ccp_alpha=0.05).fit(X, y)
print("Average number of nodes with pruning {:.1f}".format(
    np.mean([e.tree_.node_count for e in rf.estimators_])))

############################################################################
# Retrieve dataframes from OpenML
# -------------------------------
# :func:`datasets.fetch_openml` can now return pandas dataframe and thus
# properly handle datasets with heterogeneous data:

from sklearn.datasets import fetch_openml

titanic = fetch_openml('titanic', version=1, as_frame=True)
print(titanic.data.head()[['pclass', 'embarked']])
