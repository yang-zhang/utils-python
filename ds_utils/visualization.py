import unittest

import sklearn.decomposition
import sklearn.datasets

import seaborn as sns
import matplotlib.pyplot as plt

import ds_utils.preprocessing
import ds_utils.explore


def df_hist(df, col, bins=None):
    ax = plt.axes()
    sns.distplot(df[col].dropna(), bins=bins);
    ax.set_title(col)


def df_scatterplot(df, numerical_col_1, numerical_col_2):
    sns.jointplot(x=numerical_col_1, y=numerical_col_2, data=df);


def df_barplot_frequency(df, col):
    df_freq = ds_utils.explore.df_categorical_col_value_percent(df, col)
    ax = plt.axes()
    sns.barplot(x=col, y='ratio', data=df_freq)
    ax.set_title(col)


def df_boxplot_numerical_col_by_categorical_col(df, numerical_col, categorical_col):
    sns.boxplot(x=categorical_col, y=numerical_col, data=df);


def df_stackedbarplot(df, col_1, col_2):
    df_pivot = ds_utils.explore.df_describe_categorical_col_by_categorical_col(df, col_1, col_2)
    df_pivot.T.plot(kind='bar', stacked=True)


def df_pairplot(df, cols):
    sns.pairplot(df[cols].dropna());


# http://scikit-learn.org/stable/tutorial/statistical_inference/putting_together.html
def plot_pca_explained_variance_ratio(X, n_components=None):
    pca = sklearn.decomposition.PCA(n_components=n_components)
    pca.fit(X)
    plt.figure(1, figsize=(4, 3))
    plt.clf()
    plt.axes([.2, .2, .7, .7])
    plt.plot(pca.explained_variance_ratio_.cumsum(), linewidth=2)
    plt.axis('tight')
    plt.xlabel('n_components')
    plt.ylabel('explained_variance_ratio_')


def plot_df_rows(df, cols, save_as=None):
    fig = plt.figure()
    n, m = df[cols].shape
    for i in range(n):
        ax = fig.add_subplot(n, 1, i + 1)
        ax.plot(df[cols].iloc[i].values, '.-')
        ax.set_title(i)
        ax.set_xlim([-1, m])
        ax.set_ylim([0, 1])
        ax.grid()
    fig.subplots_adjust(hspace=0.4, top=1.2)
    fig.set_figheight(n * 2)
    fig.set_figwidth(16)
    if save_as:
        plt.savefig(save_as)
    else:
        plt.show()


class TestVisualizationMethods(unittest.TestCase):
    # best way to run: in jupyter notebook, run "run ds_utils / visualization.py".
    test_df = ds_utils.testing.make_test_df()
    df = ds_utils.preprocessing.df_cast_column_types(test_df, ds_utils.testing.test_df_dict_dtype_col)

    def test_visual_functions(self):
        df_hist(self.df, 'income')
        plt.show()

        df_scatterplot(self.df, 'income', 'tax')
        plt.show()

        df_barplot_frequency(self.df, 'region')
        plt.show()

        df_boxplot_numerical_col_by_categorical_col(self.df, 'income', 'has_churned')
        plt.show()

        df_stackedbarplot(self.df, 'region', 'product_purchased')
        plt.show()

        df_pairplot(self.df, ['has_churned', 'income', 'price_plan',
                              'product_purchased', 'region', 'tax', 'total_purchase'])
        plt.show()

        plot_pca_explained_variance_ratio(sklearn.datasets.load_digits().data)
        plt.show()


if __name__ == '__main__':
    # best way to run: in jupyter notebook, run "run ds_utils / visualization.py".
    unittest.main()
